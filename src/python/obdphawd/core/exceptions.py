"""Exception classes for OBDPHAWD."""


class OBDPHAWDException(Exception):
    """Base exception class for OBDPHAWD."""
    pass


class ConnectionError(OBDPHAWDException):
    """Raised when connection to vehicle or adapter fails."""
    pass


class ProtocolError(OBDPHAWDException):
    """Raised when protocol communication errors occur."""
    pass


class TimeoutError(OBDPHAWDException):
    """Raised when operations timeout."""
    pass


class BluetoothError(OBDPHAWDException):
    """Raised when Bluetooth operations fail."""
    pass