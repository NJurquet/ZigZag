"""
config.py

This module contains all configuration constants and parameter constants used throughout the project.
It serves as a centralized location for managing settings and values that are used in multiple
parts of the application.
"""

from enum import Enum

# CONFIGURATION ###################
WINDOW_NAME = "BlueStacks App Player"
VISION_EN = True


# PARAMETERS ######################


class Colors(Enum):
    """
    Enum class for colors (in RGB) used in the project.
    """
    BALL_DRAWING_COLOR = (0, 0, 255)
    EDGE_DRAWING_COLOR = (0, 255, 0)


class Align(Enum):
    """
    Enum class for alignment types.
    """
    LEFT = 0
    CENTER = 1
    RIGHT = 2
    NONE = 3
