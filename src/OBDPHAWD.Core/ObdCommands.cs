namespace OBDPHAWD.Core.Commands;

/// <summary>
/// Standard OBD-II Parameter IDs (PIDs) and commands
/// </summary>
public static class ObdCommands
{
    /// <summary>
    /// Engine RPM command
    /// </summary>
    public static readonly ObdCommand EngineRpm = new("010C", "Engine RPM", 2, "rpm");
    
    /// <summary>
    /// Vehicle speed command
    /// </summary>
    public static readonly ObdCommand VehicleSpeed = new("010D", "Vehicle Speed", 1, "km/h");
    
    /// <summary>
    /// Engine coolant temperature command
    /// </summary>
    public static readonly ObdCommand CoolantTemperature = new("0105", "Engine Coolant Temperature", 1, "°C");
    
    /// <summary>
    /// Throttle position command
    /// </summary>
    public static readonly ObdCommand ThrottlePosition = new("0111", "Throttle Position", 1, "%");
    
    /// <summary>
    /// Fuel level input command
    /// </summary>
    public static readonly ObdCommand FuelLevel = new("012F", "Fuel Tank Level Input", 1, "%");
    
    /// <summary>
    /// Mass air flow rate command
    /// </summary>
    public static readonly ObdCommand MassAirFlow = new("0110", "Mass Air Flow Rate", 2, "g/s");
}