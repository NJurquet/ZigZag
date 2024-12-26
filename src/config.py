"""
config.py

This module contains all configuration constants used throughout the project.
It serves as a centralized location for managing settings and values that are used in multiple parts of the application.
Change these config constants toc customize the behavior of the application.
"""

from enum import Enum

# CONFIGURATION ###################
WINDOW_NAME = "BlueStacks App Player"
VISION_EN = True  # Enable vision processing & image display
WINDOW_HEIGHT = 1200  # Target window height
PROCESSING_DELAY = 100  # Time in milliseconds before starting processing


# PARAMETERS ######################


class Colors(Enum):
    """
    Enum class for colors (in RGB) used in the project.
    """
    BALL_DRAWING_COLOR = (0, 0, 255)
    EDGE_DRAWING_COLOR = (0, 255, 0)
