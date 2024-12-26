import cv2
import numpy as np

from ..utils import crop_centered


class Detector:
    @staticmethod
    def detect_ball(frame: np.ndarray) -> tuple[int, int, int]:
        # Find the ball considering a particular region of the frame with HoughCircles
        resize_factor = 2
        frame = cv2.resize(frame, (0, 0), fx=1/resize_factor, fy=1/resize_factor)
        cropped_frame, crop_y1, _ = crop_centered(frame, 0.47, 0.10)
        gray = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)

        height = gray.shape[0]
        min_dist = int(height * 30/100)
        min_dist = 1 if min_dist == 0 else min_dist
        min_radius = int(height * 13/100)
        min_radius = 1 if min_radius == 0 else min_radius
        max_radius = int(height * 15/100)
        max_radius = 1 if max_radius == 0 else max_radius

        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=min_dist,
                                   param1=20, param2=15,
                                   minRadius=min_radius, maxRadius=max_radius)

        x, y, r = 0, 0, 0
        if circles is not None:
            circles = np.around(circles).astype(np.uint16)
            x, y, r = circles[0, 0, :]

        return x * resize_factor, (y + crop_y1) * resize_factor, r * resize_factor

    @staticmethod
    def detect_path_edges(frame: np.ndarray) -> np.ndarray:
        # Find edges lines considering a particular region of the frame with HoughLinesP
        resize_factor = 2
        frame = cv2.resize(frame, (0, 0), fx=1/resize_factor, fy=1/resize_factor)
        cropped_frame, crop_y1, _ = crop_centered(frame, 0.47, 0.10)
        hsv = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2HSV)

        mask = Detector.diamond_mask(hsv)

        edges = cv2.Canny(cropped_frame, threshold1=175, threshold2=350)
        edges = cv2.bitwise_and(edges, edges, mask=cv2.bitwise_not(mask))

        height = hsv.shape[0]
        min_line_length = int(height * 25/100)
        min_line_length = 1 if min_line_length == 0 else min_line_length

        lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=20, minLineLength=min_line_length, maxLineGap=1)

        # Adjust the lines to the original frame (scale & offset) using numpy array / matrix operations
        if lines is not None:
            # Convert lines to initial frame coordinates using matrix operations
            lines = lines.reshape(-1, 4)
            lines[:, [0, 2]] = lines[:, [0, 2]] * resize_factor
            lines[:, [1, 3]] = (lines[:, [1, 3]] + crop_y1) * resize_factor
            lines = lines.reshape(-1, 1, 4)

        return lines

    @staticmethod
    def diamond_mask(frame: np.ndarray) -> np.ndarray:
        mask = cv2.inRange(frame, np.array([137, 80, 140]), np.array([156, 255, 255]))
        mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=1)
        return mask


if __name__ == "__main__":
    frame = cv2.imread("images/game_sample_1.jpg")
    frame2 = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    x, y, r = Detector.detect_ball(frame)
    cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
    print(f"Ball position: {x=}, {y=}, {r=}")
    cv2.imshow("ZigZag Vision", frame)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
