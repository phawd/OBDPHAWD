/**
 * @file obdphawd.h
 * @brief Main header file for OBDPHAWD C library
 * @author PHAWD Team
 * @version 0.1.0
 * 
 * OBD2 and Automotive Protocol Handler with Bluetooth Low Energy Support
 * C library for low-level automotive communication and protocol handling.
 */

#ifndef OBDPHAWD_H
#define OBDPHAWD_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

/* Version information */
#define OBDPHAWD_VERSION_MAJOR 0
#define OBDPHAWD_VERSION_MINOR 1
#define OBDPHAWD_VERSION_PATCH 0
#define OBDPHAWD_VERSION_STRING "0.1.0"

/* Error codes */
typedef enum {
    OBDPHAWD_SUCCESS = 0,
    OBDPHAWD_ERROR_INVALID_PARAM = -1,
    OBDPHAWD_ERROR_MEMORY = -2,
    OBDPHAWD_ERROR_CONNECTION = -3,
    OBDPHAWD_ERROR_TIMEOUT = -4,
    OBDPHAWD_ERROR_PROTOCOL = -5,
    OBDPHAWD_ERROR_NOT_IMPLEMENTED = -6,
    OBDPHAWD_ERROR_BLUETOOTH = -7
} obdphawd_error_t;

/* Connection types */
typedef enum {
    OBDPHAWD_CONN_BLUETOOTH_LE,
    OBDPHAWD_CONN_BLUETOOTH_CLASSIC,
    OBDPHAWD_CONN_USB,
    OBDPHAWD_CONN_SERIAL,
    OBDPHAWD_CONN_WIFI
} obdphawd_connection_type_t;

/* Forward declarations */
typedef struct obdphawd_context obdphawd_context_t;
typedef struct obdphawd_connection obdphawd_connection_t;

/**
 * @brief Initialize OBDPHAWD library
 * @return Context pointer on success, NULL on failure
 */
obdphawd_context_t* obdphawd_init(void);

/**
 * @brief Cleanup OBDPHAWD library
 * @param ctx Context to cleanup
 */
void obdphawd_cleanup(obdphawd_context_t* ctx);

/**
 * @brief Get library version string
 * @return Version string
 */
const char* obdphawd_version(void);

/**
 * @brief Get error string for error code
 * @param error Error code
 * @return Error description string
 */
const char* obdphawd_error_string(obdphawd_error_t error);

/**
 * @brief Set log level for debugging
 * @param level Log level (0=NONE, 1=ERROR, 2=WARN, 3=INFO, 4=DEBUG)
 */
void obdphawd_set_log_level(int level);

/* Include sub-modules */
#include "connection.h"
#include "bluetooth_le.h"
#include "obd2_protocol.h"
#include "utils.h"

#ifdef __cplusplus
}
#endif

#endif /* OBDPHAWD_H */