from send_captured_video import Server
from setup.camera import Capture_video
from setup.controller import Controller

class Car(object):
    
    def __init__(self):
        self.server = Server()
        self.controller = Controller(20)
        self.video = Capture_video()
        
    def drive(self):
        
        self.server.connect()
        
        while(self.video.recording()):
            
            frame = self.video.get_frame()
            
            self.server.send_frame(frame)
            
            current_angle = self.controller.get_current_steering_angle()
            self.server.send(current_angle)
            
            new_angle = self.server.receive()
            self.controller.update_steering_angle(new_angle)
            
            #if abs(steering_angle-90) >= 15:
            #    self.controller.update_speed(1.5)
            #else:
            #    self.controller.update_speed(1.7)
            #self.controller.update_speed(0)
        
        
    def stop(self):
        self.controller.update_speed(0)
        self.controller.cleanup()
        
car = Car()
try:
    car.drive()
finally:
    car.stop()
