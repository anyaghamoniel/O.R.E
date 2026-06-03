"""
O.R.E Base Agent - Abstract class for all agents
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """
    Base class for all O.R.E agents
    Each agent inherits from this and implements execute()
    """
    
    def __init__(self, agent_type: str, name: str):
        self.agent_type = agent_type
        self.name = name
    
    @abstractmethod
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute agent task
        
        Args:
            input_data: Input parameters for the agent
        
        Returns:
            Output/result from agent
        """
        pass
    
    def validate_input(self, input_data: Dict[str, Any]):
        """
        Validate input data (override in subclasses)
        
        Args:
            input_data: Input to validate
        
        Raises:
            ValueError: If validation fails
        """
        pass
    
    def log_execution(self, message: str, level: str = "info"):
        """
        Log agent execution
        
        Args:
            message: Log message
            level: Log level (info, warning, error)
        """
        if level == "info":
            logger.info(f"[{self.name}] {message}")
        elif level == "warning":
            logger.warning(f"[{self.name}] {message}")
        elif level == "error":
            logger.error(f"[{self.name}] {message}")
