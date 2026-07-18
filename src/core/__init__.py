"""
==========================================
Sigma AI Desktop Agent

Core Package
==========================================
"""

__version__ = "1.0.0"
__author__ = "Sigma"
__license__ = "Private"
__status__ = "Development"

from .agent import SigmaAgent
from .banner import show_banner
from .logger import logger

__all__ = [
    "SigmaAgent",
    "show_banner",
    "logger",
]