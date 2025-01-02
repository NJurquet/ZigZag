import cv2
import numpy as np
import math

from ..constants import Direction

from .detector import Detector
from ..utils import isometric_front_point


def nothing(x):
    pass


def adjust_diamonds(frame_path: str):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 400, 420)
    cv2.createTrackbar("Threshold1", "Trackbars", 175, 500, nothing)
    cv2.createTrackbar("Threshold2", "Trackbars", 350, 500, nothing)
    cv2.createTrackbar("Tresh lines", "Trackbars", 20, 150, nothing)
    cv2.createTrackbar("minLineLength", "Trackbars", 25, 100, nothing)
    cv2.createTrackbar("maxLineGap ", "Trackbars", 1, 100, nothing)
    cv2.createTrackbar("HueMin", "Trackbars", 137, 255, nothing)
    cv2.createTrackbar("HueMax", "Trackbars", 156, 255, nothing)
    cv2.createTrackbar("SatMin", "Trackbars", 80, 255, nothing)
    cv2.createTrackbar("SatMax", "Trackbars", 255, 255, nothing)
    cv2.createTrackbar("ValMin", "Trackbars", 140, 255, nothing)
    cv2.createTrackbar("ValMax", "Trackbars", 255, 255, nothing)

    while True:
        frame = cv2.imread(frame_path)
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        # Calculate the crop region (center x% of the frame)
        crop_ratio = 0.10
        crop_y1 = int(frame.shape[0] * (0.47 - crop_ratio / 2))
        crop_y2 = int(frame.shape[0] * (0.47 + crop_ratio / 2))
        cropped_frame = frame[crop_y1:crop_y2, :]  # Crop the frame to the center x%
        hsv = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2HSV)

        height = hsv.shape[0]
        threshold1 = cv2.getTrackbarPos("Threshold1", "Trackbars")
        threshold2 = cv2.getTrackbarPos("Threshold2", "Trackbars")
        tresh_lines = cv2.getTrackbarPos("Tresh lines", "Trackbars")
        min_line_length_ratio = cv2.getTrackbarPos("minLineLength", "Trackbars") / 100
        min_line_length = int(height * min_line_length_ratio)
        min_line_length = 1 if min_line_length == 0 else min_line_length
        max_line_gap = cv2.getTrackbarPos("maxLineGap ", "Trackbars")
        hue_min = cv2.getTrackbarPos("HueMin", "Trackbars")
        hue_max = cv2.getTrackbarPos("HueMax", "Trackbars")
        sat_min = cv2.getTrackbarPos("SatMin", "Trackbars")
        sat_max = cv2.getTrackbarPos("SatMax", "Trackbars")
        val_min = cv2.getTrackbarPos("ValMin", "Trackbars")
        val_max = cv2.getTrackbarPos("ValMax", "Trackbars")

        lower_bound = np.array([hue_min, sat_min, val_min])
        upper_bound = np.array([hue_max, sat_max, val_max])
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=1)

        edges = cv2.Canny(cropped_frame, threshold1, threshold2)
        edges = cv2.bitwise_and(edges, edges, mask=cv2.bitwise_not(mask))

        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, tresh_lines, minLineLength=min_line_length, maxLineGap=max_line_gap)

        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(frame, (x1, y1 + crop_y1), (x2, y2 + crop_y1), (0, 255, 0), 2)

        # Draw a rectangle on the initial frame to represent the processing crop
        cv2.rectangle(frame, (0, crop_y1), (frame.shape[1], crop_y2), (255, 0, 0), 2)

        cv2.imshow("Frame", frame)
        cv2.imshow("Mask", mask)
        cv2.imshow("Canny", edges)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


