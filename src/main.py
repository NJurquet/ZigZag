import cv2
import os
import pyautogui
from time import time

from .config import WINDOW_NAME, VISION_EN, WINDOW_HEIGHT, PROCESSING_DELAY
from .constants import Align, Direction

from .capture.screen_capture import ScreenCapture
from .control.action_controller import ActionController, Actions
from .detection.detector import Detector
from .ui.drawing_manager import DrawingManager


def main():
    pyautogui.PAUSE = 0

    # Setup initial game start conditions
    ScreenCapture.set_window_pos_size(WINDOW_NAME, WINDOW_HEIGHT, Align.NONE)
    center = ScreenCapture.get_window_center(WINDOW_NAME)
    Actions.move_mouse_to(*center)
    Actions.click()

    direction = Direction.RIGHT
    START_TIME = time()
    balls_not_found = 0
    ball_detected = True
    fps_list = []
    loop_time = time()
    while True:
        frame = ScreenCapture.capture_window(WINDOW_NAME)

        # Start processing when game starts
        if time() - START_TIME >= PROCESSING_DELAY / 1000:
            x, y, r = Detector.detect_ball(frame)
            if (x, y, r) == (0, 0, 0):
                balls_not_found += 1
                if balls_not_found >= 10:
                    ball_detected = False
            else:
                balls_not_found = 0
            lines = Detector.detect_path_edges(frame)
            lines_img = DrawingManager.get_path_edges_image(frame, lines)

            if ball_detected:
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


if __name__ == "__main__":
    main()
