import cv2

from capture import ScreenCapture
from detection import Detector


def main():
    while True:
        frame = ScreenCapture.capture_window("BlueStacks App Player")
        Detector.detect_ball(frame)
        Detector.detect_path_edges(frame)

        cv2.imshow("Frame", frame)

        # Exit when 'Esc' key is pressed
        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    main()
