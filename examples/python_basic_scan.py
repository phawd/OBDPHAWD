#!/usr/bin/env python3
"""
Basic example demonstrating BLE device scanning and OBD2 communication.
"""

import asyncio
import sys
import logging
from pathlib import Path

# Add the Python package to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "python"))

from obdphawd import ConnectionManager, OBD2Protocol, BLEAdapter
from obdphawd.bluetooth import DeviceScanner
from obdphawd.core import ConnectionType
from obdphawd.utils import setup_logging


async def main():
    # Set up logging
    setup_logging("INFO", log_to_console=True)
    logger = logging.getLogger("example")
    
    logger.info("OBDPHAWD Basic Example - BLE Scan and OBD2 Communication")
    
    # Initialize device scanner
    scanner = DeviceScanner()
    
    try:
        # Scan for automotive devices
        logger.info("Scanning for automotive BLE devices...")
        devices = await scanner.scan(timeout=10.0, automotive_only=True)
        
        if not devices:
            logger.warning("No automotive devices found")
            return
        
        # Display found devices
        logger.info(f"Found {len(devices)} automotive devices:")
        for i, device in enumerate(devices):
            logger.info(f"  {i+1}. {device.name} ({device.address}) - {device.device_type}")
            logger.info(f"     RSSI: {device.rssi} dBm")
        
        # Select first device for connection
        target_device = devices[0]
        logger.info(f"Connecting to: {target_device.name} ({target_device.address})")
        
        # Initialize connection manager
        conn_manager = ConnectionManager()
        
        # Connect to the device
        connection_id = await conn_manager.connect(
            ConnectionType.BLUETOOTH_LE,
            target_device.address
        )
        
        logger.info(f"Connected! Connection ID: {connection_id}")
        
        # Initialize OBD2 protocol
        obd2 = OBD2Protocol(conn_manager, connection_id)
        
        if await obd2.initialize():
            logger.info("OBD2 protocol initialized successfully")
            
            # Read some basic OBD2 data
            commands_to_try = [
                (0x0C, "Engine RPM"),
                (0x0D, "Vehicle Speed"),
                (0x05, "Engine Coolant Temperature"),
                (0x11, "Throttle Position")
            ]
            
            for pid, description in commands_to_try:
                if pid in obd2.COMMON_PIDS:
                    logger.info(f"Reading {description}...")
                    
                    response = await obd2.send_command(obd2.COMMON_PIDS[pid])
                    
                    if response.success:
                        logger.info(f"  {description}: {response.processed_data}")
                    else:
                        logger.warning(f"  Failed to read {description}: {response.error_message}")
            
            # Read diagnostic trouble codes
            logger.info("Reading diagnostic trouble codes...")
            dtc_codes = await obd2.read_dtc_codes()
            
            if dtc_codes:
                logger.info(f"Found {len(dtc_codes)} diagnostic trouble codes:")
                for code in dtc_codes:
                    logger.info(f"  - {code}")
            else:
                logger.info("No diagnostic trouble codes found")
        
        else:
            logger.error("Failed to initialize OBD2 protocol")
        
        # Disconnect
        await conn_manager.disconnect(connection_id)
        logger.info("Disconnected from device")
        
    except Exception as e:
        logger.error(f"Example failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExample interrupted by user")
    except Exception as e:
        print(f"Example failed: {e}")
        sys.exit(1)