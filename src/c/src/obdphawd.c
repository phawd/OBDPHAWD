/**
 * @file obdphawd.c
 * @brief Main implementation file for OBDPHAWD C library
 */

#include "obdphawd.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <pthread.h>

/* Internal context structure */
struct obdphawd_context {
    int log_level;
    pthread_mutex_t mutex;
    /* Add more context fields as needed */
};

/* Global log level */
static int g_log_level = 2; /* Default to WARN */

/* Error strings */
static const char* error_strings[] = {
    "Success",
    "Invalid parameter",
    "Memory allocation failed",
    "Connection error",
    "Operation timeout",
    "Protocol error",
    "Not implemented",
    "Bluetooth error"
};

obdphawd_context_t* obdphawd_init(void) {
    obdphawd_context_t* ctx = malloc(sizeof(obdphawd_context_t));
    if (!ctx) {
        return NULL;
    }
    
    memset(ctx, 0, sizeof(obdphawd_context_t));
    ctx->log_level = g_log_level;
    
    if (pthread_mutex_init(&ctx->mutex, NULL) != 0) {
        free(ctx);
        return NULL;
    }
    
    printf("OBDPHAWD v%s initialized\n", OBDPHAWD_VERSION_STRING);
    return ctx;
}

void obdphawd_cleanup(obdphawd_context_t* ctx) {
    if (!ctx) {
        return;
    }
    
    pthread_mutex_destroy(&ctx->mutex);
    free(ctx);
    printf("OBDPHAWD cleanup completed\n");
}

const char* obdphawd_version(void) {
    return OBDPHAWD_VERSION_STRING;
}

const char* obdphawd_error_string(obdphawd_error_t error) {
    int index = -error; /* Convert negative error codes to positive indices */
    
    if (index >= 0 && index < (int)(sizeof(error_strings) / sizeof(error_strings[0]))) {
        return error_strings[index];
    }
    
    return "Unknown error";
}

void obdphawd_set_log_level(int level) {
    g_log_level = level;
}

/* Internal logging function */
void obdphawd_log(int level, const char* format, ...) {
    if (level > g_log_level) {
        return;
    }
    
    const char* level_names[] = {"", "ERROR", "WARN", "INFO", "DEBUG"};
    const char* level_name = (level >= 1 && level <= 4) ? level_names[level] : "UNKNOWN";
    
    printf("[OBDPHAWD %s] ", level_name);
    
    va_list args;
    va_start(args, format);
    vprintf(format, args);
    va_end(args);
    
    printf("\n");
}