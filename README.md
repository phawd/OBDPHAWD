# OBDPHAWD

**OBD2 and Automotive Protocol Handler with Bluetooth Low Energy Support**

A comprehensive multi-language library for automotive diagnostics and communication protocols including OBD2, proprietary protocols, and Bluetooth Low Energy (BLE). Designed for cross-platform compatibility and low-level hardware integration.

## 🚗 Features

- **Multi-Language Support**: Python, Java, and C/C++ implementations
- **Bluetooth Low Energy (BLE)**: Native support for BLE automotive adapters
- **OBD2 Protocol**: Full OBD2/OBDII protocol implementation with ELM327 support
- **Extensible Architecture**: Easy to add proprietary automotive protocols
- **Cross-Platform**: Works on Linux, Windows, macOS, and embedded systems
- **Asynchronous Operations**: Non-blocking communication for real-time applications
- **Device Discovery**: Automatic scanning and discovery of automotive BLE devices
- **Diagnostic Tools**: Built-in support for reading DTCs, PIDs, and vehicle parameters

## 📁 Project Structure

```
OBDPHAWD/
├── src/
│   ├── python/          # Python implementation
│   │   ├── obdphawd/    # Main Python package
│   │   │   ├── core/    # Core connection management
│   │   │   ├── protocols/   # Protocol implementations (OBD2, etc.)
│   │   │   ├── bluetooth/   # BLE communication layer
│   │   │   └── utils/   # Utility functions
│   │   ├── setup.py     # Python package setup
│   │   └── requirements.txt
│   ├── java/            # Java implementation
│   │   ├── com/phawd/obdphawd/  # Java packages
│   │   └── pom.xml      # Maven build configuration
│   └── c/               # C/C++ implementation
│       ├── include/     # Header files
│       ├── src/         # Source files
│       └── CMakeLists.txt   # CMake build configuration
├── examples/            # Example code and demos
├── tests/               # Unit tests for all languages
├── docs/                # Documentation
└── build/               # Build artifacts
```

## 🚀 Quick Start

### Python Installation

```bash
# Clone the repository
git clone https://github.com/phawd/OBDPHAWD.git
cd OBDPHAWD

# Install Python dependencies
pip install -r src/python/requirements.txt

# Install the Python package in development mode
cd src/python
pip install -e .
```

### Basic Python Usage

```python
import asyncio
from obdphawd import ConnectionManager, OBD2Protocol
from obdphawd.bluetooth import DeviceScanner
from obdphawd.core import ConnectionType

async def main():
    # Scan for automotive BLE devices
    scanner = DeviceScanner()
    devices = await scanner.scan(timeout=10.0, automotive_only=True)
    
    if devices:
        # Connect to the first device found
        conn_manager = ConnectionManager()
        connection_id = await conn_manager.connect(
            ConnectionType.BLUETOOTH_LE,
            devices[0].address
        )
        
        # Initialize OBD2 protocol
        obd2 = OBD2Protocol(conn_manager, connection_id)
        if await obd2.initialize():
            # Read engine RPM
            response = await obd2.send_command(obd2.COMMON_PIDS[0x0C])
            if response.success:
                print(f"Engine RPM: {response.processed_data}")
        
        # Disconnect
        await conn_manager.disconnect(connection_id)

asyncio.run(main())
```

### Java Build and Usage

```bash
# Build Java components
cd src/java
mvn clean compile package

# Run Java example
java -cp target/obdphawd-java-0.1.0.jar com.phawd.obdphawd.examples.BasicExample
```

### C/C++ Build and Usage

```bash
# Build C components
cd src/c
mkdir build && cd build
cmake ..
make

# Run C example
./examples/basic_example
```

## 📋 Dependencies

### Python Dependencies
- `bleak>=0.20.0` - Bluetooth Low Energy communication
- `asyncio-mqtt>=0.11.0` - MQTT support (optional)
- `pyserial>=3.5` - Serial port communication
- `crcmod>=1.7` - CRC calculations

### Java Dependencies
- Java 11 or higher
- Maven 3.6 or higher
- `jSerialComm` - Serial communication
- `usb4java` - USB communication

### C/C++ Dependencies
- CMake 3.12 or higher
- GCC 7.0 or higher / Clang 6.0 or higher
- BlueZ (Linux) - Bluetooth stack
- pthread - Threading support

## 🔧 Supported Protocols

### OBD2/OBDII
- **Mode 01**: Current Data
- **Mode 02**: Freeze Frame Data
- **Mode 03**: Stored Diagnostic Trouble Codes
- **Mode 04**: Clear Diagnostic Trouble Codes
- **Mode 05**: Oxygen Sensor Test Results
- **Mode 06**: Monitor Test Results
- **Mode 07**: Pending Diagnostic Trouble Codes
- **Mode 08**: Control Operation
- **Mode 09**: Vehicle Information
- **Mode 0A**: Permanent Diagnostic Trouble Codes

