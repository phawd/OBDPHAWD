# OBDPHAWD - Copilot Instructions

## Repository Summary

**OBDPHAWD** appears to be an OBD (On-Board Diagnostics) related project in its early development stage. Based on the repository structure and .gitignore file, this is intended to be a .NET/C# project using Visual Studio as the primary development environment.

### Current State
- **Programming Language**: Intended for C#/.NET (based on .gitignore)
- **Development Environment**: Visual Studio 
- **License**: GNU General Public License v3.0
- **Project Stage**: Early/Initial setup - no source code present yet
- **Repository Structure**: Minimal (README.md, LICENSE, .gitignore only)

### Key Details
- The repository name suggests it's related to OBD (On-Board Diagnostics) functionality
- Currently contains only foundational files
- .gitignore is configured for Visual Studio/.NET projects
- Repository is GPL v3 licensed

## Build and Validation Steps

### Prerequisites
Since this is an early-stage repository with no source code yet, specific build tools are not yet determined. Based on the .gitignore configuration, the following tools will likely be needed:

**Expected Prerequisites:**
- .NET SDK (version TBD when project develops)
- Visual Studio or Visual Studio Code
- Git for version control

**Current Validation:**
```bash
# Verify repository structure
ls -la

# Check git status
git status

# Verify license and readme
cat README.md
head -20 LICENSE
```

### Build Commands
**Note**: No build system is currently configured. When the project develops, typical .NET commands would be:

```bash
# Expected future commands (not yet applicable):
# dotnet restore    # Restore dependencies
# dotnet build      # Build the project
# dotnet test       # Run tests
# dotnet run        # Run the application
```

### Testing
No test framework is currently configured. This will need to be established as the project develops.

### Linting
No linting tools are currently configured. For .NET projects, typical tools include:
- EditorConfig for formatting
- Roslyn analyzers
- StyleCop for code style

## Project Layout

### Current Structure
```
OBDPHAWD/
├── .git/               # Git repository metadata
├── .github/            # GitHub configuration (created for this file)
│   └── copilot-instructions.md
├── .gitignore          # Visual Studio/.NET gitignore template
├── LICENSE             # GNU GPL v3.0 license
└── README.md           # Minimal project readme
```

### Expected Future Structure
Based on typical .NET project patterns:
```
OBDPHAWD/
├── src/                # Source code
│   └── OBDPHAWD/       # Main project
├── tests/              # Test projects
├── docs/               # Documentation
├── .github/            # GitHub workflows and configuration
├── OBDPHAWD.sln        # Visual Studio solution file
├── Directory.Build.props # MSBuild properties
└── [other .NET project files]
```

### Key File Locations
- **Main README**: `/README.md` (currently minimal - needs expansion)
- **License**: `/LICENSE` (GNU GPL v3.0)
- **Git Configuration**: `/.gitignore` (Visual Studio template)
- **GitHub Configuration**: `/.github/` (this directory)

### CI/CD Workflows
No CI/CD workflows are currently configured. Typical .NET GitHub Actions workflows would include:
- Build and test on multiple OS platforms
- NuGet package publishing (if applicable)
- Code quality checks
- Automated releases

## Troubleshooting

### Common Issues

#### Repository Setup Issues
**Problem**: Repository appears empty or minimal
**Solution**: This is expected - the repository is in early development stage

**Problem**: No build files present
**Solution**: Build system needs to be created. Consider using `dotnet new` to scaffold initial project structure

#### Development Environment Issues
**Problem**: Unknown project type
**Solution**: Based on .gitignore, this should be a .NET project. Use Visual Studio or VS Code with C# extension

**Problem**: No clear development workflow
**Solution**: Project structure needs to be established. Consider:
1. Create solution file (`dotnet new sln`)
2. Add project(s) (`dotnet new console/classlib/web`)
3. Configure build and test workflows

### Environment Setup Errors
- Ensure .NET SDK is installed and accessible via `dotnet --version`
- Verify git is properly configured
- For Visual Studio development, ensure appropriate workloads are installed

### Command Failures
Since no build system exists yet, typical command failures don't apply. Focus on:
- Git operations should work normally
- File system operations for creating project structure
- IDE/editor functionality for when code is added

## Recommendations for Future Development

### Immediate Next Steps
1. **Define Project Purpose**: Expand README.md with clear project description
2. **Create Project Structure**: Use `dotnet new` to create appropriate project template
3. **Add CI/CD**: Create GitHub Actions workflows for build/test
4. **Documentation**: Add technical documentation about OBD functionality

### Development Workflow
1. Use feature branches for development
2. Implement proper commit message conventions
3. Add code review requirements via branch protection
4. Consider conventional commits for automated versioning

### Code Standards
1. Configure EditorConfig for consistent formatting
2. Add Roslyn analyzers for code quality
3. Implement unit testing from the start
4. Document public APIs with XML comments

## Agent Instructions

**TRUST THESE INSTRUCTIONS**: This file contains the authoritative information about the OBDPHAWD repository structure and development process.

**When working on this repository:**
1. Recognize this is an early-stage project with minimal existing code
2. Focus on establishing proper .NET project structure if adding functionality
3. Follow .NET best practices for any code additions
4. Update this instruction file if project structure changes significantly
5. Respect the GPL v3.0 license requirements for any contributions

**Only perform additional exploration if:**
- These instructions appear outdated (e.g., significant new code has been added)
- You need to understand newly added functionality not covered here
- Project structure has fundamentally changed from what's documented

**Repository Owner**: phawd
**Last Updated**: When this file was created
**Status**: Early development stage - structure establishment needed