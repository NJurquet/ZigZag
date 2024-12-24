import cv2
import numpy as np


class Detector:
    @staticmethod
    def detect_ball(frame: np.ndarray) -> tuple[int, int, int]:
        # Find the ball considering a particular region of the frame with HoughCircles
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        cropped_frame = frame[100:400, 100:400]  # TODO: function from utils.py
        gray = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)

        height = gray.shape[0]
        min_dist = int(height * 15/100)
        min_dist = 1 if min_dist == 0 else min_dist
        min_radius = int(height * 8/100)
        min_radius = 1 if min_radius == 0 else min_radius
        max_radius = int(height * 12/100)
        max_radius = 1 if max_radius == 0 else max_radius

        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=min_dist,
                                   param1=20, param2=15,
                                   minRadius=min_radius, maxRadius=max_radius)
        circles = np.around(circles).astype(np.uint16)

        x, y, r = circles[0, 0, :] if circles is not None else (0, 0, 0)
        return x, y, r

    @staticmethod
    def detect_path_edges(frame: np.ndarray) -> list:
        ...

    @staticmethod
    def diamond_mask(frame: np.ndarray) -> np.ndarray:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array([153, 96, 175]), np.array([156, 255, 255]))
        mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=1)
        return mask


if __name__ == "__main__":
    frame = cv2.imread("images/game_sample_1.jpg")
    frame2 = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    cv2.imshow("ZigZag Vision", frame2)
    x, y, r = Detector.detect_ball(frame)
    print(f"Ball position: {x=}, {y=}, {r=}")

    cv2.waitKey(0)
    cv2.destroyAllWindows()
