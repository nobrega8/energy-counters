"""
Lovato Counter Modules

This module provides interfaces for Lovato energy meters and counters.

Available counters:
- DMG210: Complete implementation with TCP and RTU support
- DMG800: (To be implemented)
- DMG6: (To be implemented)
"""

from .dmg210 import (
    CounterConfiguration,
    ModbusTCPConfiguration,
    ModbusRTUConfiguration,
    ModbusErrorManager,
    DMG210DataCollector
)

# TODO: Implement remaining counter classes and functions
# from .dmg800 import DMG800DataCollector
# from .dmg6 import DMG6DataCollector

__all__ = [
    'CounterConfiguration',
    'ModbusTCPConfiguration',
    'ModbusRTUConfiguration',
    'ModbusErrorManager',
    'DMG210DataCollector'
]