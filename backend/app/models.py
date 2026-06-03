"""
O.R.E Database Models
"""
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, DateTime, JSON, Integer, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class TaskStatus(str, Enum):
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"

class AgentType(str, Enum):
    STRATEGY = "strategy"
    SCRIPT = "script"
    VIDEO = "video"
    VOICE = "voice"
    MEDIA = "media"
    DISTRIBUTION = "distribution"

class Task(Base):
    """Task model"""
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    status = Column(String, default=TaskStatus.PENDING, index=True)
    agent_type = Column(String, index=True)
    workflow_id = Column(String, ForeignKey("workflows.id"), nullable=True)
    
    # Input/Output
    input_data = Column(JSON)
    output_data = Column(JSON, nullable=True)
    
    # Error handling & retries
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Job Queue
    job_id = Column(String, nullable=True, unique=True, index=True)
    
    def __repr__(self):
        return f"<Task {self.id} - {self.agent_type} - {self.status}>"

class Workflow(Base):
    """Workflow model for multi-agent task execution"""
    __tablename__ = "workflows"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    status = Column(String, default=TaskStatus.PENDING, index=True)
    
    # Workflow structure
    steps = Column(JSON)  # List of agent tasks in order
    current_step = Column(Integer, default=0)
    
    # Results
    results = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    tasks = relationship("Task", foreign_keys=[Task.workflow_id])
    
    def __repr__(self):
        return f"<Workflow {self.id} - {self.status}>"

class Agent(Base):
    """Agent model"""
    __tablename__ = "agents"
    
    id = Column(String, primary_key=True, index=True)
    agent_type = Column(String, unique=True, index=True)
    name = Column(String)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    
    # Metadata
    version = Column(String, default="1.0.0")
    config = Column(JSON, nullable=True)
    
    # Stats
    tasks_completed = Column(Integer, default=0)
    tasks_failed = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Agent {self.agent_type}>"

class TaskLog(Base):
    """Task execution logs"""
    __tablename__ = "task_logs"
    
    id = Column(String, primary_key=True, index=True)
    task_id = Column(String, ForeignKey("tasks.id"), index=True)
    level = Column(String)  # INFO, WARNING, ERROR
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<TaskLog {self.task_id} - {self.level}>"
