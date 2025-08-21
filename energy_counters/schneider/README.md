# Schneider Electric Counters

This folder contains implementations for Schneider Electric energy meters.

## Implemented Counters

### IEM3255 Energy Meter

- **Status**: ✅ Implemented
- **Counter ID**: 130
- **Unit ID**: 12
- **Counter Name**: "L21 - Bobinadora"
- **Description**: Interface for the Schneider Electric IEM3255 energy meter
- **Based on**: Node-RED flow from issue #21
- **Features**:
  - Modbus TCP/RTU communication support
  - Error threshold of 6 consecutive failures
  - Multiple register block data collection
  - Standardized output format
  - Professional error handling and logging

### IEM3155 Energy Meter

- **Status**: ✅ Implemented
- **Counter ID**: 137
- **Unit ID**: 20
- **Counter Name**: "L21 - Secadores Linhas 21 e 22"
- **Description**: Interface for the Schneider Electric IEM3155 energy meter (similar to IEM3255)
- **Based on**: Same register map as IEM3255
- **Features**:
  - Modbus TCP/RTU communication support
  - Error threshold of 6 consecutive failures
  - Multiple register block data collection
  - Standardized output format
  - Professional error handling and logging

#### Communication Parameters

- **Error Threshold**: 6 consecutive failures before declaring communication error
- **IEM3255 (Counter #130)**: Unit ID 12, "L21 - Bobinadora"
- **IEM3155 (Counter #137)**: Unit ID 20, "L21 - Secadores Linhas 21 e 22" 
- **Preferred Protocol**: Modbus TCP (port 502)
- **Fallback Protocol**: Modbus RTU
- **Default Host**: 172.16.5.9 (as per Node-RED implementation)

#### Modbus Register Map

##### Current Data Block (Address: 2998, Registers: 8)

| Register Address | Register Count | Data Type | Scale Factor | Description |
|------------------|----------------|-----------|--------------|-------------|
| 2998-2999 | 2 | floatbe | 1 | Current L1 (A) |
| 3000-3001 | 2 | floatbe | 1 | Current L2 (A) |
| 3002-3003 | 2 | floatbe | 1 | Current L3 (A) |

##### Voltage Data Block (Address: 3018, Registers: 16)

| Register Address | Register Count | Data Type | Scale Factor | Description |
|------------------|----------------|-----------|--------------|-------------|
| 3018-3019 | 2 | floatbe | 1 | Voltage L1-L2 (V) |
| 3020-3021 | 2 | floatbe | 1 | Voltage L2-L3 (V) |
| 3022-3023 | 2 | floatbe | 1 | Voltage L3-L1 (V) |
| 3026-3027 | 2 | floatbe | 1 | Voltage L1 (V) |
| 3028-3029 | 2 | floatbe | 1 | Voltage L2 (V) |
| 3030-3031 | 2 | floatbe | 1 | Voltage L3 (V) |

##### Power Data Block (Address: 3052, Registers: 12)

| Register Address | Register Count | Data Type | Scale Factor | Description |
|------------------|----------------|-----------|--------------|-------------|
| 3052-3053 | 2 | floatbe | 1 | Active Power L1 (W) |
| 3054-3055 | 2 | floatbe | 1 | Active Power L2 (W) |
| 3056-3057 | 2 | floatbe | 1 | Active Power L3 (W) |
| 3058-3059 | 2 | floatbe | 1 | Active Power Equivalent (W) |

##### Frequency Data Block (Address: 3108, Registers: 4)

| Register Address | Register Count | Data Type | Scale Factor | Description |
|------------------|----------------|-----------|--------------|-------------|
| 3108-3109 | 2 | floatbe | 1 | Frequency (Hz) |

##### Energy Data Block (Address: 45098, Registers: 4)

| Register Address | Register Count | Data Type | Scale Factor | Description |
|------------------|----------------|-----------|--------------|-------------|
| 45098-45099 | 2 | floatbe | 1 | Active Energy (kWh) |

#### Output Data Fields

- `companyID`: Company identifier
- `ts`: Timestamp (ISO format)
- `counterID`: Counter identifier (130 or 137)
- `counterName`: Counter name
- `vl12`, `vl23`, `vl31`: Line-to-line voltages (V)
- `vl1`, `vl2`, `vl3`: Line-to-neutral voltages (V) - hardcoded to "0.0"
- `il1`, `il2`, `il3`: Line currents (A)
- `pl1`, `pl2`, `pl3`: Line powers (W) - hardcoded to "0.0"
- `paeq`, `qaeq`, `saeq`, `pfeq`: Equivalent powers - hardcoded to "0.0"
- `freq`: Frequency (Hz)
- `energyActive`: Active energy (kWh)
- `energyReactive`, `energyApparent`: Reactive and apparent energy - hardcoded to "0.0"
- `thdV1`, `thdV2`, `thdV3`: Voltage THD per phase (%) - hardcoded to "0.0"
- `thdIL1`, `thdIL2`, `thdIL3`: Current THD per phase (%) - hardcoded to "0.0"

**Note**: Some values are hardcoded to "0.0" as per the original Node-RED implementation.

#### Usage Examples

##### IEM3255 (Counter ID 130)

```python
from energy_counters.schneider import IEM3255DataCollector
from energy_counters.common import CounterConfiguration, ModbusTCPConfiguration

# Configure counter
counter_config = CounterConfiguration(
    counter_id=130,
    unit_id=12,
    counter_name="L21 - Bobinadora",
    company_id="YourCompany"
)

# Configure TCP connection
tcp_config = ModbusTCPConfiguration(
    host="172.16.5.9",
    port=502,
    timeout=3.0
)

# Create collector and collect data
collector = IEM3255DataCollector(counter_config, tcp_config, use_tcp=True)
collector.connect()
data = collector.collect_data()
print(data)
collector.disconnect()
```

##### IEM3155 (Counter ID 137)

```python
from energy_counters.schneider import IEM3155DataCollector
from energy_counters.common import CounterConfiguration, ModbusTCPConfiguration

# Configure counter
counter_config = CounterConfiguration(
    counter_id=137,
    unit_id=20,
    counter_name="L21 - Secadores Linhas 21 e 22",
    company_id="YourCompany"
)

# Configure TCP connection
tcp_config = ModbusTCPConfiguration(
    host="172.16.5.9",
    port=502,
    timeout=3.0
)

# Create collector and collect data
collector = IEM3155DataCollector(counter_config, tcp_config, use_tcp=True)
collector.connect()
data = collector.collect_data()
print(data)
collector.disconnect()
```

## Planned Counters

### IEM3250 Energy Meter

- **Status**: Not yet implemented
- **Description**: Will provide interface for the Schneider Electric IEM3250 energy meter
- **Features**: To be implemented including:
  - Configuration classes
  - Communication protocol setup
  - Data collection functions
  - Error handling

## Implementation Status

Both IEM3255 and IEM3155 counters are fully implemented and ready for use. The remaining counters are in planning phase. The implementation follows the same patterns established by other counter modules in this library:

- Modbus TCP/RTU communication support
- Configurable error thresholds
- Comprehensive data collection
- Standardized output format
- Professional error handling and logging

## Future Development

The remaining Schneider Electric counter implementations will be added in future releases with:

- Complete Modbus register mapping documentation
- Usage examples and configuration guides
- Comprehensive test coverage
- Integration with the existing counter framework

Register tables and detailed documentation will be added once the implementations are complete.