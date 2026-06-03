"""
Agent API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import AgentResponse
from app.models import Agent
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=list[AgentResponse])
async def list_agents(db: Session = Depends(get_db)):
    """
    List all available agents
    """
    agents = db.query(Agent).filter(Agent.is_active == True).all()
    return agents

@router.get("/{agent_type}", response_model=AgentResponse)
async def get_agent(agent_type: str, db: Session = Depends(get_db)):
    """
    Get agent by type
    """
    agent = db.query(Agent).filter(Agent.agent_type == agent_type).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent
