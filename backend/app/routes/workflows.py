"""
Workflow API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import WorkflowCreate, WorkflowResponse
from app.models import Workflow
from app.database import get_db
from app.services.task_router import TaskRouter

router = APIRouter()

@router.post("/", response_model=WorkflowResponse)
async def create_workflow(workflow_data: WorkflowCreate, db: Session = Depends(get_db)):
    """
    Create a new workflow
    """
    try:
        router_service = TaskRouter(db)
        workflow = router_service.create_workflow(workflow_data.dict())
        return workflow
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{workflow_id}/execute", response_model=WorkflowResponse)
async def execute_workflow(workflow_id: str, db: Session = Depends(get_db)):
    """
    Execute a workflow
    """
    try:
        router_service = TaskRouter(db)
        workflow = router_service.execute_workflow(workflow_id)
        return workflow
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(workflow_id: str, db: Session = Depends(get_db)):
    """
    Get workflow by ID
    """
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow
