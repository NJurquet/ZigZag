import numpy as np


def crop_centered(frame: np.ndarray, center_ratio: float, crop_ratio: float) -> np.ndarray:
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
    `np.ndarray`
        The cropped frame.
    """
    crop_y1 = int(frame.shape[0] * (center_ratio - crop_ratio / 2))
    crop_y2 = int(frame.shape[0] * (center_ratio + crop_ratio / 2))
    return frame[crop_y1:crop_y2, :]
