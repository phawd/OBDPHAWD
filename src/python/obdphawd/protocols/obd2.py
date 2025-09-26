"""OBD2 protocol implementation."""

import asyncio
import time
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
from enum import Enum

from .base_protocol import BaseProtocol
from ..core.exceptions import ProtocolError, TimeoutError


class OBD2Mode(Enum):
    """OBD2 diagnostic modes."""
    CURRENT_DATA = 0x01
    FREEZE_FRAME = 0x02
    STORED_CODES = 0x03
    CLEAR_CODES = 0x04
    OXYGEN_SENSOR = 0x05
    MONITOR_RESULTS = 0x06
    PENDING_CODES = 0x07
    CONTROL_OPERATION = 0x08
    VEHICLE_INFO = 0x09
    PERMANENT_CODES = 0x0A


@dataclass
class OBD2Command:
    """OBD2 command structure."""
    mode: OBD2Mode
    pid: int
    description: str
    bytes_expected: int = 0
    formula: Optional[str] = None


@dataclass
class OBD2Response:
    """OBD2 response structure."""
    command: OBD2Command
    raw_data: bytes
    processed_data: Any
    timestamp: float
    success: bool
    error_message: Optional[str] = None


class OBD2Protocol(BaseProtocol):
    """OBD2 protocol implementation."""
    
    # Common OBD2 PIDs for Mode 01 (Current Data)
    COMMON_PIDS = {
        0x00: OBD2Command(OBD2Mode.CURRENT_DATA, 0x00, "PIDs supported [01-20]", 4),
        0x01: OBD2Command(OBD2Mode.CURRENT_DATA, 0x01, "Monitor status since DTCs cleared", 4),
        0x02: OBD2Command(OBD2Mode.CURRENT_DATA, 0x02, "Freeze DTC", 2),
        0x03: OBD2Command(OBD2Mode.CURRENT_DATA, 0x03, "Fuel system status", 2),
        0x04: OBD2Command(OBD2Mode.CURRENT_DATA, 0x04, "Calculated engine load", 1, "A*100/255"),
        0x05: OBD2Command(OBD2Mode.CURRENT_DATA, 0x05, "Engine coolant temperature", 1, "A-40"),
        0x06: OBD2Command(OBD2Mode.CURRENT_DATA, 0x06, "Short term fuel trim—Bank 1", 1, "(A-128)*100/128"),
        0x07: OBD2Command(OBD2Mode.CURRENT_DATA, 0x07, "Long term fuel trim—Bank 1", 1, "(A-128)*100/128"),
        0x08: OBD2Command(OBD2Mode.CURRENT_DATA, 0x08, "Short term fuel trim—Bank 2", 1, "(A-128)*100/128"),
        0x09: OBD2Command(OBD2Mode.CURRENT_DATA, 0x09, "Long term fuel trim—Bank 2", 1, "(A-128)*100/128"),
        0x0A: OBD2Command(OBD2Mode.CURRENT_DATA, 0x0A, "Fuel pressure", 1, "A*3"),
        0x0B: OBD2Command(OBD2Mode.CURRENT_DATA, 0x0B, "Intake manifold absolute pressure", 1, "A"),
        0x0C: OBD2Command(OBD2Mode.CURRENT_DATA, 0x0C, "Engine RPM", 2, "((A*256)+B)/4"),
        0x0D: OBD2Command(OBD2Mode.CURRENT_DATA, 0x0D, "Vehicle speed", 1, "A"),
        0x0E: OBD2Command(OBD2Mode.CURRENT_DATA, 0x0E, "Timing advance", 1, "(A-128)/2"),
        0x0F: OBD2Command(OBD2Mode.CURRENT_DATA, 0x0F, "Intake air temperature", 1, "A-40"),
        0x10: OBD2Command(OBD2Mode.CURRENT_DATA, 0x10, "MAF air flow rate", 2, "((A*256)+B)/100"),
        0x11: OBD2Command(OBD2Mode.CURRENT_DATA, 0x11, "Throttle position", 1, "A*100/255"),
    }
    
    def __init__(self, connection_manager, connection_id: str):
        super().__init__(connection_manager, connection_id)
        self._elm_mode = True  # Assume ELM327 adapter initially
        self._supported_pids: Dict[int, List[int]] = {}
        self._protocol_detected = False
    
    async def initialize(self) -> bool:
        """Initialize OBD2 protocol."""
        try:
            self.logger.info("Initializing OBD2 protocol")
            
            # Send ELM327 initialization commands
            if self._elm_mode:
                await self._initialize_elm327()
            
            # Test basic communication
            response = await self.send_command(self.COMMON_PIDS[0x01])  # Monitor status
            if response.success:
                self._protocol_detected = True
                self.logger.info("OBD2 protocol initialized successfully")
                
                # Query supported PIDs
                await self._query_supported_pids()
                return True
            else:
                self.logger.error("Failed to initialize OBD2 protocol")
                return False
                
        except Exception as e:
            self.logger.error(f"OBD2 initialization failed: {e}")
            return False
    
    async def _initialize_elm327(self) -> None:
        """Initialize ELM327 adapter."""
        elm_commands = [
            b"ATZ\r",      # Reset
            b"ATE0\r",     # Echo off
            b"ATL0\r",     # Linefeeds off
            b"ATS0\r",     # Spaces off
            b"ATH1\r",     # Headers on
            b"ATSP0\r",    # Set protocol auto
        ]
        
        for cmd in elm_commands:
            try:
                await asyncio.sleep(0.1)  # Small delay between commands
                await self.connection_manager.send_data(
                    self.connection_id, cmd, timeout=2.0
                )
            except Exception as e:
                self.logger.warning(f"ELM327 command {cmd} failed: {e}")
    
    async def send_command(self, command: OBD2Command, timeout: float = 5.0) -> OBD2Response:
        """Send OBD2 command and return response."""
        try:
            # Format command
            cmd_bytes = self._format_command(command)
            
            # Send command
            raw_response = await self.connection_manager.send_data(
                self.connection_id, cmd_bytes, timeout=timeout
            )
            
            # Parse response
            processed_data = self._parse_obd2_response(command, raw_response)
            
            return OBD2Response(
                command=command,
                raw_data=raw_response,
                processed_data=processed_data,
                timestamp=time.time(),
                success=True
            )
            
        except Exception as e:
            self.logger.error(f"Command {command.description} failed: {e}")
            return OBD2Response(
                command=command,
                raw_data=b"",
                processed_data=None,
                timestamp=time.time(),
                success=False,
                error_message=str(e)
            )
    
    def _format_command(self, command: OBD2Command) -> bytes:
        """Format OBD2 command for transmission."""
        if self._elm_mode:
            # ELM327 format: "01 0C\r" for Mode 01, PID 0C
            cmd_str = f"{command.mode.value:02X} {command.pid:02X}\r"
            return cmd_str.encode('ascii')
        else:
            # Raw OBD2 format
            return bytes([command.mode.value, command.pid])
    
    def _parse_obd2_response(self, command: OBD2Command, raw_data: bytes) -> Any:
        """Parse raw OBD2 response data."""
        try:
            if self._elm_mode:
                # Parse ELM327 response
                response_str = raw_data.decode('ascii').strip()
                
                # Remove common ELM327 response prefixes/suffixes
                response_str = response_str.replace('>', '').replace('\r', '').replace('\n', '')
                
                # Check for errors
                if 'NO DATA' in response_str or 'ERROR' in response_str:
                    raise ProtocolError(f"OBD2 error: {response_str}")
                
                # Extract hex data
                hex_parts = response_str.split()
                if len(hex_parts) < 2:
                    raise ProtocolError(f"Invalid response format: {response_str}")
                
                # Verify response matches command
                response_mode = int(hex_parts[0], 16)
                response_pid = int(hex_parts[1], 16)
                
                if response_mode != (command.mode.value + 0x40):
                    raise ProtocolError(f"Mode mismatch: expected {command.mode.value + 0x40:02X}, got {response_mode:02X}")
                
                if response_pid != command.pid:
                    raise ProtocolError(f"PID mismatch: expected {command.pid:02X}, got {response_pid:02X}")
                
                # Extract data bytes
                data_bytes = [int(hex_part, 16) for hex_part in hex_parts[2:]]
                
                # Apply formula if available
                if command.formula and data_bytes:
                    return self._apply_formula(command.formula, data_bytes)
                else:
                    return data_bytes
            else:
                # Parse raw OBD2 response
                if len(raw_data) < 2:
                    raise ProtocolError("Response too short")
                
                # Extract data portion (skip mode and PID echo)
                data_bytes = list(raw_data[2:])
                
                if command.formula and data_bytes:
                    return self._apply_formula(command.formula, data_bytes)
                else:
                    return data_bytes
                    
        except Exception as e:
            raise ProtocolError(f"Response parsing failed: {e}")
    
    def _apply_formula(self, formula: str, data_bytes: List[int]) -> Union[int, float]:
        """Apply formula to convert raw data to meaningful values."""
        try:
            # Create variables for formula
            variables = {}
            for i, byte_val in enumerate(data_bytes):
                variables[chr(ord('A') + i)] = byte_val
            
            # Evaluate formula
            result = eval(formula, {"__builtins__": {}}, variables)
            return result
            
        except Exception as e:
            self.logger.error(f"Formula evaluation failed: {e}")
            return data_bytes[0] if data_bytes else 0
    
    async def _query_supported_pids(self) -> None:
        """Query which PIDs are supported by the vehicle."""
        try:
            # Query PID support for ranges
            pid_ranges = [0x00, 0x20, 0x40, 0x60, 0x80, 0xA0, 0xC0]
            
            for base_pid in pid_ranges:
                if base_pid in self.COMMON_PIDS:
                    response = await self.send_command(self.COMMON_PIDS[base_pid])
                    if response.success and isinstance(response.processed_data, list):
                        # Parse supported PIDs bitmap
                        supported = self._parse_pid_support(response.processed_data, base_pid)
                        self._supported_pids[base_pid] = supported
                        
        except Exception as e:
            self.logger.error(f"PID support query failed: {e}")
    
    def _parse_pid_support(self, data_bytes: List[int], base_pid: int) -> List[int]:
        """Parse PID support bitmap."""
        supported = []
        if len(data_bytes) >= 4:
            # Convert 4 bytes to 32-bit bitmap
            bitmap = (data_bytes[0] << 24) | (data_bytes[1] << 16) | (data_bytes[2] << 8) | data_bytes[3]
            
            # Check each bit
            for i in range(32):
                if bitmap & (1 << (31 - i)):
                    supported.append(base_pid + i + 1)
        
        return supported
    
    def parse_response(self, raw_data: bytes) -> OBD2Response:
        """Parse raw response data."""
        # This is a simplified version - normally would need context of the command
        return OBD2Response(
            command=OBD2Command(OBD2Mode.CURRENT_DATA, 0x00, "Unknown", 0),
            raw_data=raw_data,
            processed_data=list(raw_data),
            timestamp=time.time(),
            success=True
        )
    
    def get_supported_pids(self, base_pid: int = 0x00) -> List[int]:
        """Get list of supported PIDs."""
        return self._supported_pids.get(base_pid, [])
    
    def is_pid_supported(self, pid: int) -> bool:
        """Check if a specific PID is supported."""
        base_pid = (pid // 32) * 32
        return pid in self._supported_pids.get(base_pid, [])
    
    async def read_dtc_codes(self) -> List[str]:
        """Read diagnostic trouble codes."""
        try:
            stored_codes_cmd = OBD2Command(
                OBD2Mode.STORED_CODES, 0x00, "Stored DTCs", 0
            )
            response = await self.send_command(stored_codes_cmd)
            
            if response.success and response.processed_data:
                return self._parse_dtc_codes(response.processed_data)
            else:
                return []
                
        except Exception as e:
            self.logger.error(f"DTC reading failed: {e}")
            return []
    
    def _parse_dtc_codes(self, data_bytes: List[int]) -> List[str]:
        """Parse DTC codes from response data."""
        codes = []
        
        # DTCs are typically 2 bytes each
        for i in range(0, len(data_bytes), 2):
            if i + 1 < len(data_bytes):
                code_bytes = (data_bytes[i] << 8) | data_bytes[i + 1]
                if code_bytes != 0:  # 0x0000 means no code
                    dtc = self._format_dtc_code(code_bytes)
                    codes.append(dtc)
        
        return codes
    
    def _format_dtc_code(self, code_value: int) -> str:
        """Format DTC code value to standard format (e.g., P0301)."""
        # First digit determines code type
        first_digit = (code_value >> 14) & 0x03
        type_map = {0: 'P', 1: 'C', 2: 'B', 3: 'U'}
        code_type = type_map.get(first_digit, 'P')
        
        # Remaining digits
        remaining = code_value & 0x3FFF
        return f"{code_type}{remaining:04X}"
    
    async def clear_dtc_codes(self) -> bool:
        """Clear diagnostic trouble codes."""
        try:
            clear_cmd = OBD2Command(
                OBD2Mode.CLEAR_CODES, 0x00, "Clear DTCs", 0
            )
            response = await self.send_command(clear_cmd)
            return response.success
            
        except Exception as e:
            self.logger.error(f"DTC clearing failed: {e}")
            return False