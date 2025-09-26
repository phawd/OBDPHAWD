package com.phawd.obdphawd.core.exceptions;

/**
 * Exception thrown when operations timeout.
 */
public class TimeoutException extends OBDPHAWDException {
    
    public TimeoutException(String message) {
        super(message);
    }
    
    public TimeoutException(String message, Throwable cause) {
        super(message, cause);
    }
    
    public TimeoutException(Throwable cause) {
        super(cause);
    }
}