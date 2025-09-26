package com.phawd.obdphawd.core;

import com.phawd.obdphawd.core.exceptions.ConnectionException;
import com.phawd.obdphawd.core.exceptions.TimeoutException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;
import java.util.Map;

/**
 * Connection manager for handling multiple connection types in Java.
 * Provides cross-platform compatibility for automotive communication.
 */
public class ConnectionManager {
    private static final Logger logger = LoggerFactory.getLogger(ConnectionManager.class);
    
    private final Map<String, Connection> activeConnections = new ConcurrentHashMap<>();
    
    /**
     * Supported connection types
     */
    public enum ConnectionType {
        BLUETOOTH_LE,
        BLUETOOTH_CLASSIC,
        USB,
        SERIAL,
        WIFI
    }
    
    /**
     * Establish a connection to an automotive adapter.
     * 
     * @param connectionType Type of connection to establish
     * @param address Address/identifier of the target device
     * @param config Additional connection parameters
     * @return Connection ID for managing the connection
     * @throws ConnectionException If connection fails
     */
    public CompletableFuture<String> connect(ConnectionType connectionType, String address, 
                                           Map<String, Object> config) throws ConnectionException {
        return CompletableFuture.supplyAsync(() -> {
            try {
                String connectionId = connectionType.name().toLowerCase() + "_" + address;
                
                Connection connection = createConnection(connectionType, address, config);
                connection.connect();
                
                activeConnections.put(connectionId, connection);
                logger.info("Connected to {} via {}", address, connectionType);
                
                return connectionId;
            } catch (Exception e) {
                logger.error("Failed to connect to {}: {}", address, e.getMessage());
                throw new ConnectionException("Connection failed: " + e.getMessage(), e);
            }
        });
    }
    
    /**
     * Disconnect from a device.
     * 
     * @param connectionId Connection ID to disconnect
     * @return CompletableFuture that completes when disconnection is done
     */
    public CompletableFuture<Void> disconnect(String connectionId) {
        return CompletableFuture.runAsync(() -> {
            Connection connection = activeConnections.remove(connectionId);
            if (connection != null) {
                try {
                    connection.disconnect();
                    logger.info("Disconnected {}", connectionId);
                } catch (Exception e) {
                    logger.error("Error disconnecting {}: {}", connectionId, e.getMessage());
                }
            }
        });
    }
    
    /**
     * Send data and receive response.
     * 
     * @param connectionId Connection ID
     * @param data Data to send
     * @param timeoutMs Timeout in milliseconds
     * @return Response data
     * @throws ConnectionException If connection is not active
     * @throws TimeoutException If operation times out
     */
    public CompletableFuture<byte[]> sendData(String connectionId, byte[] data, 
                                            long timeoutMs) throws ConnectionException {
        Connection connection = activeConnections.get(connectionId);
        if (connection == null) {
            throw new ConnectionException("No active connection: " + connectionId);
        }
        
        return CompletableFuture.supplyAsync(() -> {
            try {
                return connection.sendReceive(data);
            } catch (Exception e) {
                throw new RuntimeException("Data transmission failed: " + e.getMessage(), e);
            }
        }).orTimeout(timeoutMs, TimeUnit.MILLISECONDS)
          .exceptionally(throwable -> {
              if (throwable.getCause() instanceof java.util.concurrent.TimeoutException) {
                  throw new TimeoutException("Data transmission timeout for " + connectionId);
              }
              throw new RuntimeException(throwable);
          });
    }
    
    /**
     * List all active connections.
     * 
     * @return Map of connection ID to connection type
     */
    public Map<String, String> listConnections() {
        Map<String, String> connections = new ConcurrentHashMap<>();
        activeConnections.forEach((id, conn) -> {
            connections.put(id, conn.getClass().getSimpleName());
        });
        return connections;
    }
    
    /**
     * Close all active connections.
     */
    public CompletableFuture<Void> closeAll() {
        return CompletableFuture.runAsync(() -> {
            activeConnections.keySet().forEach(connectionId -> {
                try {
                    disconnect(connectionId).get();
                } catch (Exception e) {
                    logger.error("Error closing connection {}: {}", connectionId, e.getMessage());
                }
            });
        });
    }
    
    private Connection createConnection(ConnectionType type, String address, 
                                     Map<String, Object> config) throws ConnectionException {
        switch (type) {
            case BLUETOOTH_LE:
                // return new BLEConnection(address, config);
                throw new ConnectionException("Bluetooth LE not yet implemented");
            case BLUETOOTH_CLASSIC:
                throw new ConnectionException("Bluetooth Classic not yet implemented");
            case USB:
                return new USBConnection(address, config);
            case SERIAL:
                return new SerialConnection(address, config);
            case WIFI:
                throw new ConnectionException("WiFi connection not yet implemented");
            default:
                throw new ConnectionException("Unsupported connection type: " + type);
        }
    }
    
    /**
     * Base interface for all connection types
     */
    public interface Connection {
        void connect() throws Exception;
        void disconnect() throws Exception;
        byte[] sendReceive(byte[] data) throws Exception;
        boolean isConnected();
    }
}