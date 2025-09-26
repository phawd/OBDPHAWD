/**
 * @file bluetooth_le.h
 * @brief Bluetooth Low Energy support for automotive communication
 * @author PHAWD Team
 */

#ifndef OBDPHAWD_BLUETOOTH_LE_H
#define OBDPHAWD_BLUETOOTH_LE_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdbool.h>

/* BLE device information */
typedef struct {
    char address[18];      /* MAC address (XX:XX:XX:XX:XX:XX) */
    char name[256];        /* Device name */
    int8_t rssi;          /* Signal strength */
    bool connectable;      /* Whether device is connectable */
    uint16_t appearance;   /* Device appearance */
} obdphawd_ble_device_t;

/* BLE scan callback */
typedef void (*obdphawd_ble_scan_callback_t)(const obdphawd_ble_device_t* device, void* user_data);

/**
 * @brief Scan for BLE devices
 * @param ctx OBDPHAWD context
 * @param timeout_ms Scan timeout in milliseconds
 * @param callback Callback function for discovered devices
 * @param user_data User data passed to callback
 * @return OBDPHAWD_SUCCESS on success, error code on failure
 */
obdphawd_error_t obdphawd_ble_scan(obdphawd_context_t* ctx,
                                   uint32_t timeout_ms,
                                   obdphawd_ble_scan_callback_t callback,
                                   void* user_data);

/**
 * @brief Connect to BLE device
 * @param ctx OBDPHAWD context
 * @param address Device MAC address
 * @param connection Output connection handle
 * @return OBDPHAWD_SUCCESS on success, error code on failure
 */
obdphawd_error_t obdphawd_ble_connect(obdphawd_context_t* ctx,
                                      const char* address,
                                      obdphawd_connection_t** connection);

/**
 * @brief Disconnect from BLE device
 * @param connection Connection handle
 * @return OBDPHAWD_SUCCESS on success, error code on failure
 */
obdphawd_error_t obdphawd_ble_disconnect(obdphawd_connection_t* connection);

/**
 * @brief Send data via BLE and receive response
 * @param connection Connection handle
 * @param data Data buffer to send
 * @param data_len Length of data to send
 * @param response Buffer for response data
 * @param response_len Input: buffer size, Output: actual response length
 * @param timeout_ms Timeout in milliseconds
 * @return OBDPHAWD_SUCCESS on success, error code on failure
 */
obdphawd_error_t obdphawd_ble_send_receive(obdphawd_connection_t* connection,
                                           const uint8_t* data,
                                           size_t data_len,
                                           uint8_t* response,
                                           size_t* response_len,
                                           uint32_t timeout_ms);

/**
 * @brief Check if BLE connection is active
 * @param connection Connection handle
 * @return true if connected, false otherwise
 */
bool obdphawd_ble_is_connected(obdphawd_connection_t* connection);

#ifdef __cplusplus
}
#endif

#endif /* OBDPHAWD_BLUETOOTH_LE_H */