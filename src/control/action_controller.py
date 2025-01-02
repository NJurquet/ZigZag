import cv2
import numpy as np

from ..config import VISION_EN
from ..constants import Direction

from .actions import Actions
from ..utils import isometric_front_point


class ActionController:
    @staticmethod
    def decide_action(ball_pos: tuple[int, int], edge_lines: np.ndarray, frame: np.ndarray, direction: Direction) -> bool:
        """
        Decides which action to perform based on the ball position and edge lines proximity.

        Parameters
        ----------
        `ball_pos` : `tuple[int, int]`
            The (x, y) coordinates of the ball.
        `edge_lines` : `np.ndarray`
            Image of white edge lines detected in the frame.
        `frame` : `np.ndarray`
            The frame for which the action is to be decided.
        `direction` : `Direction`
            The current ball direction.

        Returns
        -------
        `bool`
            `True` if the direction is changed; otherwise, `False`.
        """
        if edge_lines.size == 0 or ball_pos == (0, 0) or ball_pos[0] > frame.shape[1] or ball_pos[0] < 0:
            return False

        b, g, r = cv2.split(frame)

        # Perform a click action if a line is present within the horizontal point region and isometric point region of the ball, and depending on the direction.
        horizontal_distance = int(frame.shape[0] * 55/1000)
        iso_x, iso_y = isometric_front_point((ball_pos[0], ball_pos[1]), horizontal_distance, direction)
        region_size = 7
        if direction == Direction.LEFT:
            x = int(ball_pos[0]) - horizontal_distance
            x_low, x_high = x, x + region_size * 2
            iso_x_low, iso_x_high = iso_x - region_size, iso_x + region_size
        elif direction == Direction.RIGHT:
            x = int(ball_pos[0]) + horizontal_distance
            x_low, x_high = x - region_size * 2, x
            iso_x_low, iso_x_high = iso_x - region_size, iso_x + region_size
        else:
            raise ValueError(f"Invalid direction: {direction}. Expected LEFT or RIGHT.")
        y = ball_pos[1]
        y_low, y_high = y - region_size, y + region_size
        iso_y_low, iso_y_high = iso_y - region_size, iso_y + region_size

        if VISION_EN:
            cv2.circle(frame, (x, y), radius=6, color=(0, 0, 255), thickness=-1)
            cv2.circle(frame, (iso_x, iso_y), radius=6, color=(0, 0, 255), thickness=-1)

        # If the ball is at the edge of the screen, do not click.
        if x < 0 or x > frame.shape[1]:
            return False

        # Check if any line is within a region of 'region_size' pixels around the points on the edge_lines image, or if the white background is reached.
        line_on_front_point = np.any(edge_lines[y_low:y_high,
                                                x_low:x_high] == 255)
        line_on_iso_point = np.any(edge_lines[iso_y_low:iso_y_high,
                                              iso_x_low:iso_x_high] == 255)
        try:
            ws = 3
            front_white_background = np.any(
                b[y-ws:y+ws, x-ws:x+ws] == 255) and np.any(
                    g[y-ws:y+ws, x-ws:x+ws] == 255) and np.any(
                        r[y-ws:y+ws, x-ws:x+ws] == 255)
            iso_white_background = np.any(
                b[iso_y-ws:iso_y+ws, iso_x-ws:iso_x+ws] == 255) and np.any(
                    g[iso_y-ws:iso_y+ws, iso_x-ws:iso_x+ws] == 255) and np.any(
                        r[iso_y-ws:iso_y+ws, iso_x-ws:iso_x+ws] == 255)
            white_background_detected = front_white_background and iso_white_background
        except IndexError as e:
            print(f"IndexError: y={y}, x={x}, iso_y={iso_y}, iso_x={iso_x}, b.shape={b.shape}, frame.shape={frame.shape}")
            print(e)
            white_background_detected = True

        if (line_on_front_point and line_on_iso_point) or white_background_detected:
            Actions.click()
            return True

        return False
