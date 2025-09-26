"""
OBDPHAWD - OBD2 and Automotive Protocol Handler with Bluetooth Low Energy Support

A comprehensive Python library for automotive diagnostics and communication
protocols including OBD2, proprietary protocols, and Bluetooth Low Energy.
"""

__version__ = "0.1.0"
__author__ = "PHAWD Team"
__email__ = "support@phawd.com"

from .core.connection_manager import ConnectionManager
from .protocols.obd2 import OBD2Protocol
from .bluetooth.ble_adapter import BLEAdapter

__all__ = [
    "ConnectionManager",
    "OBD2Protocol", 
    "BLEAdapter",
    "__version__",
]