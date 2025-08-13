"""
Carlo Gavazzi Counter Modules

This module provides interfaces for Carlo Gavazzi energy meters and counters.

Available counters:
- EM530: Energy meter with Modbus RTU communication
"""

from .em530 import (
    ConfiguracaoContador,
    ConfiguracaoModbus, 
    GestorErrosModbus,
    ColectorDadosEM530
)

__all__ = [
    'ConfiguracaoContador',
    'ConfiguracaoModbus',
    'GestorErrosModbus', 
    'ColectorDadosEM530'
]