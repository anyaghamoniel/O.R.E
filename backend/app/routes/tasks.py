"""
Task API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import TaskCreate, TaskResponse
from app.models import Task
from app.database import get_db
from app.services.task_router import TaskRouter

router = APIRouter()

@router.post("/", response_model=TaskResponse)
async def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task
    """
    try:
        router_service = TaskRouter(db)
        task = router_service.route_task(task_data.dict())
        return task
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str, db: Session = Depends(get_db)):
    """
    Get task by ID
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/user/{user_id}", response_model=list[TaskResponse])
async def get_user_tasks(user_id: str, db: Session = Depends(get_db)):
    """
    Get all tasks for a user
    """
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    return tasks
