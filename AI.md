# AI Project Usage

This document contains the prompts given to a particular AI and their corresponding responses.

## Prompts and Responses

For clarity, some part of the response code may be omitted and replaced with `...` if it's not relevant to the prompt or if the code has not changed.

### Window relative cropping

**Prompt:**

```
The game window has a title border at the top.
Update the `capture_window` method so this border is cropped from the image using the relative dimension of the window.
Also make sure it still works with win32 package and DPI awareness.
```

**Response:**

```py
import win32api
import win32con

class ScreenCapture:
    @staticmethod
    def capture_window(window_name: str) -> np.ndarray:

        ...

        # Get window dimensions
        left, top, right, bottom = win32gui.GetClientRect(hwnd)
        width = right - left
        height = bottom - top

        # Get the window's title bar height
        title_bar_height = win32api.GetSystemMetrics(win32con.SM_CYCAPTION)

        ...

        # Crop the title bar from the image
        img = img[title_bar_height:, :, :]
```

### Robust circle detection

**Prompt:**

```
The ball is detected with HoughCircles.
`adjust_circles()` is trying to find the best parameters for that function.
minDist, minRadius, maxRadius all depends on the size of the captured frame and on the PC resolution.
Using relative dimensions to the frame can be a good idea but prone to errors if the captured frame is not of the same size (eg. an emulator with a sidebar or extra space).
Find a way to make the circle detection reliable and robust.
```

**Response:**

```py
# adjust_detection.py
import cv2
import numpy as np


def nothing(x):
    pass


def adjust_circles(frame_path: str):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 300, 300)
    cv2.createTrackbar("Threshold1", "Trackbars", 270, 500, nothing)
    cv2.createTrackbar("Threshold2", "Trackbars", 400, 500, nothing)
    cv2.createTrackbar("Dp", "Trackbars", 1, 10, nothing)
    cv2.createTrackbar("MinDistRatio", "Trackbars", 10, 100, nothing)
    cv2.createTrackbar("Param1", "Trackbars", 50, 100, nothing)
    cv2.createTrackbar("Param2", "Trackbars", 18, 100, nothing)
    cv2.createTrackbar("MinRadiusRatio", "Trackbars", 2, 100, nothing)
    cv2.createTrackbar("MaxRadiusRatio", "Trackbars", 5, 100, nothing)

    while True:
        frame = cv2.imread(frame_path)
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        threshold1 = cv2.getTrackbarPos("Threshold1", "Trackbars")
        threshold2 = cv2.getTrackbarPos("Threshold2", "Trackbars")
        dp = cv2.getTrackbarPos("Dp", "Trackbars")
        dp = 1 if dp == 0 else dp

        height = gray.shape[0]
        min_dist_ratio = cv2.getTrackbarPos("MinDistRatio", "Trackbars") / 100
        min_radius_ratio = cv2.getTrackbarPos("MinRadiusRatio", "Trackbars") / 100
        max_radius_ratio = cv2.getTrackbarPos("MaxRadiusRatio", "Trackbars") / 100

        min_dist = int(height * min_dist_ratio)
        min_radius = int(height * min_radius_ratio)
        max_radius = int(height * max_radius_ratio)

        param1 = cv2.getTrackbarPos("Param1", "Trackbars")
        param1 = 1 if param1 == 0 else param1
        param2 = cv2.getTrackbarPos("Param2", "Trackbars")
        param2 = 1 if param2 == 0 else param2

        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=dp, minDist=min_dist,
                                   param1=param1, param2=param2, minRadius=min_radius, maxRadius=max_radius)
        if circles is not None:
            circles = np.around(circles).astype(np.uint16)
            for circle in circles[0, :]:
                x, y, r = circle
                cv2.circle(frame, (x, y), r, (0, 255, 0), 2)

        edges = cv2.Canny(frame, threshold1, threshold2)

        cv2.imshow("Circles", frame)
        cv2.imshow("Edges", edges)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    adjust_circles("images/game_sample_1.jpg")
```

### Multiplication & offset of lines coordinates

**Prompt:**

```
`detect_path_edges()` function resizes the frame and crops it for processing purposes.
The lines found with `HoughLinesP` have coordinates in the cropped & resized frame.
Give a solution to return lines in the initial frame coordinates in a optimized way (preferably without looping all the lines).
```

