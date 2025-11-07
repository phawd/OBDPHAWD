using OBDPHAWD.Core;
using OBDPHAWD.Core.Commands;

namespace OBDPHAWD.Core.Tests;

/// <summary>
/// Unit tests for OBD diagnostic functionality
/// </summary>
public class ObdDiagnosticsTests
{
    [Fact]
    public void GetDiagnosticInfo_ReturnsExpectedMessage()
    {
        // Arrange
        var diagnostics = new ObdDiagnostics();
        
        // Act
        var result = diagnostics.GetDiagnosticInfo();
        
        // Assert
        Assert.Equal("OBD System Ready", result);
    }
}

/// <summary>
/// Unit tests for OBD commands
/// </summary>
public class ObdCommandTests
{
    [Fact]
    public void ObdCommand_Constructor_SetsPropertiesCorrectly()
    {
        // Arrange & Act
        var command = new ObdCommand("010C", "Engine RPM", 2, "rpm");
        
        // Assert
        Assert.Equal("010C", command.Pid);
        Assert.Equal("Engine RPM", command.Description);
        Assert.Equal(2, command.ExpectedResponseLength);
        Assert.Equal("rpm", command.Unit);
    }
    
    [Fact]
    public void ObdCommand_GetCommand_ReturnsPid()
    {
        // Arrange
        var command = new ObdCommand("010C", "Engine RPM", 2, "rpm");
        
        // Act
        var result = command.GetCommand();
        
        // Assert
        Assert.Equal("010C", result);
    }
    
    [Theory]
    [InlineData(null, "description")]
    [InlineData("pid", null)]
    public void ObdCommand_Constructor_ThrowsArgumentNullException_WhenParametersAreNull(string pid, string description)
    {
        // Act & Assert
        Assert.Throws<ArgumentNullException>(() => new ObdCommand(pid, description, 1));
    }
}

/// <summary>
/// Unit tests for standard OBD commands
/// </summary>
public class ObdCommandsTests
{
    [Fact]
    public void EngineRpm_HasCorrectProperties()
    {
        // Arrange & Act
        var command = ObdCommands.EngineRpm;
        
        // Assert
        Assert.Equal("010C", command.Pid);
        Assert.Equal("Engine RPM", command.Description);
        Assert.Equal(2, command.ExpectedResponseLength);
        Assert.Equal("rpm", command.Unit);
    }
    
    [Fact]
    public void VehicleSpeed_HasCorrectProperties()
    {
        // Arrange & Act
        var command = ObdCommands.VehicleSpeed;
        
        // Assert
        Assert.Equal("010D", command.Pid);
        Assert.Equal("Vehicle Speed", command.Description);
        Assert.Equal(1, command.ExpectedResponseLength);
        Assert.Equal("km/h", command.Unit);
    }
}