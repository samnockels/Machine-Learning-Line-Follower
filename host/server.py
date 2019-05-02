"""
Server which handles receiving pixy data from the rover,
making a prediction, and sending the prediction back to the rover
"""
import os
import sys
import ipc
import json
import time
import model
import pygame
import pickle
import pprint
import asyncio
import websockets

class Server:

    def __init__(self):

        # Uncomment Model that you want to run (Linear Regression/Neural Network)(Weighted Average, Matrix 3x3, Matrix 9x9)
        
        # Linear Regression
        self.model = model.Model("models/linear_regression/weighted_xy/", left_right=True)
        # self.model = model.Model("models/linear_regression/matrix_3x3/", left_right=True, matrix=True, matrix_size=3)
        # self.model = model.Model("models/linear_regression/matrix_9x9/", left_right=True, matrix=True, matrix_size=9)
        
        # Neural Network
        # self.model = model.Model("models/neural_network/weighted_xy/", left_right=True)
        # self.model = model.Model("models/neural_network/matrix_3x3/", left_right=True, matrix=True, matrix_size=3)
        # self.model = model.Model("models/neural_network/matrix_9x9/", left_right=True, matrix=True, matrix_size=9)

        # start server (for rover connection) on port 2000
        self.server = ipc.IPC()
        self.server.bind(12955)
        print("Connected to rover")
        self.frameCount = 0

        # run main loop
        self.run()

    def run(self):
        try:
            while True:
                self.frameCount += 1

                # 1. Receive data from robot
                message = self.server.recv()
                if not message:
                    break

                if message == "LOST_LINE":
                    print("Lost Line")
                else:
                    blocks = message
            
                    # 2. Make prediction
                    prediction = self.model.predict( blocks )

                    # 3. Send prediction back to robot
                    print(prediction)
                    self.server.send(prediction)
                
        finally:       
            # make sure to close the socket to the rover 
            self.close()    

    def close(self):
        if self.server:
            self.server.close()

    def __del__(self):
        self.close()
    
if __name__ == "__main__":
    s = Server()