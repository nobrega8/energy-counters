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
```python
from nemotek_counters.carlo_gavazzi.em530 import (
    ConfiguracaoContador, 
    ConfiguracaoModbus, 
    ColectorDadosEM530
)

# Configure the counter
config_contador = ConfiguracaoContador(
    id_contador=167,
    id_unidade=100,  # Modbus address
    nome_contador="ContadorTeste",
    id_empresa="MinhaEmpresa"
)

# Configure Modbus connection
config_modbus = ConfiguracaoModbus(
    porta="/dev/ttyNS0",  # Adjust according to your system
    velocidade=9600
)

# Create collector
colector = ColectorDadosEM530(config_contador, config_modbus)

# Connect and read data
if colector.ligar():
    dados = colector.recolher_dados()
    if dados:
        print(f"Voltage L1: {dados['tensaoL1']}V")
        print(f"Current L1: {dados['correnteL1']}A")
        print(f"Active Power: {dados['potenciaActiva']}kW")
    colector.desligar()
```

## Supported Counters

### Currently Implemented
- **Carlo Gavazzi EM530**: Full Modbus RTU implementation

### Planned (Empty modules ready for implementation)
- **Contrel uD3h**
- **Diris A10**
- **Lovato DMG800**
- **Lovato DMG210** 
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