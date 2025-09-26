"""Bluetooth Low Energy adapter for automotive communication."""

import asyncio
import logging
from typing import Optional, List, Dict, Callable
from uuid import UUID

try:
    from bleak import BleakClient, BleakScanner
    from bleak.backends.device import BLEDevice
    from bleak.backends.characteristic import BleakGATTCharacteristic
    BLEAK_AVAILABLE = True
except ImportError:
    BLEAK_AVAILABLE = False
    BleakClient = None
    BleakScanner = None
    BLEDevice = None
    BleakGATTCharacteristic = None

from ..core.exceptions import BluetoothError, ConnectionError


class BLEAdapter:
    """Bluetooth Low Energy adapter for automotive diagnostics."""
    
    # Common OBD2 BLE service UUIDs
    OBD2_SERVICE_UUID = "0000fff0-0000-1000-8000-00805f9b34fb"
    OBD2_WRITE_CHAR_UUID = "0000fff1-0000-1000-8000-00805f9b34fb"
    OBD2_READ_CHAR_UUID = "0000fff2-0000-1000-8000-00805f9b34fb"
    
    def __init__(self):
        if not BLEAK_AVAILABLE:
            raise BluetoothError(
                "Bleak library not available. Install with: pip install bleak"
            )
        
        self.logger = logging.getLogger(__name__)
        self.client: Optional[BleakClient] = None
        self.device: Optional[BLEDevice] = None
        self.write_char: Optional[BleakGATTCharacteristic] = None
        self.read_char: Optional[BleakGATTCharacteristic] = None
        self._response_queue = asyncio.Queue()
        self._notification_handlers: Dict[str, Callable] = {}
    
    async def scan_devices(self, timeout: float = 10.0) -> List[BLEDevice]:
        """Scan for nearby BLE devices."""
        try:
            self.logger.info(f"Scanning for BLE devices (timeout: {timeout}s)")
            devices = await BleakScanner.discover(timeout=timeout)
            
            # Filter for automotive/OBD2 devices
            automotive_devices = []
            for device in devices:
                if device.name and any(keyword in device.name.lower() 
                                     for keyword in ['obd', 'elm', 'vlink', 'obdii']):
                    automotive_devices.append(device)
            
            self.logger.info(f"Found {len(automotive_devices)} automotive BLE devices")
            return automotive_devices
            
        except Exception as e:
            self.logger.error(f"BLE scan failed: {e}")
            raise BluetoothError(f"Device scan failed: {e}")
    
    async def connect(self, address_or_device) -> None:
        """Connect to a BLE device."""
        try:
            if isinstance(address_or_device, str):
                # Connect by address
                self.client = BleakClient(address_or_device)
            elif isinstance(address_or_device, BLEDevice):
                # Connect by device object
                self.device = address_or_device
                self.client = BleakClient(address_or_device)
            else:
                raise BluetoothError("Invalid device address or device object")
            
            await self.client.connect()
            self.logger.info(f"Connected to BLE device: {self.client.address}")
            
            # Discover services and characteristics
            await self._discover_characteristics()
            
            # Set up notification handling
            if self.read_char:
                await self.client.start_notify(
                    self.read_char, self._notification_handler
                )
                
        except Exception as e:
            self.logger.error(f"BLE connection failed: {e}")
            raise ConnectionError(f"Failed to connect to BLE device: {e}")
    
    async def disconnect(self) -> None:
        """Disconnect from the BLE device."""
        if self.client and self.client.is_connected:
            try:
                if self.read_char:
                    await self.client.stop_notify(self.read_char)
                await self.client.disconnect()
                self.logger.info("Disconnected from BLE device")
            except Exception as e:
                self.logger.error(f"Disconnect error: {e}")
        
        self.client = None
        self.device = None
        self.write_char = None
        self.read_char = None
    
    async def send_receive(self, data: bytes, timeout: float = 5.0) -> bytes:
        """Send data and wait for response."""
        if not self.client or not self.client.is_connected:
            raise ConnectionError("Not connected to BLE device")
        
        if not self.write_char:
            raise BluetoothError("No write characteristic available")
        
        try:
            # Send data
            await self.client.write_gatt_char(self.write_char, data)
            self.logger.debug(f"Sent: {data.hex()}")
            
            # Wait for response
            response = await asyncio.wait_for(
                self._response_queue.get(), timeout=timeout
            )
            self.logger.debug(f"Received: {response.hex()}")
            return response
            
        except asyncio.TimeoutError:
            raise BluetoothError(f"No response within {timeout} seconds")
        except Exception as e:
            raise BluetoothError(f"Send/receive failed: {e}")
    
    async def _discover_characteristics(self) -> None:
        """Discover and set up BLE characteristics."""
        try:
            services = self.client.services
            
            # Look for OBD2 service
            target_service = None
            for service in services:
                if (service.uuid.lower() == self.OBD2_SERVICE_UUID.lower() or
                    'fff0' in service.uuid.lower()):
                    target_service = service
                    break
            
            if not target_service:
                # Use first available service with write/read characteristics
                for service in services:
                    chars = service.characteristics
                    write_chars = [c for c in chars if 'write' in c.properties]
                    read_chars = [c for c in chars if 'read' in c.properties or 'notify' in c.properties]
                    
                    if write_chars and read_chars:
                        target_service = service
                        self.write_char = write_chars[0]
                        self.read_char = read_chars[0]
                        break
            else:
                # Set up characteristics for OBD2 service
                for char in target_service.characteristics:
                    if (char.uuid.lower() == self.OBD2_WRITE_CHAR_UUID.lower() or
                        'fff1' in char.uuid.lower()):
                        self.write_char = char
                    elif (char.uuid.lower() == self.OBD2_READ_CHAR_UUID.lower() or
                          'fff2' in char.uuid.lower()):
                        self.read_char = char
            
            if not self.write_char or not self.read_char:
                raise BluetoothError("Could not find suitable write/read characteristics")
            
            self.logger.info(
                f"Using service: {target_service.uuid}, "
                f"write: {self.write_char.uuid}, read: {self.read_char.uuid}"
            )
            
        except Exception as e:
            raise BluetoothError(f"Characteristic discovery failed: {e}")
    
    def _notification_handler(self, characteristic: BleakGATTCharacteristic, data: bytes) -> None:
        """Handle incoming notifications."""
        try:
            self._response_queue.put_nowait(data)
        except asyncio.QueueFull:
            self.logger.warning("Response queue full, dropping data")
    
    def is_connected(self) -> bool:
        """Check if connected to a device."""
        return self.client is not None and self.client.is_connected
    
    def get_device_info(self) -> Dict[str, str]:
        """Get information about the connected device."""
        if not self.client:
            return {}
        
        info = {
            "address": self.client.address,
            "connected": str(self.is_connected())
        }
        
        if self.device and self.device.name:
            info["name"] = self.device.name
        
        return info