# Contrel Counters

This folder contains implementations for Contrel energy meters.

## Implemented Counters

### uD3h Energy Meter

The uD3h is a three-phase energy meter with comprehensive measurement capabilities and high precision.

#### Modbus Register Map

The uD3h implementation reads three separate register blocks:

##### Instant Data Block 1 (Address: 4098, Registers: 22)

| Register Address | Register Count | Data Type | Scale Factor | Description |
|------------------|----------------|-----------|--------------|-------------|
| 4098-4099 | 2 | uint32be | 1 | Voltage L1-N (V) |
| 4100-4101 | 2 | uint32be | 1 | Voltage L2-N (V) |
| 4102-4103 | 2 | uint32be | 1 | Voltage L3-N (V) |
| 4104-4105 | 2 | uint32be | 1 | Voltage L1-L2 (V) |
| 4106-4107 | 2 | uint32be | 1 | Voltage L2-L3 (V) |
| 4108-4109 | 2 | uint32be | 1 | Voltage L3-L1 (V) |
| 4110-4111 | 2 | uint32be | 1 | Current Equivalent (A) |
| 4112-4113 | 2 | uint32be | 0.001 | Current L1 (A) |
| 4114-4115 | 2 | uint32be | 0.001 | Current L2 (A) |
| 4116-4117 | 2 | uint32be | 0.001 | Current L3 (A) |
| 4118-4119 | 2 | int32be | 0.001 | Power Factor Equivalent |

##### Instant Data Block 2 (Address: 4134, Registers: 32)

| Register Address | Register Count | Data Type | Scale Factor | Description |
|------------------|----------------|-----------|--------------|-------------|
| 4134-4135 | 2 | uint32be | 1 | Apparent Power Equivalent (VA) |
| 4136-4137 | 2 | uint32be | 1 | Apparent Power L1 (VA) |
| 4138-4139 | 2 | uint32be | 1 | Apparent Power L2 (VA) |
| 4140-4141 | 2 | uint32be | 1 | Apparent Power L3 (VA) |
| 4142-4143 | 2 | uint32be | 1 | Active Power Equivalent (W) |
| 4144-4145 | 2 | uint32be | 1 | Active Power L1 (W) |
| 4146-4147 | 2 | uint32be | 1 | Active Power L2 (W) |
| 4148-4149 | 2 | uint32be | 1 | Active Power L3 (W) |
| 4150-4151 | 2 | uint32be | 1 | Reactive Power Equivalent (VAr) |
| 4158-4159 | 2 | uint32be | 0.1 | Active Energy (kWh) |
| 4160-4161 | 2 | uint32be | 0.1 | Reactive Energy (kVArh) |

##### Energy Data Block (Address: 4166, Registers: 6)

| Register Address | Register Count | Data Type | Scale Factor | Description |
|------------------|----------------|-----------|--------------|-------------|
| 4166-4167 | 2 | uint32be | 0.001 | Frequency (Hz) |
| 4170-4171 | 2 | uint32be | 0.1 | Apparent Energy (kVAh) |

#### Communication Parameters

- **Error Threshold**: 6 consecutive failures before declaring communication error
- **Default Unit ID**: 87 (as per Node-RED implementation)
- **Preferred Protocol**: Modbus TCP (port 502)
- **Fallback Protocol**: Modbus RTU

#### Usage Example

```python
from energy_counters.contrel.ud3h import (
    CounterConfiguration,
    ModbusTCPConfiguration,
    ModbusRTUConfiguration,
    UD3hDataCollector
)

# Configure the counter
counter_config = CounterConfiguration(
    counter_id=175,
    unit_id=1,  # Modbus address
    counter_name="MainMeter",
    company_id="MyCompany"
)

# Configure Modbus TCP connection (primary)
tcp_config = ModbusTCPConfiguration(
    host="192.162.10.10",
    port=502,
    timeout=4.0
)

# Configure Modbus RTU connection (fallback)
rtu_config = ModbusRTUConfiguration(
    port="/dev/ttyNS0",
    baudrate=9600
)

# Create collector with both TCP and RTU support
collector = UD3hDataCollector(
    counter_config,
    modbus_tcp_config=tcp_config,
    modbus_rtu_config=rtu_config
)

# Connect and read data (tries TCP first, RTU as fallback)
if collector.connect():
    data = collector.collect_data()
    if data:
        print(f"Counter: {data['counterName']}")
        print(f"L-N Voltage L1: {data['vl1']}V")
        print(f"L-L Voltage L12: {data['vl12']}V")
        print(f"Current L1: {data['il1']}A")
        print(f"Phase Power L1: {data['pl1']}W")
        print(f"Total Active Power: {data['paeq']}W")
        print(f"Frequency: {data['freq']}Hz")
        print(f"Power Factor: {data['pfeq']}")
        print(f"Active Energy: {data['energyActive']}Wh")
    collector.disconnect()
```

## Output Data Fields

The uD3h collector returns a dictionary with the following fields:

- `companyID`: Company identifier
- `ts`: ISO timestamp of the reading
- `counterID`: Counter identifier
- `counterName`: Counter name
- `vl1`, `vl2`, `vl3`: Line-to-neutral voltages (V)
- `vl12`, `vl23`, `vl31`: Line-to-line voltages (V)
- `il1`, `il2`, `il3`: Line currents (A)
- `pl1`, `pl2`, `pl3`: Phase active powers (W)
- `paeq`: Total active power (W)
- `qaeq`: Total reactive power (VAr)
- `saeq`: Total apparent power (VA)
- `pfeq`: Power factor equivalent
- `freq`: System frequency (Hz)
- `energyActive`: Active energy (kWh)
- `energyReactive`: Reactive energy (kVArh)
- `energyApparent`: Apparent energy (kVAh)
- `thdV1`, `thdV2`, `thdV3`: Voltage THD per phase (%) - hardcoded to "0"
- `thdIL1`, `thdIL2`, `thdIL3`: Current THD per phase (%) - hardcoded to "0"

**Note**: THD values are currently hardcoded to "0" as per the original Node-RED implementation.