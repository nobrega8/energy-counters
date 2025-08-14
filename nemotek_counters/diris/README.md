# Diris Counters

This folder contains implementations for Diris energy meters.

## Implemented Counters

### A10 Energy Meter

The Diris A10 is a three-phase energy meter with comprehensive measurement capabilities and advanced power quality monitoring.

#### Modbus Register Map

The A10 implementation reads three separate register blocks:

##### Instant Data Block (Address: 50514, Registers: 36)

| Register Address | Register Count | Data Type | Scale Factor | Description |
|------------------|----------------|-----------|--------------|-------------|
| 50514-50515 | 2 | uint32be | 1 | Voltage L1-L2 (V) |
| 50516-50517 | 2 | uint32be | 1 | Voltage L2-L3 (V) |
| 50518-50519 | 2 | uint32be | 1 | Voltage L3-L1 (V) |
| 50520-50521 | 2 | uint32be | 1 | Voltage L1-N (V) |
| 50522-50523 | 2 | uint32be | 1 | Voltage L2-N (V) |
| 50524-50525 | 2 | uint32be | 1 | Voltage L3-N (V) |
| 50526-50527 | 2 | uint32be | 0.001 | Frequency (Hz) |
| 50528-50529 | 2 | uint32be | 0.001 | Current L1 (A) |
| 50530-50531 | 2 | uint32be | 0.001 | Current L2 (A) |
| 50532-50533 | 2 | uint32be | 0.001 | Current L3 (A) |
| 50534-50535 | 2 | uint32be | 0.001 | Current Neutral (A) |
| 50536-50537 | 2 | int32be | 1 | Active Power Equivalent (W) |
| 50538-50539 | 2 | int32be | 1 | Reactive Power Equivalent (VAr) |
| 50540-50541 | 2 | uint32be | 1 | Apparent Power Equivalent (VA) |
| 50542-50543 | 2 | int32be | 0.001 | Power Factor Equivalent |
| 50544-50545 | 2 | int32be | 1 | Active Power L1 (W) |
| 50546-50547 | 2 | int32be | 1 | Active Power L2 (W) |
| 50548-50549 | 2 | int32be | 1 | Active Power L3 (W) |

##### Energy Data Block (Address: 50780, Registers: 6)

| Register Address | Register Count | Data Type | Scale Factor | Description |
|------------------|----------------|-----------|--------------|-------------|
| 50780-50781 | 2 | uint32be | 0.1 | Active Energy (kWh) |
| 50782-50783 | 2 | uint32be | 0.1 | Reactive Energy (kVArh) |
| 50784-50785 | 2 | uint32be | 0.1 | Apparent Energy (kVAh) |

##### THD Data Block (Address: 51539, Registers: 6)

| Register Address | Register Count | Data Type | Scale Factor | Description |
|------------------|----------------|-----------|--------------|-------------|
| 51539 | 1 | uint16 | 0.01 | Voltage THD L1 (%) |
| 51540 | 1 | uint16 | 0.01 | Voltage THD L2 (%) |
| 51541 | 1 | uint16 | 0.01 | Voltage THD L3 (%) |
| 51542 | 1 | uint16 | 0.01 | Current THD L1 (%) |
| 51543 | 1 | uint16 | 0.01 | Current THD L2 (%) |
| 51544 | 1 | uint16 | 0.01 | Current THD L3 (%) |

#### Communication Parameters

- **Error Threshold**: 6 consecutive failures before declaring communication error
- **Preferred Protocol**: Modbus TCP (port 502)
- **Fallback Protocol**: Modbus RTU
- **Register Addressing**: Extended range (50000+ registers)
- **Data Format**: Big-endian for multi-register values

#### Usage Example

```python
from nemotek_counters.common import CounterConfiguration, ModbusTCPConfiguration
from nemotek_counters.diris.a10 import A10DataCollector

# Configure counter
counter_config = CounterConfiguration(
    counter_id=789,
    unit_id=1,
    counter_name="Diris_A10_Main",
    company_id="MyCompany"
)

# Configure Modbus TCP
modbus_config = ModbusTCPConfiguration(
    host="192.162.10.10",
    port=502,
    timeout=3.0
)

# Create collector and get data
collector = A10DataCollector(counter_config, modbus_tcp_config=modbus_config)
if collector.connect():
    data = collector.collect_data()
    print(f"Voltage L1: {data['vl1']}V")
    print(f"Current L1: {data['il1']}A")
    print(f"Active Power: {data['paeq']}W")
    print(f"Frequency: {data['freq']}Hz")
    collector.disconnect()
```

## Output Data Fields

The A10 collector returns a dictionary with the following fields:

### Basic Information
- `companyId`: Company identifier
- `timestamp`: ISO timestamp of the reading
- `counterId`: Counter identifier
- `counterName`: Counter name

### Voltage Measurements (V)
- `vl1`, `vl2`, `vl3`: Line-to-neutral voltages (V)
- `vl12`, `vl23`, `vl31`: Line-to-line voltages (V)

### Current Measurements (A)
- `il1`, `il2`, `il3`: Line currents (A)
- `iln`: Neutral current (A)

### Power Measurements
- `paeq`: Active power equivalent (W)
- `qaeq`: Reactive power equivalent (VAr)
- `saeq`: Apparent power equivalent (VA)
- `pfeq`: Power factor equivalent
- `pl1`, `pl2`, `pl3`: Phase active powers (W)

### System Parameters
- `freq`: System frequency (Hz)

### Energy Measurements
- `energyActive`: Active energy (kWh)
- `energyReactive`: Reactive energy (kVArh)
- `energyApparent`: Apparent energy (kVAh)

### Power Quality (THD)
- `thdV1`, `thdV2`, `thdV3`: Voltage THD per phase (%)
- `thdIL1`, `thdIL2`, `thdIL3`: Current THD per phase (%)

**Note**: The A10 provides comprehensive power quality monitoring including THD measurements, making it suitable for applications requiring detailed electrical analysis.