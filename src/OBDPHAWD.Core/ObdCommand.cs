using System;

namespace OBDPHAWD.Core.Commands;

/// <summary>
/// Represents an OBD command with its parameters and response handling
/// </summary>
public class ObdCommand
{
    /// <summary>
    /// Gets or sets the command identifier (PID)
    /// </summary>
    public string Pid { get; set; } = string.Empty;
    
    /// <summary>
    /// Gets or sets the command description
    /// </summary>
    public string Description { get; set; } = string.Empty;
    
    /// <summary>
    /// Gets or sets the expected response length in bytes
    /// </summary>
    public int ExpectedResponseLength { get; set; }
    
    /// <summary>
    /// Gets or sets the unit of measurement for the response
    /// </summary>
    public string Unit { get; set; } = string.Empty;

    /// <summary>
    /// Initializes a new instance of the ObdCommand class
    /// </summary>
    /// <param name="pid">The command PID</param>
    /// <param name="description">The command description</param>
    /// <param name="expectedResponseLength">Expected response length</param>
    /// <param name="unit">Unit of measurement</param>
    public ObdCommand(string pid, string description, int expectedResponseLength, string unit = "")
    {
        Pid = pid ?? throw new ArgumentNullException(nameof(pid));
        Description = description ?? throw new ArgumentNullException(nameof(description));
        ExpectedResponseLength = expectedResponseLength;
        Unit = unit;
    }

    /// <summary>
    /// Returns the formatted command string to send to the OBD interface
    /// </summary>
    /// <returns>Formatted command string</returns>
    public virtual string GetCommand()
    {
        return Pid;
    }
}