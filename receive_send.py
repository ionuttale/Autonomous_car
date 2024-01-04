import cv2 as cv
import socket
import struct
import numpy as np

import lane_detect

# Inițializează serverul pentru a primi conexiuni de la Raspberry Pi
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.1.165', 5555)  # Adresa IP a laptopului și portul de comunicare
server_socket.bind(server_address)
server_socket.listen(1)

print("Așteptare conexiune...")

connection, client_address = server_socket.accept()

try:
    while True:
        # Primește dimensiunea imaginii de la Raspberry Pi
        data = connection.recv(4)
        if not data:
            break
        data_len = struct.unpack("!I", data)[0]

        # Primește imaginea propriu-zisă de la Raspberry Pi
        data = b""
        while len(data) < data_len:
            packet = connection.recv(data_len - len(data))
            if not packet:
                break
            data += packet

        # Decodifică imaginea și afișează-o pe laptop
        frame = cv.imdecode(np.frombuffer(data, dtype=np.uint8), cv.IMREAD_COLOR)
        
        __lane_detect = lane_detect.detect_lane_lines(frame)
        
        cv.imshow('Frame', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Curăță resursele și închide conexiunea
    connection.close()
    server_socket.close()
    cv.destroyAllWindows()
