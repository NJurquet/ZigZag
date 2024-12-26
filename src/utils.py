import numpy as np
import math

from .constants import Direction


def crop_centered(frame: np.ndarray, center_ratio: float, crop_ratio: float) -> tuple[np.ndarray, int, int]:
    """
    Crops the frame to a region at the center of the frame with a specified height ratio.

    Parameters
    ----------
    `frame` : `np.ndarray`
        The frame to crop.
    `center_ratio` : `float`
        The ratio of the height of the frame defining the center.
    `crop_ratio` : `float`
        The ratio of the height of the frame to crop.

    Returns
    -------
    `tuple[np.ndarray, int, int]`
        The cropped frame and the y-coordinates of the top and bottom of the cropped region.
    """
    crop_y1 = int(frame.shape[0] * (center_ratio - crop_ratio / 2))
    crop_y2 = int(frame.shape[0] * (center_ratio + crop_ratio / 2))
    return frame[crop_y1:crop_y2, :], crop_y1, crop_y2


def isometric_front_point(center_pos: tuple[int, int], horiz_dist: int, direction: Direction) -> tuple[int, int]:
    """
    Computes the position of the point isometrically in front of the ball in the specified direction based on the horizontal distance from the center.

    Parameters
    ----------
    center_pos : tuple[int, int]
        The (x, y) coordinates of the isometric square center position.
    horiz_dist : int
        The horizontal distance from the center of the isometric square.
    direction : Direction
        The direction of the point from the center (LEFT or RIGHT).

    Returns
    -------
    tuple[int, int]
        The (x, y) coordinates of the point isometrically in front of the ball.
    """
    x, y = center_pos
    iso_x, iso_y = 0, 0
    if direction == Direction.LEFT:
        iso_x = x - horiz_dist / 2
    elif direction == Direction.RIGHT:
        iso_x = x + horiz_dist / 2
    else:
        raise ValueError(f"Invalid direction: {direction}. Expected LEFT or RIGHT.")
    iso_y = y - horiz_dist * math.tan(math.radians(30)) / 2
    return int(iso_x), int(iso_y)
