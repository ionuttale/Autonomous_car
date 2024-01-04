import cv2 as cv

class Capture_video(object):
    
    def __init__(self):
        self.video = cv.VideoCapture(0)
        self.video.set(cv.CAP_PROP_FPS, 60)
        
    def recording(self):
        return self.video.isOpened()
    
    def get_frame(self):
        ret, frame = self.video.read()
        return frame
    

        
