"""Data conversion utilities for automotive protocols."""

from typing import List, Union, Any
import struct


class DataConverter:
    """Utility class for converting automotive data formats."""
    
    @staticmethod
    def bytes_to_hex_string(data: bytes, separator: str = " ") -> str:
        """Convert bytes to hex string representation."""
        return separator.join(f"{b:02X}" for b in data)
    
    @staticmethod
    def hex_string_to_bytes(hex_str: str, separator: str = " ") -> bytes:
        """Convert hex string to bytes."""
        hex_values = hex_str.replace(separator, "").replace(" ", "")
        return bytes(int(hex_values[i:i+2], 16) for i in range(0, len(hex_values), 2))
    
    @staticmethod
    def int_to_bytes(value: int, byte_count: int, endianness: str = 'big') -> bytes:
        """Convert integer to bytes with specified byte count and endianness."""
        return value.to_bytes(byte_count, endianness)
    
    @staticmethod
    def bytes_to_int(data: bytes, endianness: str = 'big') -> int:
        """Convert bytes to integer."""
        return int.from_bytes(data, endianness)
    
    @staticmethod
    def calculate_checksum(data: bytes, algorithm: str = 'simple') -> int:
        """Calculate checksum for data."""
        if algorithm == 'simple':
            return sum(data) & 0xFF
        elif algorithm == 'xor':
            checksum = 0
            for byte in data:
                checksum ^= byte
            return checksum
        elif algorithm == 'two_complement':
            return (256 - (sum(data) & 0xFF)) & 0xFF
        else:
            raise ValueError(f"Unknown checksum algorithm: {algorithm}")
    
    @staticmethod
    def verify_checksum(data: bytes, expected: int, algorithm: str = 'simple') -> bool:
        """Verify data checksum."""
        calculated = DataConverter.calculate_checksum(data, algorithm)
        return calculated == expected
    
    @staticmethod
    def celsius_to_fahrenheit(celsius: float) -> float:
        """Convert Celsius to Fahrenheit."""
        return (celsius * 9/5) + 32
    
    @staticmethod
    def fahrenheit_to_celsius(fahrenheit: float) -> float:
        """Convert Fahrenheit to Celsius."""
        return (fahrenheit - 32) * 5/9
    
    @staticmethod
    def kph_to_mph(kph: float) -> float:
        """Convert kilometers per hour to miles per hour."""
        return kph * 0.621371
    
    @staticmethod
    def mph_to_kph(mph: float) -> float:
        """Convert miles per hour to kilometers per hour."""
        return mph * 1.60934
    
    @staticmethod
    def kpa_to_psi(kpa: float) -> float:
        """Convert kilopascals to pounds per square inch."""
        return kpa * 0.145038
    
    @staticmethod
    def psi_to_kpa(psi: float) -> float:
        """Convert pounds per square inch to kilopascals."""
        return psi * 6.89476
    
    @staticmethod
    def parse_vin(vin_bytes: bytes) -> str:
        """Parse Vehicle Identification Number from bytes."""
        if len(vin_bytes) >= 17:
            return vin_bytes[:17].decode('ascii', errors='ignore')
        return ""
    
    @staticmethod
    def format_dtc_code(code_bytes: bytes) -> str:
        """Format diagnostic trouble code from bytes."""
        if len(code_bytes) >= 2:
            code_value = struct.unpack('>H', code_bytes[:2])[0]
            
            # Determine code type from first two bits
            code_type_map = {0: 'P', 1: 'C', 2: 'B', 3: 'U'}
            code_type = code_type_map.get((code_value >> 14) & 0x03, 'P')
            
            # Format the code
            code_number = code_value & 0x3FFF
            return f"{code_type}{code_number:04X}"
        
        return "INVALID"
    
    @staticmethod
    def calculate_fuel_efficiency(distance_km: float, fuel_liters: float) -> dict:
        """Calculate fuel efficiency in various units."""
        if fuel_liters <= 0:
            return {"error": "Invalid fuel amount"}
        
        km_per_liter = distance_km / fuel_liters
        liters_per_100km = (fuel_liters / distance_km) * 100
        
        # Convert to imperial units
        distance_miles = DataConverter.kph_to_mph(distance_km)
        fuel_gallons = fuel_liters * 0.264172  # Liters to US gallons
        
        mpg = distance_miles / fuel_gallons if fuel_gallons > 0 else 0
        
        return {
            "km_per_liter": round(km_per_liter, 2),
            "liters_per_100km": round(liters_per_100km, 2),
            "miles_per_gallon": round(mpg, 2)
        }
    
    @staticmethod
    def decode_multiframe_response(frames: List[bytes]) -> bytes:
        """Decode multi-frame response (e.g., for long VIN responses)."""
        if not frames:
            return b""
        
        # Combine all frame data (skip frame headers if present)
        combined_data = b""
        for frame in frames:
            # Typically first byte might be frame counter/header
            # This is a simplified implementation
            combined_data += frame[1:] if len(frame) > 1 else frame
        
        return combined_data
    
    @staticmethod
    def validate_obd2_response(command_mode: int, command_pid: int, 
                              response_data: bytes) -> bool:
        """Validate OBD2 response matches the command."""
        if len(response_data) < 2:
            return False
        
        response_mode = response_data[0]
        response_pid = response_data[1]
        
        # Response mode should be command mode + 0x40
        expected_mode = command_mode + 0x40
        
        return response_mode == expected_mode and response_pid == command_pid