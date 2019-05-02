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

        # init model
        
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

        # init pygame
        # pygame.init()
        # self.size = (700, 500)
        # self.screen = pygame.display.set_mode(self.size)
        # self.clock = pygame.time.Clock()

        # run main loop
        self.run()

    def run(self):
        try:
            while True:
                self.frameCount += 1

                # receive data from rover
                # print("Waiting for data")
                message = self.server.recv()
                if not message:
                    break

                if message == "LOST_LINE":
                    os.system('say "Lost Line"')
                else:
                    blocks = message
            
                    # make prediction
                    prediction = self.model.predict( blocks )

                    # send prediction back to rover 
                    print(prediction)
                    self.server.send(prediction)
                    
                    # pygame.event.get() # clear pygame queue
                    # self.screen.fill((255,255,255))
                    # # Draw an ellipse, using a rectangle as the outside boundaries
                    # pygame.draw.ellipse(self.screen, (0,0,0), [200, 200+(prediction[0]*150), 50, 50], 0)
                    # pygame.draw.ellipse(self.screen, (0,0,0), [400, 200+(prediction[1]*150), 50, 50], 0)
                    # pygame.draw.line(self.screen,(0,0,0),[300,200],[300+((prediction[0]*100)-(prediction[1]*100)),10])
                    # font = pygame.font.SysFont(None, 20)
                    # text = font.render(str(prediction),True, (0,0,0))
                    # self.screen.blit(text, (100,100))
                    # pygame.display.flip()
                
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