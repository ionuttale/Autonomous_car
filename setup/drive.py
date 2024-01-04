import cv2 as cv
from controller import Controller
from lane_detect import Lane_detect
from camera import Capture_video

class Car(object):
    
    def __init__(self):
        self.current_wheel_angle = 90
        self.video = Capture_video()
        self.controller = Controller(20)
        self.lane_detect = Lane_detect()
        
    def drive(self):
        
        while(self.video.recording()):
            
            frame = self.video.get_frame()
            #cv.imshow('Original', frame)
            
            steering_angle = self.lane_detect.get_steering_angle(frame, self.controller.get_current_steering_angle())
            
            self.controller.update_steering_angle(steering_angle)

            #print(steering_angle)
            
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            #if abs(steering_angle-90) >= 15:
            #    self.controller.update_speed(1.5)
            #else:
            #    self.controller.update_speed(1.7)
            #self.controller.update_speed(0)
        
        self.controller.update_speed(0)
        self.controller.cleanup()

car= Car()
car.drive()