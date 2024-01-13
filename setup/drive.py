import cv2 as cv
from controller import Controller
import lane_detect
from camera import Capture_video

class Car(object):
    
    def __init__(self):
        self.current_wheel_angle = 90
        self.video = Capture_video()
        self.controller = Controller(20)
        self.lane_detect = lane_detect
        
    def drive(self):
        
        while(self.video.recording()):
            
            frame = self.video.get_frame()
            #cv.imshow('Original', frame)
            
            steering_angle = self.lane_detect.get_steering_angle(frame, self.controller.get_current_steering_angle())
            
            self.controller.update_steering_angle(steering_angle)

            #print(steering_angle)
            
            if steering_angle > 105 or steering_angle < 75:
                self.controller.update_speed(1.7)
            else:
                self.controller.update_speed(2.5)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            
            #self.controller.update_speed(0)
        
        self.controller.update_speed(0)
        self.controller.cleanup()

car= Car()
car.drive()