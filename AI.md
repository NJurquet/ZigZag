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
