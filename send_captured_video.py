import socket
import struct
import cv2 as cv

class Server(object):
    
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self):
        
        server_address = ('your_laptop_ip', 5555)  # Adresa IP și portul la care laptopul ascultă conexiuni
        self.server_socket.connect(server_address) 
    
    def send_frame(self, frame):
        encode_param = [int(cv.IMWRITE_JPEG_QUALITY), 90]
        _, img_encoded = cv.imencode('.jpg', frame, encode_param)
        data = img_encoded.tobytes()
        
        self.server_socket.sendall(struct.pack("!I", len(data)))
        self.server_socket.sendall(data)
    
    def send(self, data):
        data = int(data)
        data = str(data)
        self.server_socket.sendall(data.encode())
        
    def receive(self):
        angle = float(self.server_socket.recv(1024).decode())
        return angle
    
    def close(self):
        self.server_socket.close()
           
        
