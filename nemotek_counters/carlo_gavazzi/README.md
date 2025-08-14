# Carlo Gavazzi Counters

This folder contains implementations for Carlo Gavazzi energy meters.

## Implemented Counters

### EM530 Energy Meter

The EM530 is a three-phase energy meter with comprehensive measurement capabilities.

#### Modbus Register Map

The EM530 implementation reads four separate register blocks:

##### Main Data Block (Address: 0x0000, Registers: 64)

| Register Address | Register Count | Data Type | Scale Factor | Description |
|------------------|----------------|-----------|--------------|-------------|
| 0x0000-0x0001 | 2 | uint32be | 0.1 | Voltage L1-N (V) |
| 0x0002-0x0003 | 2 | uint32be | 0.1 | Voltage L2-N (V) |
| 0x0004-0x0005 | 2 | uint32be | 0.1 | Voltage L3-N (V) |
| 0x0006-0x0007 | 2 | uint32be | 0.1 | Voltage L1-L2 (V) |
| 0x0008-0x0009 | 2 | uint32be | 0.1 | Voltage L2-L3 (V) |
| 0x000A-0x000B | 2 | uint32be | 0.1 | Voltage L3-L1 (V) |
| 0x000C-0x000D | 2 | uint32be | 0.001 | Current L1 (A) |
| 0x000E-0x000F | 2 | uint32be | 0.001 | Current L2 (A) |
| 0x0010-0x0011 | 2 | uint32be | 0.001 | Current L3 (A) |
| 0x0012-0x0013 | 2 | uint32be | 0.0001 | Active Power L1 (kW) |
| 0x0014-0x0015 | 2 | uint32be | 0.0001 | Active Power L2 (kW) |
| 0x0016-0x0017 | 2 | uint32be | 0.0001 | Active Power L3 (kW) |
| 0x0028-0x0029 | 2 | uint32be | 0.1 | Total Active Power (kW) |
| 0x002A-0x002B | 2 | uint32be | 0.1 | Total Apparent Power (kVA) |
| 0x002C-0x002D | 2 | uint32be | 0.1 | Total Reactive Power (kVAr) |
| 0x0031 | 1 | uint16 | 0.001 | Power Factor |
| 0x0033 | 1 | uint16 | 0.1 | Frequency (Hz) |
| 0x0034-0x0035 | 2 | uint32be | 0.1 | Active Energy (kWh) |
| 0x0036-0x0037 | 2 | uint32be | 0.1 | Reactive Energy (kVArh) |

##### Apparent Energy Block (Address: 0x0056, Registers: 2)

| Register Address | Register Count | Data Type | Scale Factor | Description |
|------------------|----------------|-----------|--------------|-------------|
| 0x0056-0x0057 | 2 | uint32be | 0.1 | Apparent Energy (kVAh) |

##### Current THD Block (Address: 0x0082, Registers: 6)

| Register Address | Register Count | Data Type | Scale Factor | Description |
|------------------|----------------|-----------|--------------|-------------|
| 0x0082-0x0083 | 2 | uint32be | 0.01 | Current THD L1 (%) |
| 0x0084-0x0085 | 2 | uint32be | 0.01 | Current THD L2 (%) |
| 0x0086-0x0087 | 2 | uint32be | 0.01 | Current THD L3 (%) |

##### Voltage THD Block (Address: 0x0092, Registers: 6)

| Register Address | Register Count | Data Type | Scale Factor | Description |
|------------------|----------------|-----------|--------------|-------------|
| 0x0092-0x0093 | 2 | uint32be | 0.01 | Voltage THD L1 (%) |
| 0x0094-0x0095 | 2 | uint32be | 0.01 | Voltage THD L2 (%) |
| 0x0096-0x0097 | 2 | uint32be | 0.01 | Voltage THD L3 (%) |

#### Usage Example

```python
from nemotek_counters.common import CounterConfiguration, ModbusTCPConfiguration
from nemotek_counters.carlo_gavazzi.em530 import EM530DataCollector

# Configure counter
counter_config = CounterConfiguration(
    counter_id=167,
    unit_id=100,
    counter_name="EM530_Main",
    company_id="MyCompany"
)

# Configure Modbus TCP
modbus_config = ModbusTCPConfiguration(
    host="192.162.10.10",
    port=502
)

# Create collector and get data
collector = EM530DataCollector(counter_config, modbus_tcp_config=modbus_config)
if collector.connect():
    data = collector.collect_data()
    print(f"Voltage L1: {data['voltageL1']}V")
    print(f"Current L1: {data['currentL1']}A")
    print(f"Active Power: {data['activePower']}kW")
    collector.disconnect()
```

## Output Data Fields

The EM530 collector returns a dictionary with the following fields:

- `companyId`: Company identifier
- `timestamp`: ISO timestamp of the reading
- `counterId`: Counter identifier
- `counterName`: Counter name
- `voltageL1`, `voltageL2`, `voltageL3`: Line-to-neutral voltages (V)
- `voltageL12`, `voltageL23`, `voltageL31`: Line-to-line voltages (V)
- `currentL1`, `currentL2`, `currentL3`: Line currents (A)
- `powerL1`, `powerL2`, `powerL3`: Phase active powers (kW)
- `activePower`: Total active power (kW)
- `reactivePower`: Total reactive power (kVAr)
- `apparentPower`: Total apparent power (kVA)
- `powerFactor`: Power factor
- `frequency`: System frequency (Hz)
- `activeEnergy`: Active energy (kWh)
- `reactiveEnergy`: Reactive energy (kVArh)
- `apparentEnergy`: Apparent energy (kVAh)
- `thdCurrentL1`, `thdCurrentL2`, `thdCurrentL3`: Current THD per phase (%)
- `thdVoltageL1`, `thdVoltageL2`, `thdVoltageL3`: Voltage THD per phase (%)