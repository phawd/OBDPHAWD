"""Core components for OBDPHAWD."""

from .connection_manager import ConnectionManager
from .exceptions import OBDPHAWDException, ConnectionError, ProtocolError

__all__ = ["ConnectionManager", "OBDPHAWDException", "ConnectionError", "ProtocolError"]