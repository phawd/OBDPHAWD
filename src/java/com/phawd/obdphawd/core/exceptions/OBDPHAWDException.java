package com.phawd.obdphawd.core.exceptions;

/**
 * Base exception class for OBDPHAWD.
 */
public class OBDPHAWDException extends Exception {
    
    public OBDPHAWDException(String message) {
        super(message);
    }
    
    public OBDPHAWDException(String message, Throwable cause) {
        super(message, cause);
    }
    
    public OBDPHAWDException(Throwable cause) {
        super(cause);
    }
}