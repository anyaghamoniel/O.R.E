"""
O.R.E Agent Factory
Factory pattern to instantiate agents by type
"""
from typing import Dict
from app.agents.base_agent import BaseAgent
from app.models import AgentType

# Dictionary to map agent types to agent classes
AGENT_REGISTRY: Dict[str, type] = {}

def register_agent(agent_type: str):
    """
    Decorator to register an agent
    
    Usage:
        @register_agent("video")
        class VideoAgent(BaseAgent):
            ...
    """
    def decorator(agent_class):
        AGENT_REGISTRY[agent_type] = agent_class
        return agent_class
    return decorator

def get_agent(agent_type: str) -> BaseAgent:
    """
    Get an agent instance by type
    
    Args:
        agent_type: Type of agent (e.g., "video", "strategy")
    
    Returns:
        Agent instance
    
    Raises:
        ValueError: If agent type not found
    """
    if agent_type not in AGENT_REGISTRY:
        raise ValueError(f"Agent type '{agent_type}' not registered")
    
    agent_class = AGENT_REGISTRY[agent_type]
    return agent_class()

def list_agents() -> Dict[str, type]:
    """
    List all registered agents
    
    Returns:
        Dictionary of agent types and classes
    """
    return AGENT_REGISTRY.copy()
