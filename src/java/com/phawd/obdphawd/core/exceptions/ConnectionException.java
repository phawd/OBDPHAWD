package com.phawd.obdphawd.core.exceptions;

/**
 * Exception thrown when connection to vehicle or adapter fails.
 */
public class ConnectionException extends OBDPHAWDException {
    
    public ConnectionException(String message) {
        super(message);
    }
    
    public ConnectionException(String message, Throwable cause) {
        super(message, cause);
    }
    
    public ConnectionException(Throwable cause) {
        super(cause);
    }
}