# Nemotek Counters Library

[![PyPI version](https://badge.fury.io/py/nemotek-counters.svg)](https://badge.fury.io/py/nemotek-counters)
[![Python versions](https://img.shields.io/pypi/pyversions/nemotek-counters.svg)](https://pypi.org/project/nemotek-counters/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python library for reading data from various electrical energy counters including Carlo Gavazzi, Contrel, Diris, Lovato, RedZ, and Schneider devices.

## Features

- 🔌 **Multiple Communication Protocols**: Support for both Modbus RTU (serial) and Modbus TCP connections
- 🔄 **Automatic Fallback**: Intelligent switching between TCP and RTU when both are configured
- 📊 **Comprehensive Data Collection**: Read voltage, current, power, energy, and frequency measurements
- 🛠️ **Easy Configuration**: Simple dataclass-based configuration for counters and connections
- 📝 **Detailed Logging**: Built-in logging for debugging and monitoring
- 🐍 **Modern Python**: Written for Python 3.8+ with type hints and dataclasses
- 🔧 **Extensible Design**: Easy to add support for new counter models

## Installation

```bash
pip install nemotek-counters
```

Or for development:
```bash
pip install -e .
```

## Usage

### Import the library
```python
import nemotek_counters
from nemotek_counters import carlo_gavazzi
from nemotek_counters.carlo_gavazzi import em530
```

### Carlo Gavazzi EM530 Example

#### RTU (Serial) Connection
```python
from nemotek_counters.carlo_gavazzi.em530 import (
    CounterConfiguration, 
    ModbusRTUConfiguration, 
    EM530DataCollector
)

# Configure the counter
counter_config = CounterConfiguration(
    counter_id=167,
    unit_id=100,  # Modbus address
    counter_name="TestCounter",
    company_id="MyCompany"
)

# Configure Modbus RTU connection
rtu_config = ModbusRTUConfiguration(
    port="/dev/ttyNS0",  # Adjust according to your system
    baudrate=9600
)

# Create collector
collector = EM530DataCollector(counter_config, modbus_rtu_config=rtu_config)

# Connect and read data
if collector.connect():
    data = collector.collect_data()
    if data:
        print(f"Voltage L1: {data['voltageL1']}V")
        print(f"Current L1: {data['currentL1']}A")
        print(f"Active Power: {data['activePower']}kW")
    collector.disconnect()
```

#### TCP Connection
```python
from nemotek_counters.carlo_gavazzi.em530 import (
    CounterConfiguration, 
    ModbusTCPConfiguration, 
    EM530DataCollector
)

# Configure the counter
counter_config = CounterConfiguration(
    counter_id=167,
    unit_id=100,  # Modbus address
    counter_name="TestCounter",
    company_id="MyCompany"
)

# Configure Modbus TCP connection
tcp_config = ModbusTCPConfiguration(
    host="192.168.1.100",  # IP address of the counter
    port=502
)

# Create collector
collector = EM530DataCollector(counter_config, modbus_tcp_config=tcp_config)

# Connect and read data
if collector.connect():
    data = collector.collect_data()
    if data:
        print(f"Voltage L1: {data['voltageL1']}V")
        print(f"Current L1: {data['currentL1']}A")
        print(f"Active Power: {data['activePower']}kW")
    collector.disconnect()
```

#### TCP with RTU Fallback
```python
from nemotek_counters.carlo_gavazzi.em530 import (
    CounterConfiguration, 
    ModbusTCPConfiguration,
    ModbusRTUConfiguration,
    EM530DataCollector
)

counter_config = CounterConfiguration(167, 100, "TestCounter", "MyCompany")
tcp_config = ModbusTCPConfiguration("192.168.1.100", 502)
rtu_config = ModbusRTUConfiguration("/dev/ttyNS0", 9600)

# Create collector with both configurations (tries TCP first, then RTU)
collector = EM530DataCollector(counter_config, 
                             modbus_tcp_config=tcp_config,
                             modbus_rtu_config=rtu_config)

if collector.connect():
    data = collector.collect_data()
    if data:
        print(f"Voltage L1: {data['voltageL1']}V")
    collector.disconnect()
```

### Lovato DMG210 Example
```python
from nemotek_counters.lovato.dmg210 import (
    ConfiguracaoContador,
    ConfiguracaoModbusTCP,
    ConfiguracaoModbusRTU,
    ColectorDadosDMG210
)

# Configure the counter  
config_contador = ConfiguracaoContador(
    id_contador=115,
    id_unidade=81,  # Modbus address
    nome_contador="Geral #115",
    id_empresa="MinhaEmpresa"
)

# Configure Modbus TCP (primary)
config_tcp = ConfiguracaoModbusTCP(
    host="172.16.5.11",
    porta=502
)

# Configure Modbus RTU (fallback)
config_rtu = ConfiguracaoModbusRTU(
    porta="/dev/ttyNS0",
    velocidade=9600
)

# Create collector with both TCP and RTU support
colector = ColectorDadosDMG210(config_contador, config_tcp, config_rtu)

# Connect and read data (tries TCP first, RTU as fallback)
if colector.ligar():
    dados = colector.recolher_dados()
    if dados:
        print(f"Voltage L1: {dados['vl1']}V")
        print(f"Current L1: {dados['il1']}A") 
        print(f"Power P1: {dados['p1']}kW")
        print(f"Frequency: {dados['freq']}Hz")
        print(f"Active Energy: {dados['energiaActiva']}kWh")
    colector.desligar()
```

## Supported Counters

| Brand | Model | Status | Modbus RTU | Modbus TCP | Features |
|-------|-------|--------|------------|------------|----------|
| **Carlo Gavazzi** | EM530 | ✅ **Implemented** | ✅ | ✅ | Full energy monitoring, fallback support |
| **Lovato** | DMG210 | ✅ **Implemented** | ✅ | ✅ | Complete energy data collection, dual communication |
| **Lovato** | DMG800 | 🚧 **Planned** | - | - | Module structure ready |
| **Lovato** | DMG6 | 🚧 **Planned** | - | - | Module structure ready |
| **Contrel** | uD3h | 🚧 **Planned** | - | - | Module structure ready |
| **Diris** | A10 | 🚧 **Planned** | - | - | Module structure ready |
| **RedZ** | LKM144 | 🚧 **Planned** | - | - | Module structure ready |
| **Schneider** | IEM3250 | 🚧 **Planned** | - | - | Module structure ready |
| **Schneider** | IEM3155 | 🚧 **Planned** | - | - | Module structure ready |

### Implementation Status Legend
- ✅ **Implemented**: Full functionality with comprehensive data collection
- 🚧 **Planned**: Module structure exists, implementation pending
- ✅ Modbus RTU/TCP: Protocol supported
- 🔄 **Fallback Support**: Automatic failover between TCP and RTU connections

## Requirements

- Python 3.8+
- pymodbus 3.0.0+
- pyserial 3.5+

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.