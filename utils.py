import cv2 as cv
import numpy as np
import math

import constants

def display_lines(frame, lines):
    lines_image = np.zeros_like(frame)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv.line(lines_image, (x1, y1), (x2, y2), constants.LANE_COLOR, constants.LANE_WIDTH)
    lines_image = cv.addWeighted(frame, 0.8, lines_image, 1, 1) 
    return lines_image                       

def display_heading_line(frame, steering_angle):
    heading_image = np.zeros_like(frame)
    height, width = frame.shape[:2]
    
    steering_angle_radian = steering_angle / 180.0 * math.pi
    x1 = int(width / 2)
    y1 = height
    x2 = int(x1 - height / 2 / math.tan(steering_angle_radian))
    y2 = int(height / 2)
    
    cv.line(heading_image, (x1, y1), (x2, y2), constants.HEADING_LINE_COLOR, constants.HEADING_LINE_WIDTH)
    heading_image = cv.addWeighted(frame, 0.8, heading_image, 1, 1)
    
    return heading_image