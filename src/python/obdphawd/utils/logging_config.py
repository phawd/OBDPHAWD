"""Logging configuration for OBDPHAWD."""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional


def setup_logging(level: str = "INFO", 
                 log_file: Optional[str] = None,
                 log_to_console: bool = True,
                 max_bytes: int = 10 * 1024 * 1024,  # 10MB
                 backup_count: int = 5) -> None:
    """
    Set up logging configuration for OBDPHAWD.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (optional)
        log_to_console: Whether to log to console
        max_bytes: Maximum log file size before rotation
        backup_count: Number of backup log files to keep
    """
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, level.upper()))
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    
    # File handler with rotation
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setLevel(getattr(logging, level.upper()))
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Set specific logger levels
    logging.getLogger('bleak').setLevel(logging.WARNING)  # Reduce BLE noise
    logging.getLogger('asyncio').setLevel(logging.WARNING)
    
    # Create application-specific logger
    app_logger = logging.getLogger('obdphawd')
    app_logger.info(f"Logging initialized at {level} level")


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name."""
    return logging.getLogger(f'obdphawd.{name}')


class ProtocolLogger:
    """Specialized logger for protocol communication."""
    
    def __init__(self, protocol_name: str):
        self.logger = get_logger(f'protocol.{protocol_name}')
        self._log_raw_data = False
    
    def enable_raw_data_logging(self, enabled: bool = True) -> None:
        """Enable/disable raw data logging."""
        self._log_raw_data = enabled
    
    def log_command(self, command: str, data: bytes) -> None:
        """Log outgoing command."""
        if self._log_raw_data:
            self.logger.debug(f"TX: {command} | {data.hex()}")
        else:
            self.logger.debug(f"TX: {command}")
    
    def log_response(self, response: str, data: bytes) -> None:
        """Log incoming response."""
        if self._log_raw_data:
            self.logger.debug(f"RX: {response} | {data.hex()}")
        else:
            self.logger.debug(f"RX: {response}")
    
    def log_error(self, error: str, data: Optional[bytes] = None) -> None:
        """Log protocol error."""
        if data and self._log_raw_data:
            self.logger.error(f"ERROR: {error} | {data.hex()}")
        else:
            self.logger.error(f"ERROR: {error}")
    
    def log_connection_event(self, event: str, details: str = "") -> None:
        """Log connection events."""
        if details:
            self.logger.info(f"CONNECTION: {event} - {details}")
        else:
            self.logger.info(f"CONNECTION: {event}")