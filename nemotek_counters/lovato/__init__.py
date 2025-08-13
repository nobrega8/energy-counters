"""
Lovato Counter Modules

This module provides interfaces for Lovato energy meters and counters.

Available counters:
- DMG210: Complete implementation with TCP and RTU support
- DMG800: (To be implemented)
- DMG6: (To be implemented)
"""

from .dmg210 import (
    ConfiguracaoContador,
    ConfiguracaoModbusTCP,
    ConfiguracaoModbusRTU,
    GestorErrosModbus,
    ColectorDadosDMG210
)

# TODO: Implement remaining counter classes and functions
# from .dmg800 import ColectorDadosDMG800
# from .dmg6 import ColectorDadosDMG6

__all__ = [
    'ConfiguracaoContador',
    'ConfiguracaoModbusTCP',
    'ConfiguracaoModbusRTU',
    'GestorErrosModbus',
    'ColectorDadosDMG210'
]