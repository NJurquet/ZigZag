import numpy as np

from ..constants import Direction

from .actions import Actions
from ..utils import isometric_front_point


class ActionController:
    @staticmethod
    def decide_action(ball_pos: tuple[int, int], edge_lines: np.ndarray, frame_height: int, direction: Direction) -> bool:
        """
        Decides which action to perform based on the ball position and edge lines proximity.

        Parameters
        ----------
        `ball_position` : `tuple[int, int]`
            The (x, y) coordinates of the ball.
        `edge_lines` : `np.ndarray`
            Image of white edge lines detected in the frame.
        `frame_height` : `int`
            The height of the frame.
        `direction` : `Direction`
            The current ball direction.

        Returns
        -------
        `bool`
            `True` if the direction is changed; otherwise, `False`.
        """
        if not edge_lines:
            return False

        # Perform a click action if a line is present within the horizontal point region and isometric point region of the ball, and depending on the direction.
        horizontal_distance = int(frame_height * 60/1000)
        iso_x, iso_y = isometric_front_point(ball_pos, horizontal_distance, direction)
        if direction == Direction.LEFT:
            x, y = ball_pos[0] - horizontal_distance, ball_pos[1]

        elif direction == Direction.RIGHT:
            x, y = ball_pos[0] + horizontal_distance, ball_pos[1]
        else:
            raise ValueError(f"Invalid direction: {direction}. Expected LEFT or RIGHT.")

        # Check if any line is within a region of 10 pixels around the points on the edge_lines image
        region_size = 10
        if np.any(edge_lines[y-region_size:y+region_size, x-region_size:x+region_size] == 255) or np.any(edge_lines[iso_y-region_size:iso_y+region_size, iso_x-region_size:iso_x+region_size] == 255):
            Actions.click()
            return True

        return False
