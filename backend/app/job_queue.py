"""
O.R.E Job Queue - Redis + RQ Integration
Handles async task execution with retry and rollback support
"""
import logging
from redis import Redis
from rq import Queue, Worker
from rq.job import Job
from app.config import settings

logger = logging.getLogger(__name__)

# Initialize Redis connection
redis_conn = Redis.from_url(settings.REDIS_URL)

# Initialize RQ Queue
queue = Queue(settings.RQ_QUEUE_NAME, connection=redis_conn)

def enqueue_task(task):
    """
    Enqueue a task to the job queue
    
    Args:
        task: Task model instance
    
    Returns:
        Job object
    """
    try:
        job = queue.enqueue(
            execute_task,
            task.id,
            timeout=settings.TASK_TIMEOUT,
            job_timeout=settings.TASK_TIMEOUT
        )
        logger.info(f"Task {task.id} enqueued with job {job.id}")
        return job
    except Exception as e:
        logger.error(f"Error enqueuing task: {str(e)}")
        raise

def execute_task(task_id: str):
    """
    Execute a task (called by RQ worker)
    Routes to appropriate agent
    
    Args:
        task_id: Task ID to execute
    
    Returns:
        Task result/output
    """
    from sqlalchemy.orm import Session
    from app.models import Task, TaskStatus
    from app.database import SessionLocal
    
    db = SessionLocal()
    
    try:
        # Get task from database
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        # Update status
        task.status = TaskStatus.RUNNING
        db.commit()
        
        logger.info(f"Executing task {task_id} with agent {task.agent_type}")
        
        # Import and execute appropriate agent
        from app.agents.agent_factory import get_agent
        agent = get_agent(task.agent_type)
        
        # Execute agent
        result = agent.execute(task.input_data)
        
        # Update task with result
        task.output_data = result
        task.status = TaskStatus.COMPLETED
        db.commit()
        
        logger.info(f"Task {task_id} completed successfully")
        return result
        
    except Exception as e:
        logger.error(f"Error executing task {task_id}: {str(e)}")
        task.status = TaskStatus.FAILED
        task.error_message = str(e)
        task.retry_count += 1
        db.commit()
        raise
    
    finally:
        db.close()

def get_job(job_id: str) -> Job:
    """
    Get a job from the queue
    
    Args:
        job_id: Job ID
    
    Returns:
        Job object
    """
    return Job.fetch(job_id, connection=redis_conn)

def cancel_job(job_id: str) -> bool:
    """
    Cancel a job
    
    Args:
        job_id: Job ID
    
    Returns:
        Success status
    """
    try:
        job = Job.fetch(job_id, connection=redis_conn)
        job.cancel()
        logger.info(f"Job {job_id} cancelled")
        return True
    except Exception as e:
        logger.error(f"Error cancelling job: {str(e)}")
        return False

def start_worker():
    """
    Start an RQ worker to process jobs
    """
    worker = Worker([queue], connection=redis_conn)
    logger.info("RQ Worker started")
    worker.work()
