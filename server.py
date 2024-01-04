import cv2 as cv
import socket
import struct
import numpy as np
import lane_detect
import utils

class Server(object):
    
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def start_server(self):
        server_address = ('192.168.1.165', 5555)  # Adresa IP a laptopului și portul de comunicare
        self.server_socket.bind(server_address)
        self.server_socket.listen(1)
        print('Connecting...')
        self.connection, self.client_address = self.server_socket.accept()
        
    def receive_frame(self):
        data = self.connection.recv(4)
        if not data:
            return False
        data_len = struct.unpack("!I", data)[0]

        # Primește imaginea propriu-zisă de la Raspberry Pi
        data = b""
        while len(data) < data_len:
            packet = self.connection.recv(data_len - len(data))
            if not packet:
                break
            data += packet

        # Decodifică imaginea și afișează-o pe laptop
        self.frame = cv.imdecode(np.frombuffer(data, dtype=np.uint8), cv.IMREAD_COLOR)
        
        return True
    
    def receive_data(self):
        self.data = self.connection.recv(1024).decode()
        self.data = float(self.data)
        #print(self.data)
    
    def send(self, data):
        data = str(data)
        self.connection.sendall(data.encode())
        
    def process_data(self):
        edges = lane_detect.detect_edges(self.frame)
        
        cv.imshow(edges)
    
    def close(self):
        self.server_socket.close()
        self.connection.close()
        cv.destroyAllWindows()
        
server = Server()
server.start_server()

try:
    while server.receive_frame() == True:
        receive = server.receive_data()
        angle = lane_detect.get_steering_angle(server.frame, server.data)
        server.send(angle)
        
        cv.imshow('Frame', server.frame)
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        
    
finally:
    server.close()