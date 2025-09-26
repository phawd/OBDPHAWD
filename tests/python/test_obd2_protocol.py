"""Tests for OBD2 protocol implementation."""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
import sys
from pathlib import Path

# Add source to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "python"))

from obdphawd.protocols.obd2 import OBD2Protocol, OBD2Mode, OBD2Command
from obdphawd.core.exceptions import ProtocolError


class TestOBD2Protocol:
    """Test cases for OBD2Protocol class."""
    
    @pytest.fixture
    def mock_connection_manager(self):
        """Create a mock connection manager."""
        manager = Mock()
        manager.send_data = AsyncMock()
        return manager
    
    @pytest.fixture
    def obd2_protocol(self, mock_connection_manager):
        """Create an OBD2Protocol instance with mock connection manager."""
        return OBD2Protocol(mock_connection_manager, "test_connection")
    
    def test_command_formatting(self, obd2_protocol):
        """Test OBD2 command formatting."""
        command = OBD2Command(OBD2Mode.CURRENT_DATA, 0x0C, "Engine RPM", 2)
        
        # Test ELM327 format
        formatted = obd2_protocol._format_command(command)
        expected = b"01 0C\r"
        assert formatted == expected
    
    def test_formula_application(self, obd2_protocol):
        """Test formula application for data conversion."""
        # Test RPM calculation: ((A*256)+B)/4
        data_bytes = [0x1A, 0x2B]  # Example data
        formula = "((A*256)+B)/4"
        
        result = obd2_protocol._apply_formula(formula, data_bytes)
        expected = ((0x1A * 256) + 0x2B) / 4
        assert result == expected
    
    def test_dtc_code_formatting(self, obd2_protocol):
        """Test DTC code formatting."""
        # Test P-code (Powertrain)
        p_code = obd2_protocol._format_dtc_code(0x0301)  # P0301
        assert p_code == "P0301"
        
        # Test C-code (Chassis)
        c_code = obd2_protocol._format_dtc_code(0x4000)  # C0000
        assert c_code == "C0000"
    
    @pytest.mark.asyncio
    async def test_successful_command_execution(self, obd2_protocol, mock_connection_manager):
        """Test successful OBD2 command execution."""
        # Mock successful response for RPM command
        mock_response = b"41 0C 1A 2B>"
        mock_connection_manager.send_data.return_value = mock_response
        
        command = obd2_protocol.COMMON_PIDS[0x0C]  # Engine RPM
        response = await obd2_protocol.send_command(command)
        
        assert response.success is True
        assert response.command == command
        assert response.raw_data == mock_response
        assert isinstance(response.processed_data, (int, float))
    
    @pytest.mark.asyncio
    async def test_failed_command_execution(self, obd2_protocol, mock_connection_manager):
        """Test failed OBD2 command execution."""
        # Mock error response
        mock_response = b"NO DATA>"
        mock_connection_manager.send_data.return_value = mock_response
        
        command = obd2_protocol.COMMON_PIDS[0x0C]  # Engine RPM
        response = await obd2_protocol.send_command(command)
        
        assert response.success is False
        assert response.error_message is not None
    
    def test_response_parsing_valid(self, obd2_protocol):
        """Test parsing of valid OBD2 response."""
        command = OBD2Command(OBD2Mode.CURRENT_DATA, 0x0C, "Engine RPM", 2, "((A*256)+B)/4")
        raw_data = b"41 0C 1A 2B>"
        
        result = obd2_protocol._parse_obd2_response(command, raw_data)
        expected = ((0x1A * 256) + 0x2B) / 4
        assert result == expected
    
    def test_response_parsing_invalid(self, obd2_protocol):
        """Test parsing of invalid OBD2 response."""
        command = OBD2Command(OBD2Mode.CURRENT_DATA, 0x0C, "Engine RPM", 2)
        raw_data = b"ERROR>"
        
        with pytest.raises(ProtocolError):
            obd2_protocol._parse_obd2_response(command, raw_data)
    
    def test_pid_support_parsing(self, obd2_protocol):
        """Test parsing of PID support bitmap."""
        # Test data representing supported PIDs
        data_bytes = [0xBE, 0x1F, 0xB8, 0x10]  # Example bitmap
        supported = obd2_protocol._parse_pid_support(data_bytes, 0x00)
        
        # Check that some expected PIDs are in the list
        assert len(supported) > 0
        assert all(isinstance(pid, int) for pid in supported)
        assert all(0 < pid <= 32 for pid in supported)
    
    @pytest.mark.asyncio
    async def test_initialization_success(self, obd2_protocol, mock_connection_manager):
        """Test successful OBD2 protocol initialization."""
        # Mock successful responses for initialization
        mock_connection_manager.send_data.side_effect = [
            b"OK>",      # ATZ response
            b"OK>",      # ATE0 response
            b"OK>",      # ATL0 response
            b"OK>",      # ATS0 response
            b"OK>",      # ATH1 response
            b"OK>",      # ATSP0 response
            b"41 01 00 00 00 00>"  # Monitor status response
        ]
        
        result = await obd2_protocol.initialize()
        assert result is True
        assert obd2_protocol._protocol_detected is True
    
    @pytest.mark.asyncio
    async def test_initialization_failure(self, obd2_protocol, mock_connection_manager):
        """Test failed OBD2 protocol initialization."""
        # Mock failed response
        mock_connection_manager.send_data.side_effect = Exception("Connection failed")
        
        result = await obd2_protocol.initialize()
        assert result is False
        assert obd2_protocol._protocol_detected is False


if __name__ == "__main__":
    pytest.main([__file__])