using System;
using System.Threading.Tasks;

namespace OBDPHAWD.Core.Interfaces;

/// <summary>
/// Interface for OBD communication handling
/// </summary>
public interface IObdCommunication : IDisposable
{
    /// <summary>
    /// Establishes connection to the OBD interface
    /// </summary>
    /// <returns>Task representing the async connection operation</returns>
    Task<bool> ConnectAsync();
    
    /// <summary>
    /// Disconnects from the OBD interface
    /// </summary>
    /// <returns>Task representing the async disconnection operation</returns>
    Task DisconnectAsync();
    
    /// <summary>
    /// Sends a command to the OBD interface
    /// </summary>
    /// <param name="command">The OBD command to send</param>
    /// <returns>Task containing the response from the OBD interface</returns>
    Task<string> SendCommandAsync(string command);
    
    /// <summary>
    /// Gets a value indicating whether the connection is active
    /// </summary>
    bool IsConnected { get; }
}