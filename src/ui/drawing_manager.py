import cv2
import numpy as np

from config import Colors


class DrawingManager:
    @staticmethod
    def draw_ball(img: np.ndarray, x: int, y: int, r: int) -> None:
        cv2.circle(img, (x, y), r, Colors.BALL_DRAWING_COLOR.value, 4)

    @staticmethod
    def draw_path_edges(img: np.ndarray, lines: list) -> None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), Colors.EDGE_DRAWING_COLOR.value, 2)

    @staticmethod
    def draw_fps(img: np.ndarray, fps: float) -> None:
        cv2.putText(img, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
