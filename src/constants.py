"""
constants.py

This module contains all constants used throughout the project.

THIS FILE SHOULD NOT BE MODIFIED. ALL CONFIGURATION SHOULD BE DONE IN config.py.
"""

from enum import Enum


class Align(Enum):
    """
    Enum class for alignment types.
    """
    LEFT = 0
    CENTER = 1
    RIGHT = 2
    NONE = 3


class Direction(Enum):
    """
    Enum class for directions.
    """
    LEFT = 0
    RIGHT = 1
