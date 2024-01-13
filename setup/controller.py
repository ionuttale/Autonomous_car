import picar

class Controller(object):
    
    def __init__(self, default_speed: int):
        
        self.__default_speed = default_speed
        picar.setup()
        
        self.servo_camera_lr = picar.Servo.Servo(1, bus_number=1)
        self.servo_camera_lr.write(105)
        
        self.servo_camera_ud = picar.Servo.Servo(2, bus_number=1)
        self.servo_camera_ud.write(70)
        
        self.__current_steering_angle = 90
        self.__curent_speed = 0
        
        self.back_wheels = picar.back_wheels.Back_Wheels()
        self.back_wheels.forward()
        self.back_wheels.speed = 0
        
        self.front_wheels = picar.front_wheels.Front_Wheels()
        #self.front_wheels.turning_offset = 0
        self.front_wheels.turn(90)
        
    def cleanup(self):
        self.back_wheels.speed = 0
        self.front_wheels.turn(90)
        self.servo_camera_ud.write(90)
        self.servo_camera_lr.write(90)
    
    def update_speed(self, ratio: float):
        speed = min(self.__default_speed * ratio, 100)
        self.back_wheels.speed = int(speed)
        self.__curent_speed = speed
        
    def update_steering_angle(self, angle: float):
        if angle < 50:
            angle = 50

        if angle > 130:
            angle = 130
        self.front_wheels.turn(angle)
        self.__current_steering_angle = angle

    def get_current_steering_angle(self):
        return self.__current_steering_angle
    
    def get_current_speed(self):
        return self.__curent_speed    