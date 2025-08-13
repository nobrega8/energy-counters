"""
Nemotek Counters Library

A Python library for reading data from various electrical energy counters
including Carlo Gavazzi, Contrel, Diris, Lovato, RedZ, and Schneider devices.

Usage:
    import nemotek_counters
    from nemotek_counters import carlo_gavazzi
    from nemotek_counters.carlo_gavazzi import em530
"""

__version__ = "1.0.0"
__author__ = "Nemotek GTC"
__email__ = "info@nemotek.pt"

# Import submodules to make them available
from . import carlo_gavazzi
from . import contrel  
from . import diris
from . import lovato
from . import redz
from . import schneider

__all__ = [
    'carlo_gavazzi',
    'contrel', 
    'diris',
    'lovato',
    'redz', 
    'schneider'
]