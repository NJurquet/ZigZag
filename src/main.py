import cv2
from time import time

from config import WINDOW_NAME, VISION_EN

from capture import ScreenCapture
from detection import Detector
from ui import DrawingManager


def main():
    loop_time = time()
    while True:
        frame = ScreenCapture.capture_window(WINDOW_NAME)
        x, y, r = Detector.detect_ball(frame)
        lines = Detector.detect_path_edges(frame)

        if VISION_EN:
            DrawingManager.draw_ball(frame, x, y, r)
            DrawingManager.draw_path_edges(frame, lines)

            # Compute and display FPS
            fps = 1 / (time() - loop_time)
            DrawingManager.draw_fps(frame, fps)
            loop_time = time()

            cv2.imshow("ZigZag Vision", frame)

            # Exit when 'Esc' or 'q' key is pressed
            if cv2.waitKey(1) == 27 or cv2.waitKey(1) == ord("q"):
                cv2.destroyAllWindows()
                break


if __name__ == "__main__":
    main()
