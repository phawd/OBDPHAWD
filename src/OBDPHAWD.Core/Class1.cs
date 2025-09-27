using System;

namespace OBDPHAWD.Core;

/// <summary>
/// Core OBD diagnostic functionality
/// </summary>
public class ObdDiagnostics
{
    /// <summary>
    /// Gets diagnostic information from the OBD system
    /// </summary>
    /// <returns>A simple diagnostic message</returns>
    public string GetDiagnosticInfo()
    {
        return "OBD System Ready";
    }
}
