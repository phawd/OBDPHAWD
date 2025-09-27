using OBDPHAWD.Core;
using OBDPHAWD.Core.Commands;

namespace OBDPHAWD.Console;

/// <summary>
/// Simple console application demonstrating OBDPHAWD functionality
/// </summary>
internal class Program
{
    static void Main(string[] args)
    {
        System.Console.WriteLine("OBDPHAWD - OBD Diagnostics Console");
        System.Console.WriteLine("=====================================");
        System.Console.WriteLine();

        // Demonstrate basic diagnostics
        var diagnostics = new ObdDiagnostics();
        System.Console.WriteLine($"Status: {diagnostics.GetDiagnosticInfo()}");
        System.Console.WriteLine();

        // Display available OBD commands
        System.Console.WriteLine("Available OBD Commands:");
        System.Console.WriteLine($"- Engine RPM: {ObdCommands.EngineRpm.Pid} ({ObdCommands.EngineRpm.Description})");
        System.Console.WriteLine($"- Vehicle Speed: {ObdCommands.VehicleSpeed.Pid} ({ObdCommands.VehicleSpeed.Description})");
        System.Console.WriteLine($"- Coolant Temp: {ObdCommands.CoolantTemperature.Pid} ({ObdCommands.CoolantTemperature.Description})");
        System.Console.WriteLine($"- Throttle Position: {ObdCommands.ThrottlePosition.Pid} ({ObdCommands.ThrottlePosition.Description})");
        System.Console.WriteLine($"- Fuel Level: {ObdCommands.FuelLevel.Pid} ({ObdCommands.FuelLevel.Description})");
        System.Console.WriteLine($"- Mass Air Flow: {ObdCommands.MassAirFlow.Pid} ({ObdCommands.MassAirFlow.Description})");
        
        System.Console.WriteLine();
        System.Console.WriteLine("Ready for OBD operations...");
    }
}
