# OBDPHAWD

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

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
