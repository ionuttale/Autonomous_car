import cv2 as cv
import math
import numpy as np
import utils

def detect_edges(frame):

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    #cv.imshow('hsv', hsv)    
    lower_white = np.array([0, 0, 212])
    upper_white = np.array([131, 255, 255])
        
    mask = cv.inRange(hsv, lower_white, upper_white)
        
    edges = cv.bitwise_and(frame, frame, mask = mask)
    edges = cv.Canny(frame, 200, 400)
        
    return edges
        
def add_mask(edges):
        
    mask = np.zeros_like(edges)
        
    height, width = edges.shape[:2]
        
    polygon = np.array([
                   [(0, height),(0, 250), (100, 220), (500, 220), (width, 250), (width, height)]
                   ])
        
    cv.fillPoly(mask, polygon, 255)
    region_of_interest = cv.bitwise_and(edges, mask)
    #cv.imshow('Reg', region_of_interest)
    return region_of_interest

def extract_lines_segments(region_of_interest):
        
    rho = 1
    angle = np.pi / 180
    min_threshold = 12
    lines_segments = cv.HoughLinesP(region_of_interest, rho, angle, min_threshold, np.array([]), minLineLength = 30, maxLineGap = 10)

    return lines_segments 
    
def make_points(frame, average):
    height, width = frame.shape[:2]
    slope, intercept = average
    y1 = height
    y2 = 200
    
    x1 = max(-width, min(2*width, int((y1-intercept)/slope)))
    x2 = max(-width, min(2*width, int((y2-intercept)/slope)))
    
    #print(x1, y1, x2, y2)

    return [[x1,y1,x2,y2]]  
    
def detect_lane_lines(frame):
        
    edges = detect_edges(frame)
    #cv.imshow('edges', edges)

    region_of_interest = add_mask(edges)

    cv.imshow('Region', region_of_interest)
        
    line_segments = extract_lines_segments(region_of_interest)
        
    lane_lines = []
            
    if line_segments is None:
        return lane_lines
            
    height, width = frame.shape[:2]
    left_fit = []
    right_fit = []
            
    boundary = 1/3
    right_region_boundary = width * (1-boundary)
    left_region_boundary = width * boundary
        
    for line_segment in line_segments:
                #print(line_segment)
        for x1, y1, x2, y2 in line_segment:
            if x1 == x2:
                continue
            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = fit[0]
                    #print(slope)
            intercept = fit[1]
            if slope < 0:
                if x1 < left_region_boundary and x2 < left_region_boundary:
                    left_fit.append((slope, intercept))
            else:
                if x1 > right_region_boundary and x2 > right_region_boundary:
                    right_fit.append((slope, intercept))

    if len(left_fit) > 0:
        left_fit_average = np.average(left_fit, axis=0)
        lane_lines.append(make_points(frame, left_fit_average))
                
    if len(right_fit) > 0:
        right_fit_average = np.average(right_fit, axis=0)
        lane_lines.append(make_points(frame, right_fit_average))
                
    return lane_lines
    
def compute_steering_angle(frame, lane_lines):
        
    height, width, _ = frame.shape
    if len(lane_lines) == 1:
        x1, _, x2, _ = lane_lines[0][0]
        #print(x1, x2)
        x_offset = x2 - x1
    else:
        left_x1, left_y1, left_x2, left_y2 = lane_lines[0][0]
        right_x1, right_y1, right_x2, right_y2 = lane_lines[1][0]
            
        camera_mid_offset_percent = 0
        mid = int(width / 2 * (1 + camera_mid_offset_percent))
        x_offset = (left_x2 + right_x2) / 2 - mid

        
    y_offset = height - 200
        
    angle_to_mid_radian = math.atan(x_offset / y_offset)
    angle_to_mid_deg = int(angle_to_mid_radian * 180.0 / math.pi)
    steering_angle = angle_to_mid_deg + 90
    return steering_angle
    
def stabilize_steering_angle(current_steering_angle, new_steering_angle, num_of_lane_lines):
        
    if num_of_lane_lines == 2:
        max_angle_deviation = 4.5
    else:
        max_angle_deviation = 0.009
        
    angle_deviation = new_steering_angle - current_steering_angle
        
    if abs(angle_deviation) > max_angle_deviation:
        stabilized_steering_angle = int(current_steering_angle + max_angle_deviation * angle_deviation / abs(angle_deviation))
    else:
        stabilized_steering_angle = new_steering_angle
    #print(stabilized_steering_angle)    
    return stabilized_steering_angle
    
def get_steering_angle(frame, current_steering_angle):
        
    lane_lines = detect_lane_lines(frame)
        
    if len(lane_lines) < 1 or len(lane_lines) > 2:
        return current_steering_angle
        
    lane_lines_frame = utils.display_lines(frame, lane_lines)
        
    steering_angle = compute_steering_angle(frame, lane_lines)

    if steering_angle == -1:
        return current_steering_angle

    final_steering_angle = stabilize_steering_angle(current_steering_angle, steering_angle, len(lane_lines))
        
    heading_line_frame = utils.display_heading_line(lane_lines_frame, final_steering_angle)
    
    cv.imshow('Frame', heading_line_frame)      
    
    return final_steering_angle