def adjust_circles(frame_path: str):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 400, 300)
    cv2.createTrackbar("Threshold1", "Trackbars", 200, 500, nothing)
    cv2.createTrackbar("Threshold2", "Trackbars", 400, 500, nothing)
    cv2.createTrackbar("Dp", "Trackbars", 1, 10, nothing)
    cv2.createTrackbar("MinDist", "Trackbars", 30, 100, nothing)
    cv2.createTrackbar("Param1", "Trackbars", 20, 100, nothing)
    cv2.createTrackbar("Param2", "Trackbars", 15, 100, nothing)
    cv2.createTrackbar("MinRadius", "Trackbars", 13, 100, nothing)
    cv2.createTrackbar("MaxRadius", "Trackbars", 15, 100, nothing)

    while True:
        frame = cv2.imread(frame_path)
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        # Calculate the crop region (center x% of the frame)
        crop_ratio = 0.10
        crop_y1 = int(frame.shape[0] * (0.47 - crop_ratio / 2))
        crop_y2 = int(frame.shape[0] * (0.47 + crop_ratio / 2))
        cropped_frame = frame[crop_y1:crop_y2, :]  # Crop the frame to the center x%
        gray = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)

        threshold1 = cv2.getTrackbarPos("Threshold1", "Trackbars")
        threshold2 = cv2.getTrackbarPos("Threshold2", "Trackbars")
        dp = cv2.getTrackbarPos("Dp", "Trackbars")
        dp = 1 if dp == 0 else dp

        height = gray.shape[0]
        min_dist_ratio = cv2.getTrackbarPos("MinDist", "Trackbars") / 100
        min_dist_ratio = 0.01 if min_dist_ratio == 0 else min_dist_ratio
        min_radius_ratio = cv2.getTrackbarPos("MinRadius", "Trackbars") / 100
        min_radius_ratio = 0.01 if min_radius_ratio == 0 else min_radius_ratio
        max_radius_ratio = cv2.getTrackbarPos("MaxRadius", "Trackbars") / 100
        max_radius_ratio = 0.01 if max_radius_ratio == 0 else max_radius_ratio

        min_dist = int(height * min_dist_ratio)
        min_dist = 1 if min_dist == 0 else min_dist
        min_radius = int(height * min_radius_ratio)
        min_radius = 1 if min_radius == 0 else min_radius
        max_radius = int(height * max_radius_ratio)
        max_radius = 1 if max_radius == 0 else max_radius

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
                cv2.circle(frame, (x, y + crop_y1), r, (0, 255, 0), 2)

        edges = cv2.Canny(frame, threshold1, threshold2)
        # Draw a rectangle on the initial frame to represent the processing crop
        cv2.rectangle(frame, (0, crop_y1), (frame.shape[1], crop_y2), (255, 0, 0), 2)

        cv2.imshow("Circles", frame)
        cv2.imshow("Edges", edges)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


def adjust_ball_edge_distance(frame_path: str):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 400, 100)
    cv2.createTrackbar("hrzt dist", "Trackbars", 60, 100, nothing)

    while True:
        frame = cv2.imread(frame_path)
        frame_resized = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        x, y, r = Detector.detect_ball(frame)
        x, y = x // 2, y // 2 + r//2

        height = frame_resized.shape[0]
        horizontal_distance = cv2.getTrackbarPos("hrzt dist", "Trackbars") / 1000
        horizontal_distance = int(height * horizontal_distance)
        # compute isometric position with horizontal distance
        iso_x_left, iso_y = isometric_front_point((x, y), horizontal_distance, Direction.LEFT)
        iso_x_right, iso_y = isometric_front_point((x, y), horizontal_distance, Direction.RIGHT)

        # Right edge distance
        cv2.circle(frame_resized, (int(x + horizontal_distance), int(y)), radius=3, color=(0, 0, 255), thickness=-1)
        cv2.circle(frame_resized, (iso_x_right, iso_y), radius=3, color=(0, 0, 255), thickness=-1)
        # Left edge distance
        cv2.circle(frame_resized, (int(x - horizontal_distance), int(y)), radius=3, color=(0, 0, 255), thickness=-1)
        cv2.circle(frame_resized, (iso_x_left, iso_y), radius=3, color=(0, 0, 255), thickness=-1)

        cv2.circle(frame_resized, (x, y - r//2), r//2, (0, 255, 0), 2)

        cv2.imshow("Frame", frame_resized)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    # adjust_diamonds("images/game_sample_1.jpg")
    # adjust_diamonds("images/game_sample_2.jpg")
    # adjust_diamonds("images/game_sample_3.jpg")
    # adjust_circles("images/game_sample_1.jpg")
    # adjust_circles("images/game_sample_2.jpg")
    # adjust_circles("images/game_sample_3.jpg")
    adjust_ball_edge_distance("images/game_sample_2.jpg")
