import cv2


class Detector:
    @staticmethod
    def detect_ball(frame) -> tuple[int, int, int]:
        ...

    @staticmethod
    def detect_path_edges(frame) -> list:
        ...