**Response:**

```py
import cv2
import numpy as np

from ..utils import crop_centered


class Detector:
    @staticmethod
    def detect_path_edges(frame: np.ndarray) -> np.ndarray:
        # Find edges lines considering a particular region of the frame with HoughLinesP
        resize_factor = 2
        frame_resized = cv2.resize(frame, (0, 0), fx=1/resize_factor, fy=1/resize_factor)
        cropped_frame, crop_y1, _ = crop_centered(frame_resized, 0.47, 0.10)
        hsv = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2HSV)

        lower_bound = np.array([137, 80, 140])
        upper_bound = np.array([156, 255, 255])
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=1)

        edges = cv2.Canny(cropped_frame, threshold1=175, threshold2=350)
        edges = cv2.bitwise_and(edges, edges, mask=cv2.bitwise_not(mask))

        height = hsv.shape[0]
        min_line_length = int(height * 25/100)
        min_line_length = 1 if min_line_length == 0 else min_line_length

        lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=20, minLineLength=min_line_length, maxLineGap=1)

        if lines is not None:
            # Convert lines to initial frame coordinates using matrix operations
            lines = lines.reshape(-1, 4)
            lines[:, [0, 2]] = lines[:, [0, 2]] * resize_factor
            lines[:, [1, 3]] = (lines[:, [1, 3]] + crop_y1) * resize_factor
            lines = lines.reshape(-1, 1, 4)

        return lines
```

### End of game when ball is lost

**Prompt:**

```
When the ball is not detected for 1s, it must have fall off the path and the game should be over.
The `detect_ball` method returns (0,0,0) if the ball is not detected.
Modify the code so when the ball is not detected for 1s, no actions are done anymore and the ball is not drawn (the processing window should still be present).
```

**Response:**

```py
# main.py
import cv2
import os
from time import time

from .config import WINDOW_NAME, VISION_EN, WINDOW_HEIGHT, PROCESSING_DELAY
from .constants import Align, Direction

from .capture.screen_capture import ScreenCapture
from .control.action_controller import ActionController, Actions
from .detection.detector import Detector
from .ui.drawing_manager import DrawingManager


def main():
    # Setup initial game start conditions
    ScreenCapture.set_window_pos_size(WINDOW_NAME, WINDOW_HEIGHT, Align.NONE)
    center = ScreenCapture.get_window_center(WINDOW_NAME)
    Actions.move_mouse_to(*center)
    Actions.click()

    direction = Direction.RIGHT
    START_TIME = time()
    last_ball_detected_time = time()
    fps_list = []
    loop_time = time()
    ball_detected = True

    while True:
        frame = ScreenCapture.capture_window(WINDOW_NAME)

        # Start processing when game starts
        if time() - START_TIME >= PROCESSING_DELAY / 1000:
            x, y, r = Detector.detect_ball(frame)
            if (x, y, r) == (0, 0, 0):
                if time() - last_ball_detected_time >= 1:
                    ball_detected = False
            else:
                last_ball_detected_time = time()
                ball_detected = True

            if ball_detected:
                lines = Detector.detect_path_edges(frame)
                lines_img = DrawingManager.get_path_edges_image(frame, lines)

                changed_dir = ActionController.decide_action((x, y), lines_img, frame, direction)
                if changed_dir:
                    direction = Direction.RIGHT if direction == Direction.LEFT else Direction.LEFT

        if VISION_EN:
            # Start drawing when game starts
            if time() - START_TIME >= PROCESSING_DELAY / 1000:
                if ball_detected:
                    DrawingManager.draw_ball(frame, x, y, r)
                DrawingManager.draw_path_edges(frame, lines)

            # Compute and display average FPS
            fps = 1 / (time() - loop_time)
            loop_time = time()
            fps_list.append(fps)
            if len(fps_list) > 50:
                fps_list.pop(0)
            avg_fps = sum(fps_list) / len(fps_list)
            DrawingManager.draw_fps(frame, avg_fps)

            cv2.imshow("ZigZag Vision", frame)

        key = cv2.waitKey(1)
        # Exit when 'q' key is pressed
        if key == ord("q"):
            cv2.destroyAllWindows()
            break
        elif key == ord("s"):
            cv2.imwrite(os.path.join("images", "screenshot.jpg"), frame)
```
