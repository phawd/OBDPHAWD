"""Device scanner for discovering automotive BLE devices."""

import asyncio
import logging
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass

try:
    from bleak import BleakScanner
    from bleak.backends.device import BLEDevice
    BLEAK_AVAILABLE = True
except ImportError:
    BLEAK_AVAILABLE = False
    BleakScanner = None
    BLEDevice = None

from ..core.exceptions import BluetoothError


@dataclass
class AutomotiveDevice:
    """Information about a discovered automotive device."""
    address: str
    name: Optional[str]
    rssi: Optional[int]
    device_type: str
    manufacturer_data: Dict[int, bytes]
    service_uuids: List[str]


class DeviceScanner:
    """Scanner for automotive BLE devices."""
    
    # Known automotive device patterns
    AUTOMOTIVE_KEYWORDS = [
        'obd', 'elm', 'vlink', 'obdii', 'obdlink', 'scantool',
        'veepeak', 'bafx', 'foseal', 'panlong', 'konnwei'
    ]
    
    # Known OBD2 service UUIDs
    OBD2_SERVICE_UUIDS = [
        "0000fff0-0000-1000-8000-00805f9b34fb",
        "0000ffe0-0000-1000-8000-00805f9b34fb",
    ]
    
    def __init__(self):
        if not BLEAK_AVAILABLE:
            raise BluetoothError(
                "Bleak library not available. Install with: pip install bleak"
            )
        
        self.logger = logging.getLogger(__name__)
        self._discovered_devices: Dict[str, AutomotiveDevice] = {}
        self._scan_callbacks: List[Callable[[AutomotiveDevice], None]] = []
    
    async def scan(self, timeout: float = 10.0, 
                  automotive_only: bool = True) -> List[AutomotiveDevice]:
        """
        Scan for BLE devices.
        
        Args:
            timeout: Scan duration in seconds
            automotive_only: If True, filter for automotive devices only
            
        Returns:
            List of discovered automotive devices
        """
        self._discovered_devices.clear()
        
        try:
            self.logger.info(f"Starting BLE scan (timeout: {timeout}s)")
            
            # Start scanning with callback
            await BleakScanner.discover(
                timeout=timeout,
                detection_callback=self._detection_callback
            )
            
            devices = list(self._discovered_devices.values())
            
            if automotive_only:
                devices = [d for d in devices if self._is_automotive_device(d)]
            
            self.logger.info(f"Scan completed. Found {len(devices)} devices")
            return devices
            
        except Exception as e:
            self.logger.error(f"Scan failed: {e}")
            raise BluetoothError(f"Device scan failed: {e}")
    
    async def scan_continuous(self, duration: float = 30.0,
                            callback: Optional[Callable[[AutomotiveDevice], None]] = None) -> None:
        """
        Continuously scan for devices and call callback for each discovery.
        
        Args:
            duration: Total scan duration
            callback: Function to call when a device is discovered
        """
        if callback:
            self._scan_callbacks.append(callback)
        
        try:
            self.logger.info(f"Starting continuous scan for {duration}s")
            
            scanner = BleakScanner(detection_callback=self._detection_callback)
            await scanner.start()
            await asyncio.sleep(duration)
            await scanner.stop()
            
        except Exception as e:
            self.logger.error(f"Continuous scan failed: {e}")
            raise BluetoothError(f"Continuous scan failed: {e}")
        finally:
            if callback in self._scan_callbacks:
                self._scan_callbacks.remove(callback)
    
    def _detection_callback(self, device: BLEDevice, advertisement_data) -> None:
        """Handle device detection during scan."""
        try:
            automotive_device = self._convert_to_automotive_device(
                device, advertisement_data
            )
            
            # Update or add device
            self._discovered_devices[device.address] = automotive_device
            
            # Notify callbacks
            if self._is_automotive_device(automotive_device):
                for callback in self._scan_callbacks:
                    try:
                        callback(automotive_device)
                    except Exception as e:
                        self.logger.error(f"Callback error: {e}")
                        
        except Exception as e:
            self.logger.error(f"Detection callback error: {e}")
    
    def _convert_to_automotive_device(self, device: BLEDevice, 
                                    advertisement_data) -> AutomotiveDevice:
        """Convert BLE device to automotive device."""
        return AutomotiveDevice(
            address=device.address,
            name=device.name,
            rssi=device.rssi if hasattr(device, 'rssi') else None,
            device_type=self._determine_device_type(device, advertisement_data),
            manufacturer_data=advertisement_data.manufacturer_data or {},
            service_uuids=[str(uuid) for uuid in advertisement_data.service_uuids or []]
        )
    
    def _determine_device_type(self, device: BLEDevice, advertisement_data) -> str:
        """Determine the type of automotive device."""
        if device.name:
            name_lower = device.name.lower()
            for keyword in self.AUTOMOTIVE_KEYWORDS:
                if keyword in name_lower:
                    if 'elm' in name_lower:
                        return 'ELM327'
                    elif 'obd' in name_lower:
                        return 'OBD2'
                    elif 'vlink' in name_lower:
                        return 'VLink'
                    else:
                        return 'Unknown Automotive'
        
        # Check service UUIDs
        if advertisement_data.service_uuids:
            for uuid in advertisement_data.service_uuids:
                if str(uuid).lower() in [u.lower() for u in self.OBD2_SERVICE_UUIDS]:
                    return 'OBD2'
        
        return 'Unknown'
    
    def _is_automotive_device(self, device: AutomotiveDevice) -> bool:
        """Check if device is likely an automotive device."""
        # Check name
        if device.name:
            name_lower = device.name.lower()
            if any(keyword in name_lower for keyword in self.AUTOMOTIVE_KEYWORDS):
                return True
        
        # Check service UUIDs
        for uuid in device.service_uuids:
            if uuid.lower() in [u.lower() for u in self.OBD2_SERVICE_UUIDS]:
                return True
        
        return False
    
    def get_device_by_address(self, address: str) -> Optional[AutomotiveDevice]:
        """Get a previously discovered device by address."""
        return self._discovered_devices.get(address)
    
    def get_devices_by_type(self, device_type: str) -> List[AutomotiveDevice]:
        """Get all discovered devices of a specific type."""
        return [device for device in self._discovered_devices.values()
                if device.device_type == device_type]
    
    def clear_discovered_devices(self) -> None:
        """Clear the list of discovered devices."""
        self._discovered_devices.clear()
    
    def list_discovered_devices(self) -> List[AutomotiveDevice]:
        """Get a list of all discovered devices."""
        return list(self._discovered_devices.values())