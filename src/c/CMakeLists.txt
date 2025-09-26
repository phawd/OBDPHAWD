cmake_minimum_required(VERSION 3.12)
project(obdphawd-c VERSION 0.1.0 LANGUAGES C)

# Set C standard
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)

# Build options
option(BUILD_SHARED_LIBS "Build shared libraries" ON)
option(BUILD_EXAMPLES "Build examples" ON)
option(BUILD_TESTS "Build tests" ON)

# Include directories
include_directories(include)

# Find required libraries
find_package(PkgConfig REQUIRED)

# Check for BlueZ (Linux Bluetooth stack)
if(UNIX AND NOT APPLE)
    pkg_check_modules(BLUEZ bluez)
    if(BLUEZ_FOUND)
        add_definitions(-DHAVE_BLUEZ)
        include_directories(${BLUEZ_INCLUDE_DIRS})
        link_directories(${BLUEZ_LIBRARY_DIRS})
    endif()
endif()

# Source files
set(SOURCES
    src/obdphawd.c
    src/connection.c
    src/bluetooth_le.c
    src/obd2_protocol.c
    src/utils.c
)

set(HEADERS
    include/obdphawd.h
    include/connection.h
    include/bluetooth_le.h
    include/obd2_protocol.h
    include/utils.h
)

# Create library
add_library(obdphawd ${SOURCES} ${HEADERS})

# Set library properties
set_target_properties(obdphawd PROPERTIES
    VERSION ${PROJECT_VERSION}
    SOVERSION 0
    PUBLIC_HEADER "${HEADERS}"
)

# Link libraries
if(BLUEZ_FOUND)
    target_link_libraries(obdphawd ${BLUEZ_LIBRARIES})
endif()

target_link_libraries(obdphawd pthread)

# Install library
install(TARGETS obdphawd
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    PUBLIC_HEADER DESTINATION include/obdphawd
)

# Build examples
if(BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()

# Build tests
if(BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()

# Package configuration
configure_file(obdphawd.pc.in obdphawd.pc @ONLY)
install(FILES ${CMAKE_BINARY_DIR}/obdphawd.pc DESTINATION lib/pkgconfig)