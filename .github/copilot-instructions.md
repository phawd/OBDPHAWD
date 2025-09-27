# GitHub Copilot Instructions for OBDPHAWD

## Project Overview
OBDPHAWD is a C#/.NET project focused on OBD (On-Board Diagnostics) functionality. This repository follows standard .NET development practices and conventions.

## Development Guidelines

### Code Style and Standards
- Follow C# coding conventions and .NET best practices
- Use meaningful variable, method, and class names
- Maintain consistent indentation and formatting
- Add XML documentation comments for public APIs
- Follow SOLID principles and clean code practices

### Architecture Patterns
- Prefer dependency injection for loose coupling
- Use async/await patterns for I/O operations
- Implement proper error handling and logging
- Follow repository pattern for data access if applicable
- Use appropriate design patterns (Factory, Strategy, etc.) when beneficial

### Testing Guidelines
- Write unit tests for business logic
- Use descriptive test method names that explain what is being tested
- Follow Arrange-Act-Assert (AAA) pattern in tests
- Mock external dependencies in unit tests
- Aim for good test coverage on critical paths

### Security Considerations
- Never hardcode sensitive information (API keys, connection strings, etc.)
- Use configuration files or environment variables for settings
- Validate input parameters and sanitize user input
- Implement proper authentication and authorization where needed

### Performance Best Practices
- Use appropriate data structures for the task
- Avoid unnecessary allocations in hot paths
- Use StringBuilder for multiple string concatenations
- Implement proper disposal of resources (using statements)
- Consider memory usage and garbage collection impact

### Documentation Standards
- Keep README.md updated with setup and usage instructions
- Document complex algorithms and business logic
- Include code examples in documentation where helpful
- Maintain inline comments for complex code sections

## File Organization
- Follow standard .NET project structure
- Group related functionality into appropriate namespaces
- Keep configuration files in the root or dedicated config folder
- Use meaningful folder names that reflect functionality

## Dependencies and Libraries
- Prefer well-maintained, widely-used NuGet packages
- Keep dependencies up to date for security patches
- Avoid unnecessary dependencies that bloat the project
- Document any special setup requirements for dependencies

## Git Workflow
- Use descriptive commit messages
- Keep commits focused on single functionality changes
- Use branching for feature development
- Follow semantic versioning for releases

## OBD-Specific Considerations
- Handle OBD protocol variations appropriately
- Implement proper error handling for communication failures
- Consider real-time data processing requirements
- Document supported OBD standards and protocols
- Ensure thread safety for concurrent OBD operations

## Code Review Focus Areas
- Verify error handling is comprehensive
- Check for proper resource disposal
- Validate input parameter checking
- Ensure async patterns are used correctly
- Confirm unit tests cover the changes