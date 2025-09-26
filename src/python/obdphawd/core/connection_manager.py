"""Connection manager for handling multiple connection types."""

import asyncio
import logging
from typing import Optional, Dict, Any
from enum import Enum

from .exceptions import ConnectionError, TimeoutError


class ConnectionType(Enum):
    """Supported connection types."""
    BLUETOOTH_LE = "ble"
    BLUETOOTH_CLASSIC = "bt_classic"
    USB = "usb"
    SERIAL = "serial"
    WIFI = "wifi"


class ConnectionManager:
    """Manages connections to automotive adapters and vehicles."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.active_connections: Dict[str, Any] = {}
        self._connection_lock = asyncio.Lock()
    
    async def connect(self, connection_type: ConnectionType, 
                     address: str, **kwargs) -> str:
        """
        Establish a connection to an automotive adapter.
        
        Args:
            connection_type: Type of connection to establish
            address: Address/identifier of the target device
            **kwargs: Additional connection parameters
            
        Returns:
            Connection ID for managing the connection
            
        Raises:
            ConnectionError: If connection fails
        """
        async with self._connection_lock:
            try:
                connection_id = f"{connection_type.value}_{address}"
                
                if connection_type == ConnectionType.BLUETOOTH_LE:
                    connection = await self._connect_ble(address, **kwargs)
                elif connection_type == ConnectionType.BLUETOOTH_CLASSIC:
                    connection = await self._connect_bt_classic(address, **kwargs)
                elif connection_type == ConnectionType.USB:
                    connection = await self._connect_usb(address, **kwargs)
                elif connection_type == ConnectionType.SERIAL:
                    connection = await self._connect_serial(address, **kwargs)
                else:
                    raise ConnectionError(f"Unsupported connection type: {connection_type}")
                
                self.active_connections[connection_id] = connection
                self.logger.info(f"Connected to {address} via {connection_type.value}")
                return connection_id
                
            except Exception as e:
                self.logger.error(f"Failed to connect to {address}: {e}")
                raise ConnectionError(f"Connection failed: {e}")
    
    async def disconnect(self, connection_id: str) -> None:
        """Disconnect from a device."""
        async with self._connection_lock:
            if connection_id in self.active_connections:
                connection = self.active_connections.pop(connection_id)
                try:
                    if hasattr(connection, 'disconnect'):
                        await connection.disconnect()
                    elif hasattr(connection, 'close'):
                        connection.close()
                    self.logger.info(f"Disconnected {connection_id}")
                except Exception as e:
                    self.logger.error(f"Error disconnecting {connection_id}: {e}")
    
    async def send_data(self, connection_id: str, data: bytes, 
                       timeout: float = 5.0) -> bytes:
        """Send data and receive response."""
        if connection_id not in self.active_connections:
            raise ConnectionError(f"No active connection: {connection_id}")
        
        connection = self.active_connections[connection_id]
        
        try:
            # Implementation depends on connection type
            if hasattr(connection, 'send_receive'):
                return await asyncio.wait_for(
                    connection.send_receive(data), timeout=timeout
                )
            else:
                raise ConnectionError("Connection doesn't support data transmission")
        except asyncio.TimeoutError:
            raise TimeoutError(f"Data transmission timeout for {connection_id}")
    
    async def _connect_ble(self, address: str, **kwargs) -> Any:
        """Connect via Bluetooth Low Energy."""
        from ..bluetooth.ble_adapter import BLEAdapter
        
        adapter = BLEAdapter()
        await adapter.connect(address)
        return adapter
    
    async def _connect_bt_classic(self, address: str, **kwargs) -> Any:
        """Connect via Bluetooth Classic."""
        # Placeholder for Bluetooth Classic implementation
        raise ConnectionError("Bluetooth Classic not yet implemented")
    
    async def _connect_usb(self, device_path: str, **kwargs) -> Any:
        """Connect via USB."""
        # Placeholder for USB implementation
        raise ConnectionError("USB connection not yet implemented")
    
    async def _connect_serial(self, port: str, **kwargs) -> Any:
        """Connect via Serial port."""
        # Placeholder for Serial implementation
        raise ConnectionError("Serial connection not yet implemented")
    
    def list_connections(self) -> Dict[str, str]:
        """List all active connections."""
        return {conn_id: str(type(conn).__name__) 
                for conn_id, conn in self.active_connections.items()}
    
    async def close_all(self) -> None:
        """Close all active connections."""
        connection_ids = list(self.active_connections.keys())
        for connection_id in connection_ids:
            await self.disconnect(connection_id)