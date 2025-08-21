#!/usr/bin/env python3
"""
Main entry point for the Energy Counters library.

This file demonstrates the usage of the energy_counters module.
"""

import sys

# Import energy_counters directly (no path tricks needed)
try:
    import energy_counters
    print(f"Successfully imported energy_counters v{energy_counters.__version__}")
    print(f"Available modules: {energy_counters.__all__}")
except ImportError as e:
    print(f"Failed to import energy_counters: {e}")
    print("Make sure the package is properly installed.")
    sys.exit(1)


def main():
    """
    Main function demonstrating usage of energy_counters library.
    
    This function shows how to import and use various counter modules
    from the energy_counters library.
    """
    print("\n=== Energy Counters Library Demo ===")
    print(f"Library version: {energy_counters.__version__}")
    print(f"Author: {energy_counters.__author__}")
    print(f"Email: {energy_counters.__email__}")
    
    print("\nAvailable counter modules:")
    for module_name in energy_counters.__all__:
        try:
            module = getattr(energy_counters, module_name)
            print(f"  ✓ {module_name}")
        except AttributeError:
            print(f"  ✗ {module_name} (not available)")
    
    print("\nExample configurations:")
    
    # Import configuration classes
    from energy_counters.common import (
        CounterConfiguration, 
        ModbusTCPConfiguration, 
        ModbusRTUConfiguration
    )
    
    # Example counter configuration
    counter_config = CounterConfiguration(
        counter_id=1,
        unit_id=100,
        counter_name="ExampleCounter",
        company_id="ExampleCompany"
    )
    
    # Example Modbus TCP configuration
    tcp_config = ModbusTCPConfiguration(
        host="192.168.1.100",
        port=502,
        timeout=4.0
    )
    
    # Example Modbus RTU configuration  
    rtu_config = ModbusRTUConfiguration(
        port="/dev/ttyUSB0",
        baudrate=9600,
        timeout=2.0
    )
    
    print(f"  Counter Config: {counter_config}")
    print(f"  TCP Config: {tcp_config}")
    print(f"  RTU Config: {rtu_config}")
    
    print("\nTo use specific counters, import them directly:")
    print("  from energy_counters.carlo_gavazzi import em530")
    print("  from energy_counters.contrel import ud3h")
    print("  from energy_counters.diris import a10")
    print("  from energy_counters.lovato import dmg210, dmg6")
    print("  from energy_counters.redz import lkm144")
    print("  from energy_counters.schneider import iem3255")


if __name__ == "__main__":
    main()