"""
O.R.E Pydantic Schemas for API validation
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel
from app.models import TaskStatus, AgentType

# Task Schemas
class TaskCreate(BaseModel):
    """Create task request"""
    user_id: str
    title: str
    description: Optional[str] = None
    agent_type: str
    input_data: Optional[Dict[str, Any]] = {}
    max_retries: Optional[int] = 3

class TaskResponse(BaseModel):
    """Task response"""
    id: str
    user_id: str
    title: str
    description: Optional[str]
    status: str
    agent_type: str
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]]
    error_message: Optional[str]
    job_id: Optional[str]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Workflow Schemas
class WorkflowStep(BaseModel):
    """Workflow step"""
    agent_type: str
    input: Dict[str, Any]
    use_previous_output: Optional[bool] = False

class WorkflowCreate(BaseModel):
    """Create workflow request"""
    user_id: str
    name: str
    description: Optional[str] = None
    steps: List[WorkflowStep]

class WorkflowResponse(BaseModel):
    """Workflow response"""
    id: str
    user_id: str
    name: str
    description: Optional[str]
    status: str
    steps: List[Dict[str, Any]]
    current_step: int
    results: Optional[Dict[str, Any]]
    error_message: Optional[str]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Agent Schemas
class AgentResponse(BaseModel):
    """Agent response"""
    id: str
    agent_type: str
    name: str
    description: str
    is_active: bool
    version: str
    tasks_completed: int
    tasks_failed: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Health Check
class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    redis_connected: bool
    database_connected: bool
    version: str
