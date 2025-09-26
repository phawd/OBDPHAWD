"""Base class for automotive communication protocols."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging


class BaseProtocol(ABC):
    """Base class for automotive communication protocols."""
    
    def __init__(self, connection_manager, connection_id: str):
        self.connection_manager = connection_manager
        self.connection_id = connection_id
        self.logger = logging.getLogger(self.__class__.__name__)
        self._protocol_config: Dict[str, Any] = {}
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the protocol. Returns True if successful."""
        pass
    
    @abstractmethod
    async def send_command(self, command: Any) -> Any:
        """Send a command and return the response."""
        pass
    
    @abstractmethod
    def parse_response(self, raw_data: bytes) -> Any:
        """Parse raw response data into a structured format."""
        pass
    
    def set_config(self, key: str, value: Any) -> None:
        """Set a protocol configuration parameter."""
        self._protocol_config[key] = value
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get a protocol configuration parameter."""
        return self._protocol_config.get(key, default)
    
    async def cleanup(self) -> None:
        """Cleanup protocol resources."""
        pass