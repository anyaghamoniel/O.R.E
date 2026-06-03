"""
O.R.E Task Router - Core Decision Engine
Routes tasks to appropriate agents and manages workflow execution
"""
import uuid
import logging
from datetime import datetime
from typing import Dict, List, Optional
from app.models import Task, Workflow, TaskStatus, AgentType
from app.job_queue import enqueue_task, get_job, cancel_job
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class TaskRouter:
    """
    Core routing engine for O.R.E
    Responsible for:
    - Task validation and categorization
    - Agent selection and routing
    - Workflow orchestration
    - Error handling and rollback
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.agent_registry = self._load_agent_registry()
    
    def _load_agent_registry(self) -> Dict[str, str]:
        """Load available agents from database"""
        agents = self.db.query(Agent).filter(Agent.is_active == True).all()
        return {agent.agent_type: agent.id for agent in agents}
    
    def route_task(self, task_data: Dict) -> Task:
        """
        Route a task to the appropriate agent
        
        Args:
            task_data: {
                "user_id": str,
                "title": str,
                "agent_type": AgentType,
                "input_data": dict
            }
        
        Returns:
            Task object
        """
        try:
            # Validate task
            self._validate_task(task_data)
            
            # Create task
            task = Task(
                id=str(uuid.uuid4()),
                user_id=task_data["user_id"],
                title=task_data["title"],
                description=task_data.get("description"),
                agent_type=task_data["agent_type"],
                input_data=task_data.get("input_data", {}),
                status=TaskStatus.PENDING,
                max_retries=task_data.get("max_retries", 3)
            )
            
            self.db.add(task)
            self.db.commit()
            self.db.refresh(task)
            
            logger.info(f"Task {task.id} created for agent {task.agent_type}")
            
            # Enqueue to job queue
            job = enqueue_task(task)
            task.job_id = job.id
            task.status = TaskStatus.QUEUED
            self.db.commit()
            
            return task
            
        except Exception as e:
            logger.error(f"Error routing task: {str(e)}")
            self.db.rollback()
            raise
    
    def create_workflow(self, workflow_data: Dict) -> Workflow:
        """
        Create a multi-agent workflow
        
        Args:
            workflow_data: {
                "user_id": str,
                "name": str,
                "steps": [
                    {"agent_type": str, "input": dict},
                    ...
                ]
            }
        
        Returns:
            Workflow object
        """
        try:
            # Validate workflow
            self._validate_workflow(workflow_data)
            
            workflow = Workflow(
                id=str(uuid.uuid4()),
                user_id=workflow_data["user_id"],
                name=workflow_data["name"],
                description=workflow_data.get("description"),
                steps=workflow_data["steps"],
                status=TaskStatus.PENDING
            )
            
            self.db.add(workflow)
            self.db.commit()
            self.db.refresh(workflow)
            
            logger.info(f"Workflow {workflow.id} created with {len(workflow.steps)} steps")
            
            return workflow
            
        except Exception as e:
            logger.error(f"Error creating workflow: {str(e)}")
            self.db.rollback()
            raise
    
    def execute_workflow(self, workflow_id: str) -> Workflow:
        """
        Execute a workflow sequentially
        Each step waits for the previous to complete
        """
        try:
            workflow = self.db.query(Workflow).filter(
                Workflow.id == workflow_id
            ).first()
            
            if not workflow:
                raise ValueError(f"Workflow {workflow_id} not found")
            
            workflow.status = TaskStatus.RUNNING
            workflow.started_at = datetime.utcnow()
            self.db.commit()
            
            results = {}
            
            for step_index, step in enumerate(workflow.steps):
                try:
                    # Prepare input for this step
                    step_input = step.get("input", {})
                    
                    # If this step depends on previous output, inject it
                    if step.get("use_previous_output") and step_index > 0:
                        prev_task = workflow.tasks[step_index - 1]
                        step_input = {**step_input, "previous_output": prev_task.output_data}
                    
                    # Create and route task
                    task_data = {
                        "user_id": workflow.user_id,
                        "title": f"{workflow.name} - Step {step_index + 1}",
                        "agent_type": step["agent_type"],
                        "input_data": step_input,
                        "description": f"Workflow step {step_index + 1}"
                    }
                    
                    task = self.route_task(task_data)
                    task.workflow_id = workflow.id
                    self.db.commit()
                    
                    # Wait for task completion
                    task = self._wait_for_task(task)
                    results[step_index] = task.output_data
                    
                    workflow.current_step = step_index + 1
                    self.db.commit()
                    
                except Exception as e:
                    logger.error(f"Workflow step {step_index} failed: {str(e)}")
                    workflow.status = TaskStatus.FAILED
                    workflow.error_message = str(e)
                    self.db.commit()
                    
                    # Rollback workflow
                    self._rollback_workflow(workflow)
                    raise
            
            # All steps completed
            workflow.status = TaskStatus.COMPLETED
            workflow.completed_at = datetime.utcnow()
            workflow.results = results
            self.db.commit()
            
            logger.info(f"Workflow {workflow_id} completed successfully")
            return workflow
            
        except Exception as e:
            logger.error(f"Error executing workflow: {str(e)}")
            raise
    
    def _wait_for_task(self, task: Task, timeout: int = 3600) -> Task:
        """
        Wait for a task to complete
        Polls job queue and updates database
        """
        import time
        start_time = datetime.utcnow()
        
        while (datetime.utcnow() - start_time).seconds < timeout:
            job = get_job(task.job_id)
            
            if job.is_finished:
                task.status = TaskStatus.COMPLETED
                task.completed_at = datetime.utcnow()
                task.output_data = job.result
                self.db.commit()
                return task
            
            elif job.is_failed:
                task.status = TaskStatus.FAILED
                task.error_message = job.exc_info
                self.db.commit()
                return task
            
            time.sleep(1)
        
        raise TimeoutError(f"Task {task.id} timed out")
    
    def _rollback_workflow(self, workflow: Workflow):
        """Rollback workflow execution"""
        try:
            for task in workflow.tasks:
                if task.status in [TaskStatus.RUNNING, TaskStatus.QUEUED]:
                    cancel_job(task.job_id)
                    task.status = TaskStatus.ROLLED_BACK
            
            workflow.status = TaskStatus.ROLLED_BACK
            self.db.commit()
            logger.info(f"Workflow {workflow.id} rolled back")
            
        except Exception as e:
            logger.error(f"Error rolling back workflow: {str(e)}")
    
    def _validate_task(self, task_data: Dict):
        """Validate task data"""
        required_fields = ["user_id", "title", "agent_type"]
        
        for field in required_fields:
            if field not in task_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate agent type
        if task_data["agent_type"] not in [a.value for a in AgentType]:
            raise ValueError(f"Invalid agent type: {task_data['agent_type']}")
    
    def _validate_workflow(self, workflow_data: Dict):
        """Validate workflow data"""
        required_fields = ["user_id", "name", "steps"]
        
        for field in required_fields:
            if field not in workflow_data:
                raise ValueError(f"Missing required field: {field}")
        
        if not isinstance(workflow_data["steps"], list) or len(workflow_data["steps"]) == 0:
            raise ValueError("Workflow must have at least one step")
