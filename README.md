# Nemotek Counters Library

A Python library for reading data from various electrical energy counters including Carlo Gavazzi, Contrel, Diris, Lovato, RedZ, and Schneider devices.

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
    ConfiguracaoContador, 
    ConfiguracaoModbusRTU, 
    ColectorDadosEM530
)

# Configure the counter
config_contador = ConfiguracaoContador(
    id_contador=167,
    id_unidade=100,  # Modbus address
    nome_contador="ContadorTeste",
    id_empresa="MinhaEmpresa"
)

# Configure Modbus RTU connection
config_rtu = ConfiguracaoModbusRTU(
    porta="/dev/ttyNS0",  # Adjust according to your system
    velocidade=9600
)

# Create collector
colector = ColectorDadosEM530(config_contador, config_modbus_rtu=config_rtu)

# Connect and read data
if colector.ligar():
    dados = colector.recolher_dados()
    if dados:
        print(f"Voltage L1: {dados['tensaoL1']}V")
        print(f"Current L1: {dados['correnteL1']}A")
        print(f"Active Power: {dados['potenciaActiva']}kW")
    colector.desligar()
```

#### TCP Connection
```python
from nemotek_counters.carlo_gavazzi.em530 import (
    ConfiguracaoContador, 
    ConfiguracaoModbusTCP, 
    ColectorDadosEM530
)

# Configure the counter
config_contador = ConfiguracaoContador(
    id_contador=167,
    id_unidade=100,  # Modbus address
    nome_contador="ContadorTeste",
    id_empresa="MinhaEmpresa"
)

# Configure Modbus TCP connection
config_tcp = ConfiguracaoModbusTCP(
    host="192.168.1.100",  # IP address of the counter
    porta=502
)

# Create collector
colector = ColectorDadosEM530(config_contador, config_modbus_tcp=config_tcp)

# Connect and read data
if colector.ligar():
    dados = colector.recolher_dados()
    if dados:
        print(f"Voltage L1: {dados['tensaoL1']}V")
        print(f"Current L1: {dados['correnteL1']}A")
        print(f"Active Power: {dados['potenciaActiva']}kW")
    colector.desligar()
```

#### TCP with RTU Fallback
```python
from nemotek_counters.carlo_gavazzi.em530 import (
    ConfiguracaoContador, 
    ConfiguracaoModbusTCP,
    ConfiguracaoModbusRTU,
    ColectorDadosEM530
)

config_contador = ConfiguracaoContador(167, 100, "ContadorTeste", "MinhaEmpresa")
config_tcp = ConfiguracaoModbusTCP("192.168.1.100", 502)
config_rtu = ConfiguracaoModbusRTU("/dev/ttyNS0", 9600)

# Create collector with both configurations (tries TCP first, then RTU)
colector = ColectorDadosEM530(config_contador, 
                             config_modbus_tcp=config_tcp,
                             config_modbus_rtu=config_rtu)

if colector.ligar():
    dados = colector.recolher_dados()
    if dados:
        print(f"Voltage L1: {dados['tensaoL1']}V")
    colector.desligar()
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

### Currently Implemented
- **Carlo Gavazzi EM530**: Full Modbus RTU and TCP implementation with fallback support
- **Lovato DMG210**: Full Modbus TCP and RTU implementation with fallback support

### Planned (Empty modules ready for implementation)
- **Contrel uD3h**
- **Diris A10**
- **Lovato DMG800**
- **Lovato DMG6**
- **RedZ LKM144**
- **Schneider IEM3250**
- **Schneider IEM3155**

## Requirements

- Python 3.8+
- pymodbus 3.0.0+
- pyserial 3.5+

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.