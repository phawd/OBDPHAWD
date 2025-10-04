# GitHub Copilot Instructions for OBDPHAWD

## Repository Summary
OBDPHAWD is a C#/.NET 8.0 library for OBD (On-Board Diagnostics) functionality targeting automotive applications. This is a small repository (~5.8MB, 15 C# files, 206 total files) with a clean 3-project solution structure: core library, console demo app, and unit tests using xUnit.

**Key Technologies**: .NET 8.0 SDK, C#, xUnit, MSBuild  
**Repository Structure**: Standard .NET solution with src/ and tests/ directories  
**License**: GNU General Public License v3.0

## Build, Test, and Run Instructions

### Prerequisites
- **.NET 8.0 SDK or later** (project targets net8.0)
- Environment uses .NET 9.0.305 (forward compatible)
- No additional tools required - all operations use `dotnet` CLI

### Validated Build Sequence

**IMPORTANT**: Commands should be run from the repository root directory `/home/runner/work/OBDPHAWD/OBDPHAWD`

1. **Clean** (optional, ~2 seconds):
   ```bash
   dotnet clean
   ```

2. **Restore dependencies** (~1 second when cached):
   ```bash
   dotnet restore
   ```
   Note: This step is automatically performed by build/test commands if needed.

3. **Build the solution** (~2-5 seconds for Debug, ~2 seconds for Release):
   ```bash
   dotnet build                          # Debug configuration (default)
   dotnet build --configuration Release  # Release configuration
   ```
   
4. **Run tests** (~3-5 seconds):
   ```bash
   dotnet test                    # Runs all tests with standard output
   dotnet test --verbosity quiet  # Less verbose output
   ```
   Currently 7 tests: All pass (0 failures, 0 skipped)

5. **Run console application** (~1 second):
   ```bash
   dotnet run --project src/OBDPHAWD.Console
   ```

### Complete Clean Build Sequence
For a fresh build from clean state:
```bash
dotnet clean && dotnet build && dotnet test
```
Total time: ~7-10 seconds

### Build Notes and Gotchas
- **No separate restore needed**: `dotnet build` and `dotnet test` automatically restore if needed
- **Fast incremental builds**: Subsequent builds after first take ~0.5-2 seconds
- **No build artifacts to commit**: All build outputs are in bin/obj directories (already in .gitignore)
- **No linting configured**: No separate lint step required; compilation errors are the primary validation
- **Tests use xUnit**: Test framework is xUnit 2.5.3 with Visual Studio test adapter
- **No external test dependencies**: Tests are self-contained unit tests with no external services

## Project Structure and Architecture

### Solution Layout
```
/home/runner/work/OBDPHAWD/OBDPHAWD/
├── OBDPHAWD.sln              # Main solution file (3 projects)
├── README.md                  # User documentation
├── LICENSE                    # GPL-3.0 license
├── .gitignore                # Standard VS .gitignore
├── .github/
│   ├── copilot-instructions.md      # This file
│   ├── copilot-knowledge.md         # OBD technical knowledge base
│   ├── copilot-workspace.yml        # Copilot metadata
│   ├── CODEOWNERS                   # Code ownership
│   └── workflows/
│       └── copilot-validation.yml   # CI for Copilot config files
├── src/
│   ├── OBDPHAWD.Core/              # Core library (main project)
│   │   ├── OBDPHAWD.Core.csproj    # net8.0, no external dependencies
│   │   ├── Class1.cs               # ObdDiagnostics class
│   │   ├── ObdCommand.cs           # Base command class
│   │   ├── ObdCommands.cs          # Standard OBD-II PID definitions
│   │   └── IObdCommunication.cs    # Communication interface
│   └── OBDPHAWD.Console/           # Console demo app
│       ├── OBDPHAWD.Console.csproj # net8.0, references Core
│       └── Program.cs              # Demo entry point
└── tests/
    └── OBDPHAWD.Core.Tests/        # Unit tests
        ├── OBDPHAWD.Core.Tests.csproj  # xUnit test project
        └── UnitTest1.cs            # Test classes (3 test classes, 7 tests)
```

### Key Architecture Elements

**Core Library (`OBDPHAWD.Core`)**:
- `ObdDiagnostics` - Main diagnostics class with GetDiagnosticInfo() method
- `ObdCommand` - Base class for OBD commands with PID, Description, ExpectedResponseLength, Unit properties
- `ObdCommands` - Static class containing standard OBD-II PIDs (EngineRpm, VehicleSpeed, CoolantTemperature, etc.)
- `IObdCommunication` - Interface for async OBD communication (ConnectAsync, DisconnectAsync, SendCommandAsync)
- **Namespace structure**: `OBDPHAWD.Core`, `OBDPHAWD.Core.Commands`, `OBDPHAWD.Core.Interfaces`

**Console App** - Demonstrates library usage by printing available OBD commands

