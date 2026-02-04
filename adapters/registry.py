"""
Registry of available CAN adapter types and their configuration parameters.

This dictionary defines the supported CAN adapters and their respective parameters:
- Loopback: A loopback adapter with no parameters required.
- Candlelight: A Candlelight USB-to-CAN adapter supporting multiple ports and baudrates.
- Virtual (SocketCAN): A virtual SocketCAN adapter interface.
- UDP Bridge: A UDP-based CAN bridge with configurable IP and port.

Each adapter entry contains a 'params' key with the available configuration options.
"""
ADAPTER_TYPES = {
    "Loopback": {"params": {}},
    "Candlelight": {"params": {"port": ["can0", "can1"], "baudrate": ["500000", "1000000"]}},
    "Virtual (SocketCAN)": {"params": {"interface": "vcan0"}},
    "UDP Bridge": {"params": {"ip": "127.0.0.1", "port": "5005"}}
}