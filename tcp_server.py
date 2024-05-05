import socket
import cv2
import socket
import pickle
import numpy as np
import time

MAX_LENGTH = 65536
start_time = time.time()
interval   = 1
counter    = 0

def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        buffer   = conn.recv(MAX_LENGTH)
        frame    = np.frombuffer(buffer, dtype=np.uint8)
        frame    = frame.reshape(frame.shape[0], 1)
        frame    = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        frame    = cv2.flip(frame, 1)
        
        time.sleep(0.075)
        global counter
        global start_time
        counter += 1
        if (time.time() - start_time) > interval:
            print("FPS: ", counter / (time.time() - start_time))
            counter = 0
            start_time = time.time()
        if frame is not None and type(frame) == np.ndarray:
            cv2.imshow("Stream", frame)
            if cv2.waitKey(1) == 27:
                break

    conn.close()  # close the connection
    
server_program()