import cv2
import numpy as np

from ..config import Colors


class DrawingManager:
    @staticmethod
    def draw_ball(img: np.ndarray, x: int, y: int, r: int) -> None:
        """
        Draws a circle on the image.

        Parameters
        ----------
        `img` : `np.ndarray`
            The image to draw the circle on.
        `x` : `int`
            The x-coordinate of the center of the circle.
        `y` : `int`
            The y-coordinate of the center of the circle.
        `r` : `int`
            The radius of the circle.
        """
        cv2.circle(img, (x, y), r, Colors.BALL_DRAWING_COLOR.value, 3)

    @staticmethod
    def draw_path_edges(img: np.ndarray, lines: np.ndarray) -> None:
        """
        Draws path edges lines in the image.

        Parameters
        ----------
        `img` : `np.ndarray`
            The image to draw the path edges lines on.
        `lines` : `np.ndarray`
            The lines to draw, coming from HoughLinesP.
        """
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(img, (x1, y1), (x2, y2), Colors.EDGE_DRAWING_COLOR.value, 3)

    @staticmethod
    def get_path_edges_image(img: np.ndarray, lines: np.ndarray) -> np.ndarray:
        """
        Generates a black image with white path edges lines drawn on it.

        Parameters
        ----------
        img : np.ndarray
            Frame of the captured window.
        lines : np.ndarray
            Lines detected using HoughLinesP.

        Returns
        -------
        np.ndarray
            Binary image with black background and white path edges lines.
        """
        lines_img = np.zeros_like(img)
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(lines_img, (x1, y1), (x2, y2), (255, 255, 255), 3)
        return lines_img

    @staticmethod
    def draw_fps(img: np.ndarray, fps: float) -> None:
        """
        Draws the FPS on the frame.

        Parameters
        ----------
        img : np.ndarray
            The frame to draw the FPS on.
        fps : float
            The FPS value to draw.
        """
        cv2.putText(img, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
