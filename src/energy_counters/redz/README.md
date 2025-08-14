# RedZ Counters

This folder contains implementations for RedZ energy meters.

## Implemented Counters

### LKM144 Energy Meter

The LKM144 is a three-phase energy meter with comprehensive energy measurement and power monitoring capabilities.

#### Modbus Register Map

The LKM144 implementation reads all data in a single operation:

##### Complete Data Block (Address: 0x00, Registers: 48)

The LKM144 reads 48 registers (96 bytes) in one operation, which are parsed as 24 uint32be values:

| Register Offset | Register Count | Data Type | Scale Factor | Description |
|-----------------|----------------|-----------|--------------|-------------|
| 0-1 | 2 | uint32be | 1 | Time |
| 2-3 | 2 | uint32be | 1 | Date |
| 4-5 | 2 | uint32be | 1 | Total Active Energy Import A+ (Wh) |
| 6-7 | 2 | uint32be | 1 | Total Active Energy Export A- (Wh) |
| 8-9 | 2 | uint32be | 1 | Total Reactive Energy Import R+ (VArh) |
| 10-11 | 2 | uint32be | 1 | Total Reactive Energy Export R- (VArh) |
| 12-13 | 2 | uint32be | 1 | Total Reactive Energy (VArh) |
| 14-15 | 2 | uint32be | 1 | Reactive Energy Capacitive Import Rc+ Q2 (VArh) |
| 16-17 | 2 | uint32be | 1 | Reactive Energy Inductive Export Ri- Q3 (VArh) |
| 18-19 | 2 | uint32be | 1 | Reactive Energy Capacitive Export Rc- Q4 (VArh) |
| 20-21 | 2 | uint32be | 1 | Maximum Power Import P+max (W) |
| 22-23 | 2 | uint32be | 1 | Maximum Power Export P-max (W) |
| 24-25 | 2 | uint32be | 1 | Average Power Import P+max Last Period (W) |
| 26-27 | 2 | uint32be | 1 | Instantaneous Power P+ (W) |
| 28-29 | 2 | uint32be | 1 | Current L1 (mA) |
| 30-31 | 2 | uint32be | 1 | Current L2 (mA) |
| 32-33 | 2 | uint32be | 1 | Current L3 (mA) |
| 34-35 | 2 | uint32be | 1 | Voltage L1 (mV) |
| 36-37 | 2 | uint32be | 1 | Voltage L2 (mV) |
| 38-39 | 2 | uint32be | 1 | Voltage L3 (mV) |
| 40-41 | 2 | uint32be | 1 | Power Factor |
| 42-43 | 2 | uint32be | 1 | Frequency (mHz) |
| 44-45 | 2 | uint32be | 1 | Meter Number |
| 46-47 | 2 | uint32be | 1 | Sum Active Power A+ - A- (W) |

#### Communication Parameters

- **Error Threshold**: 5 consecutive failures before declaring communication error
- **Preferred Protocol**: Modbus RTU (primary), Modbus TCP (fallback)
- **Data Format**: Big-endian for all multi-register values
- **Single Read Operation**: All 48 registers read in one Modbus transaction

#### Usage Example

```python
from energy_counters.redz import (
    CounterConfiguration,
    ModbusRTUConfiguration,
    ModbusTCPConfiguration,
    LKM144DataCollector
)

# Configure the counter (matching Node-RED Red Z#10 setup)
counter_config = CounterConfiguration(
    counter_id=200,
    unit_id=1,  # Modbus address
    counter_name="e-Redes",
    company_id="MyCompany"
)

# Configure Modbus RTU connection (primary for LKM144)
rtu_config = ModbusRTUConfiguration(
    port="/dev/ttyNS0",
    baudrate=9600
)

# Optional TCP configuration (fallback)
tcp_config = ModbusTCPConfiguration(
    host="192.162.10.10",
    port=502
)

# Create collector with RTU primary, TCP fallback
collector = LKM144DataCollector(
    counter_config,
    modbus_tcp_config=tcp_config,
    modbus_rtu_config=rtu_config
)

# Connect and read data
if collector.connect():
    data = collector.collect_data()
    if data:
        print(f"Counter: {data['counterName']}")
        print(f"Voltage L1: {data['voltageL1']}")
        print(f"Current L1: {data['currentL1']}")
        print(f"Instantaneous Power: {data['instantaneousPower']}")
        print(f"Active Energy: {data['energyActive']}")
        print(f"Reactive Energy: {data['energyReactive']}")
        print(f"Power Factor: {data['powerFactor']}")
        print(f"Frequency: {data['frequency']}")
        print(f"Meter Number: {data['meterNumber']}")
    collector.disconnect()
```

## Output Data Fields

The LKM144 collector returns a dictionary with the following fields:

### Basic Information
- `companyId`: Company identifier
- `timestamp`: ISO timestamp of the reading
- `counterId`: Counter identifier
- `counterName`: Counter name

### Time and Date
- `time`: Internal meter time
- `date`: Internal meter date

### Energy Measurements (Wh/VArh)
- `energyActive`: Total active energy import A+ (Wh)
- `energyActiveExport`: Total active energy export A- (Wh)
- `energyReactiveImport`: Total reactive energy import R+ (VArh)
- `energyReactiveExport`: Total reactive energy export R- (VArh)
- `energyReactive`: Total reactive energy (VArh)
- `energyReactiveCapacitiveImport`: Reactive energy capacitive import Rc+ Q2 (VArh)
- `energyReactiveInductiveExport`: Reactive energy inductive export Ri- Q3 (VArh)
- `energyReactiveCapacitiveExport`: Reactive energy capacitive export Rc- Q4 (VArh)

### Power Measurements (W)
- `maxPowerImport`: Maximum power import P+max (W)
- `maxPowerExport`: Maximum power export P-max (W)
- `avgPowerImport`: Average power import P+max last period (W)
- `instantaneousPower`: Instantaneous power P+ (W)
- `sumActivePower`: Sum active power A+ - A- (W)

### Electrical Measurements
- `currentL1`, `currentL2`, `currentL3`: Line currents (mA)
- `voltageL1`, `voltageL2`, `voltageL3`: Line voltages (mV)
- `powerFactor`: Power factor
- `frequency`: System frequency (mHz)

### Meter Information
- `meterNumber`: Internal meter identification number

**Note**: The LKM144 provides measurements in base units (mA, mV, mHz, Wh) rather than standard electrical units. This is according to the original Node-RED implementation and the meter's native data format.