### Supported PIDs
- Engine RPM (0x0C)
- Vehicle Speed (0x0D)
- Engine Coolant Temperature (0x05)
- Throttle Position (0x11)
- MAF Air Flow Rate (0x10)
- Fuel System Status (0x03)
- And many more...

## 📱 Supported Devices

### Bluetooth Low Energy (BLE) Adapters
- ELM327 BLE adapters
- VLink automotive scanners
- OBDLink BLE adapters
- Generic BLE OBD2 dongles

### Connection Types
- **Bluetooth Low Energy (BLE)** - Primary focus
- **Bluetooth Classic** - Planned
- **USB** - Planned
- **Serial/UART** - Planned
- **WiFi** - Planned

## 🧪 Testing

### Python Tests
```bash
cd tests/python
pytest test_obd2_protocol.py -v
```

### Java Tests
```bash
cd src/java
mvn test
```

### C Tests
```bash
cd src/c/build
make test
ctest
```

## 📚 Examples

- `examples/python_basic_scan.py` - Basic BLE scanning and OBD2 communication
- `examples/java_connection_demo.java` - Java connection management demo
- `examples/c_ble_example.c` - C BLE communication example

## 🛠️ Development

### Setting up Development Environment

```bash
# Python development
pip install -r src/python/requirements.txt
pip install -e src/python/[dev]

# Java development
cd src/java
mvn clean install

# C development
cd src/c
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Debug ..
make
```

### Code Style
- **Python**: Black formatter, isort for imports
- **Java**: Google Java Style Guide
- **C/C++**: Linux Kernel style with 4-space indentation

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

- Create an issue on GitHub for bug reports
- Discussion and questions: GitHub Discussions
- Email: support@phawd.com

## 🗺️ Roadmap

- [ ] ✅ Basic OBD2 protocol support
- [ ] ✅ Bluetooth Low Energy communication
- [ ] ✅ Multi-language architecture (Python, Java, C)
- [ ] 🔄 Bluetooth Classic support
- [ ] 🔄 USB connection support
- [ ] 🔄 Serial connection support
- [ ] 🔄 Proprietary protocol frameworks
- [ ] 🔄 Real-time data streaming
- [ ] 🔄 GUI applications
- [ ] 🔄 Mobile app integration
- [ ] 🔄 Cloud connectivity

## 🏷️ Version History

- **v0.1.0** - Initial release with basic BLE and OBD2 support

---

**Made with ❤️ for the automotive community**
=======
OBDPHAWD is a C#/.NET project focused on OBD (On-Board Diagnostics) functionality for automotive applications.

## GitHub Copilot Integration

This repository is configured with GitHub Copilot coding agent instructions to provide context-aware assistance for OBD-related development. The Copilot configuration includes:

- **Development Guidelines**: C#/.NET best practices and OBD-specific patterns
- **Technical Knowledge**: OBD protocols, PIDs, and automotive diagnostic standards  
- **Code Standards**: Consistent formatting, error handling, and testing approaches
- **Project Context**: Automotive focus with real-time data processing considerations

### Copilot Configuration Files

- `.github/copilot-instructions.md` - Development guidelines and coding standards
- `.github/copilot-knowledge.md` - Technical knowledge base for OBD development
- `.github/copilot-workspace.yml` - Project metadata and configuration
- `.github/workflows/copilot-validation.yml` - Automated validation of Copilot config

## Project Structure

The solution is organized as follows:

- **`src/OBDPHAWD.Core/`** - Core library containing OBD functionality
  - `ObdDiagnostics.cs` - Main diagnostics class
  - `IObdCommunication.cs` - Interface for OBD communication
  - `ObdCommand.cs` - Base class for OBD commands
  - `ObdCommands.cs` - Standard OBD-II command definitions
- **`src/OBDPHAWD.Console/`** - Console application demonstrating the library
- **`tests/OBDPHAWD.Core.Tests/`** - Unit tests for the core library

## Getting Started

### Prerequisites
- .NET 8.0 SDK or later

### Building the Solution
```bash
dotnet build
```

### Running Tests
```bash
dotnet test
```

### Running the Console Application
```bash
dotnet run --project src/OBDPHAWD.Console
```

### Development Guidelines
This project follows the coding standards and patterns defined in `.github/copilot-instructions.md`, including:
- Async/await patterns for I/O operations
- Proper error handling and resource disposal
- Unit tests following Arrange-Act-Assert pattern
- XML documentation for public APIs

## L
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
