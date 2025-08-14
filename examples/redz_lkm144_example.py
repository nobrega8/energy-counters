#!/usr/bin/env python3
"""
RedZ LKM144 Energy Meter Example
This example demonstrates how to use the RedZ LKM144 data collector
based on the Node-RED implementation.
"""

import time
import json
from nemotek_counters.redz.lkm144 import (
    LKM144DataCollector,
    CounterConfiguration,
    ModbusRTUConfiguration,
    ModbusTCPConfiguration
)

def main():
    """Example usage of RedZ LKM144 data collector"""
    
    # Configure the counter (matches Node-RED Red Z#10 configuration)
    counter_config = CounterConfiguration(
        counter_id=200,         # From Node-RED: msg.counterID = 200
        unit_id=1,              # From Node-RED: msg.unitid = 1
        counter_name="e-Redes", # From Node-RED: msg.counterName = 'e-Redes'
        company_id="MyCompany"
    )

    # Configure Modbus RTU connection (primary, matches Node-RED setup)
    rtu_config = ModbusRTUConfiguration(
        port="/dev/ttyNS0",  # From Node-RED serialPort: "/dev/ttyNS0"
        baudrate=9600        # From Node-RED serialBaudrate: "9600"
    )

    # Optional TCP configuration (fallback)
    tcp_config = ModbusTCPConfiguration(
        host="192.162.10.10",
        port=502,
        timeout=4.0
    )

    # Create collector with RTU primary and TCP fallback
    collector = LKM144DataCollector(
        counter_config,
        modbus_tcp_config=tcp_config,
        modbus_rtu_config=rtu_config
    )

    print("RedZ LKM144 Data Collection Example")
    print("=" * 40)
    print(f"Counter: {counter_config.counter_name}")
    print(f"Counter ID: {counter_config.counter_id}")
    print(f"Modbus Unit ID: {counter_config.unit_id}")
    print(f"RTU Port: {rtu_config.port}")
    print(f"RTU Baudrate: {rtu_config.baudrate}")
    print(f"Error Threshold: 5 (matches Node-RED 'Errors > 5')")
    print()

    try:
        # Connect to the device
        print("Attempting to connect...")
        if not collector.connect():
            print("❌ Failed to connect to LKM144 device")
            print("Note: This example requires actual hardware or simulator")
            return

        print(f"✅ Connected via {collector.connection_type}")
        print()

        # Collect data
        print("Reading data from LKM144...")
        data = collector.collect_data()

        if data:
            print("✅ Data collection successful!")
            print()
            print("Sample Data (48 registers parsed into 24 fields):")
            print("-" * 50)
            
            # Display key measurements
            print(f"Time: {data['time']}")
            print(f"Date: {data['date']}")
            print(f"Active Energy: {data['energyActive']}")
            print(f"Reactive Energy: {data['energyReactive']}")
            print(f"Instantaneous Power: {data['instantaneousPower']}")
            print(f"Voltage L1: {data['voltageL1']}")
            print(f"Voltage L2: {data['voltageL2']}")
            print(f"Voltage L3: {data['voltageL3']}")
            print(f"Current L1: {data['currentL1']}")
            print(f"Current L2: {data['currentL2']}")
            print(f"Current L3: {data['currentL3']}")
            print(f"Power Factor: {data['powerFactor']}")
            print(f"Frequency: {data['frequency']}")
            print(f"Meter Number: {data['meterNumber']}")
            print()
            
            # Full data in JSON format
            print("Complete Data Structure:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
        else:
            print("❌ Failed to collect data")

    except KeyboardInterrupt:
        print("\n⏹️  Stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Always disconnect
        collector.disconnect()
        print("🔌 Disconnected")

if __name__ == "__main__":
    main()