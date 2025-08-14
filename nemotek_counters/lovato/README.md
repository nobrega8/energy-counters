# Lovato Counters

This folder contains implementations for Lovato energy meters.

## Implemented Counters

### DMG210 Energy Meter

The DMG210 is a three-phase energy meter with comprehensive measurement capabilities.

#### Modbus Register Map

The DMG210 implementation reads three separate register blocks:

##### Instantaneous Data Block (Address: 2, Registers: 24)

| Register Address | Register Count | Data Type | Scale Factor | Description |
|------------------|----------------|-----------|--------------|-------------|
| 2-3 | 2 | uint32be | 0.01 | Voltage L1-N (V) |
| 4-5 | 2 | uint32be | 0.01 | Voltage L2-N (V) |
| 6-7 | 2 | uint32be | 0.01 | Voltage L3-N (V) |
| 8-9 | 2 | uint32be | 0.0001 | Current L1 (A) |
| 10-11 | 2 | uint32be | 0.0001 | Current L2 (A) |
| 12-13 | 2 | uint32be | 0.0001 | Current L3 (A) |
| 14-15 | 2 | uint32be | 0.01 | Voltage L1-L2 (V) |
| 16-17 | 2 | uint32be | 0.01 | Voltage L2-L3 (V) |
| 18-19 | 2 | uint32be | 0.01 | Voltage L3-L1 (V) |
| 20-21 | 2 | int32be | 0.01 | Active Power L1 (kW) |
| 22-23 | 2 | int32be | 0.01 | Active Power L2 (kW) |
| 24-25 | 2 | int32be | 0.01 | Active Power L3 (kW) |

##### Frequency and Equivalent Data Block (Address: 50/0x32, Registers: 38)

| Register Offset | Register Count | Data Type | Scale Factor | Description |
|-----------------|----------------|-----------|--------------|-------------|
| 0-1 | 2 | uint32be | 0.01 | Frequency (Hz) |
| 2-3 | 2 | uint32be | 0.01 | Voltage Equivalent (V) |
| 4-5 | 2 | uint32be | 0.01 | Voltage Equivalent L-L (V) |
| 6-7 | 2 | uint32be | 0.0001 | Current Equivalent (A) |
| 8-9 | 2 | int32be | 0.01 | Active Power Equivalent (kW) |
| 10-11 | 2 | int32be | 0.01 | Reactive Power Equivalent (kVAr) |
| 12-13 | 2 | uint32be | 0.01 | Apparent Power Equivalent (kVA) |
| 14-15 | 2 | int32be | 0.0001 | Power Factor Equivalent |
| 16-17 | 2 | uint32be | 0.01 | Current THD L1 (%) |
| 18-19 | 2 | uint32be | 0.01 | Current THD L2 (%) |
| 20-21 | 2 | uint32be | 0.01 | Current THD L3 (%) |
| 22-23 | 2 | uint32be | 0.01 | Voltage THD L1 (%) |
| 24-25 | 2 | uint32be | 0.01 | Voltage THD L2 (%) |
| 26-27 | 2 | uint32be | 0.01 | Voltage THD L3 (%) |

##### Energy Data Block (Address: 6687, Registers: 10)

| Register Offset | Register Count | Data Type | Scale Factor | Description |
|-----------------|----------------|-----------|--------------|-------------|
| 0-1 | 2 | uint32be | 0.01 | Active Energy Import (kWh) |
| 2-3 | 2 | uint32be | 0.01 | Active Energy Export (kWh) |
| 4-5 | 2 | uint32be | 0.01 | Reactive Energy Import (kVArh) |
| 6-7 | 2 | uint32be | 0.01 | Reactive Energy Export (kVArh) |
| 8-9 | 2 | uint32be | 0.01 | Apparent Energy (kVAh) |

#### Communication Parameters

- **Error Threshold**: 2 consecutive failures before declaring communication error
- **Preferred Protocol**: Both TCP and RTU supported
- **Data Format**: Big-endian for multi-register values

#### Usage Example

```python
from nemotek_counters.common import CounterConfiguration, ModbusTCPConfiguration
from nemotek_counters.lovato.dmg210 import DMG210DataCollector

# Configure counter
counter_config = CounterConfiguration(
    counter_id=123,
    unit_id=1,
    counter_name="DMG210_Main",
    company_id="MyCompany"
)

# Configure Modbus TCP
modbus_config = ModbusTCPConfiguration(
    host="192.162.10.10",
    port=502
)

# Create collector and get data
collector = DMG210DataCollector(counter_config, modbus_tcp_config=modbus_config)
if collector.connect():
    data = collector.collect_data()
    print(f"Voltage L1: {data['vl1']}V")
    print(f"Current L1: {data['il1']}A")
    print(f"Power L1: {data['p1']}kW")
    print(f"Frequency: {data['freq']}Hz")
    collector.disconnect()
```

## Output Data Fields

The DMG210 collector returns a dictionary with the following fields:

### Basic Information
- `companyId`: Company identifier
- `timestamp`: ISO timestamp of the reading
- `counterId`: Counter identifier
- `counterName`: Counter name

### Electrical Measurements
- `vl1`, `vl2`, `vl3`: Line-to-neutral voltages (V)
- `vl12`, `vl23`, `vl31`: Line-to-line voltages (V)
- `il1`, `il2`, `il3`: Line currents (A)
- `p1`, `p2`, `p3`: Phase active powers (kW)
- `freq`: System frequency (Hz)

### Equivalent Values
- `veq`: Voltage equivalent (V)
- `veql`: Voltage equivalent L-L (V)
- `ieq`: Current equivalent (A)
- `peq`: Active power equivalent (kW)
- `qeq`: Reactive power equivalent (kVAr)
- `seq`: Apparent power equivalent (kVA)
- `pfeq`: Power factor equivalent

### Energy Measurements
- `activeEnergyImport`: Active energy import (kWh)
- `activeEnergyExport`: Active energy export (kWh)
- `reactiveEnergyImport`: Reactive energy import (kVArh)
- `reactiveEnergyExport`: Reactive energy export (kVArh)
- `apparentEnergy`: Apparent energy (kVAh)

### Power Quality
- `thdCurrentL1`, `thdCurrentL2`, `thdCurrentL3`: Current THD per phase (%)
- `thdVoltageL1`, `thdVoltageL2`, `thdVoltageL3`: Voltage THD per phase (%)

## Planned Counters

### DMG6 Energy Meter
- **Status**: Not yet implemented
- **Description**: Will provide interface for the Lovato DMG6 energy meter

### DMG800 Energy Meter
- **Status**: Not yet implemented
- **Description**: Will provide interface for the Lovato DMG800 energy meter