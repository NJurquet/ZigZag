import cv2
from time import time

from config import WINDOW_NAME, VISION_EN, Align

from capture import ScreenCapture
from detection import Detector
from ui import DrawingManager


def main():
    ScreenCapture.set_window_pos_size(WINDOW_NAME, 640, Align.LEFT)

    fps_list = []
    loop_time = time()
    while True:
        frame = ScreenCapture.capture_window(WINDOW_NAME)
        # x, y, r = Detector.detect_ball(frame)
        # lines = Detector.detect_path_edges(frame)

        if VISION_EN:
            # DrawingManager.draw_ball(frame, x, y, r)
            # DrawingManager.draw_path_edges(frame, lines)

            # Compute and display average FPS
            fps = 1 / (time() - loop_time)
            loop_time = time()
            fps_list.append(fps)
            if len(fps_list) > 50:
                fps_list.pop(0)
            avg_fps = sum(fps_list) / len(fps_list)
            DrawingManager.draw_fps(frame, avg_fps)

            cv2.imshow("ZigZag Vision", frame)

        # Exit when 'q' key is pressed
        key = cv2.waitKey(1)
        if key == ord("q"):
            cv2.destroyAllWindows()
            break
        elif key == ord("s"):
            cv2.imwrite("screenshot.jpg", frame)


if __name__ == "__main__":
    main()