**Test Project** - Contains:
- `ObdDiagnosticsTests` - Tests for main diagnostics class
- `ObdCommandTests` - Tests for command creation and validation
- `ObdCommandsTests` - Tests for standard PID definitions
- All tests follow Arrange-Act-Assert (AAA) pattern

### Project File Configuration
All projects target `net8.0` with:
- `ImplicitUsings` enabled (common namespaces auto-imported)
- `Nullable` enabled (nullable reference types)
- Test project has `IsPackable=false` and `IsTestProject=true`

### Dependencies
- **Core library**: Zero NuGet dependencies (pure .NET)
- **Console app**: Only references OBDPHAWD.Core
- **Test project**: xUnit 2.5.3, Microsoft.NET.Test.Sdk 17.8.0, coverlet.collector 6.0.0

## GitHub Actions and CI

### Copilot Configuration Validation Workflow
**File**: `.github/workflows/copilot-validation.yml`  
**Triggers**: Push or PR with changes to `.github/copilot-*.md` or `.github/copilot-*.yml`  
**Runner**: ubuntu-latest

**Steps**:
1. Checkout code
2. Validate all required Copilot files exist (copilot-instructions.md, copilot-knowledge.md, copilot-workspace.yml)
3. Validate YAML syntax of copilot-workspace.yml using Python

**No other CI workflows** - No automated build/test on push/PR currently configured

## Development Guidelines

### Code Style and Standards
- Follow C# coding conventions and .NET best practices
- Use meaningful variable, method, and class names
- Maintain consistent indentation and formatting
- **Always add XML documentation comments for public APIs** (see existing code for examples)
- Follow SOLID principles and clean code practices

### Architecture Patterns
- Prefer dependency injection for loose coupling
- **Use async/await patterns for I/O operations** (see IObdCommunication interface)
- Implement proper error handling with specific exceptions (ArgumentNullException for null params)
- Use appropriate design patterns when beneficial

### Testing Requirements
- **Write unit tests for all business logic** - test coverage is expected
- Use descriptive test method names: `MethodName_Scenario_ExpectedBehavior`
- **Always follow Arrange-Act-Assert (AAA) pattern** (see existing tests)
- Use `[Fact]` for single test cases, `[Theory]` with `[InlineData]` for parameterized tests
- Mock external dependencies in unit tests (IObdCommunication should be mocked)
- **Run tests before committing**: `dotnet test` must pass

### Security Considerations
- Never hardcode sensitive information
- Validate all input parameters (see ObdCommand constructor for null checks)
- Consider automotive security when exposing vehicle data

### Performance Best Practices
- Use appropriate data structures
- Implement proper disposal of resources (IObdCommunication implements IDisposable)
- Consider real-time data processing requirements for OBD
- Avoid unnecessary allocations in hot paths

### OBD-Specific Considerations
- Handle OBD protocol variations appropriately
- Implement proper error handling for communication failures
- Consider real-time data processing requirements
- Document supported OBD standards and PIDs (see copilot-knowledge.md)
- Ensure thread safety for concurrent OBD operations

## Validation and Confidence Checks

Before considering changes complete:

1. **Build succeeds**: `dotnet build` exits with code 0
2. **All tests pass**: `dotnet test` shows "Test summary: total: 7, failed: 0, succeeded: 7"
3. **Console app runs**: `dotnet run --project src/OBDPHAWD.Console` produces expected output
4. **No warnings**: Build produces no compiler warnings
5. **Clean repository**: `git status` shows only intended changes

## Common Issues and Troubleshooting

### Build Issues
- **Restore timeout**: First restore can take longer (~15 seconds) when NuGet cache is cold
- **Incremental build confusion**: Use `dotnet clean` before build if experiencing strange behavior
- **Missing SDK**: Ensure .NET 8.0+ SDK is installed (`dotnet --version`)

### Test Issues  
- **Tests not found**: Ensure you're running from repository root
- **Test failures**: Check that you haven't modified test assertions unintentionally

### Runtime Issues
- **Console app crashes**: Verify OBDPHAWD.Core.dll was built successfully in bin directory

## Important Notes for Coding Agents

1. **Trust these instructions first** - These have been validated. Only search for information if these instructions are incomplete or incorrect.

2. **Always work from repository root** - All commands assume working directory is `/home/runner/work/OBDPHAWD/OBDPHAWD`

3. **Build before testing changes** - Run `dotnet build` first to catch compilation errors early

4. **Small, focused changes** - This is a small, clean codebase. Keep changes minimal and surgical.

5. **Preserve existing patterns** - Follow established patterns for XML docs, error handling, and testing

6. **No configuration files to manage** - No .editorconfig, Directory.Build.props, or other special config files exist

7. **Simple dependency graph** - Console → Core ← Tests. No circular dependencies.

8. **Fast feedback loop** - Full clean build + test cycle is only ~10 seconds. Use it frequently.