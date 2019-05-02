"""
'Run' a model on the rover
Send pixy data to server running on the machine with the model,
receive the prediction, and send prediction as input to both motors
"""
import os
import sys
import ipc
import time
import pprint
import explorerhat
sys.path.insert(0,'/home/pi/pixy/build/libpixyusb_swig/')
import get_blocks
import pygame

class Run_Model:

    def __init__(self, motors=False, lostLineStop=False):
        pygame.init()
        os.environ["SDL_VIDEODRIVER"] = "dummy" # or maybe 'fbcon'
        screen = pygame.display.set_mode((1,1))
        self.outputToMotors = motors
        self.lostLineStop = lostLineStop
        # init pixy
        print("Initialising Pixy...")
        self.pixy = get_blocks.Pixy()
        # make connection to server
        self.server = ipc.IPC()
        self.server.connect('samsmac', 12955)
        # run loop
        self.run()

    # loop which takes input from pixy and sends blocks to 
    # server before receiving prediction controlling motors
    def run(self):

        raw_input("Press any key to begin...")

        start_time = time.time()

        time_without_blocks = -1
        searching = False
        lost_line_count = 0
        predictions = 0

        while True:
            try:                
                # Poll pixy
                blocks = self.pixy.poll()                
                print(str(len(blocks)) + " blocks")

                # blocks found?
                if len(blocks) > 0:

                    # reset vars
                    time_without_blocks = -1
                    searching = False
                    
                    # send blocks to server
                    self.server.send(blocks)

                    # block until received prediction for motors
                    prediction = self.server.recv()
                    if not prediction:
                        break

                    # decode response
                    motor1 = prediction[0]
                    motor2 = prediction[1]

                    # just for protection
                    if motor1 > 100: motor1 = 100
                    if motor1 < -100: motor1 = -100
                    if motor2 > 100: motor2 = 100
                    if motor2 < -100: motor2 = -100

                    # write to motors
                    if self.outputToMotors:
                        explorerhat.motor.one.speed(motor1)
                        explorerhat.motor.two.speed(motor2)
                        predictions+=1 
                else:
                    
                    if self.lostLineStop:
                        # stop rover from moving, 
                        # and display debugging message
                        current_time = time.time()
                        if time_without_blocks == -1:
                            self.server.send("LOST_LINE")
                            print("Lost Line!")
                            lost_line_count += 1
                            print("Lost line count: " + str(lost_line_count))  
                            time_without_blocks = current_time
                            explorerhat.motor.one.speed(0)	
                            explorerhat.motor.two.speed(0)  
                            raw_input("Press any key to restart...")
                    else:
                        explorerhat.motor.one.speed(0)	
                        explorerhat.motor.two.speed(0)  
                        print("0 blocks")

            except KeyboardInterrupt:

                end_time = time.time()

                duration = end_time - start_time

                print("Done")
                print("Summary:")

                print(str(predictions) + " predictions made" )
                print(str(duration) + "s run time" )
                print("lost line " + str(lost_line_count) + " times")

                sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        runmotors=False
        lost_line_stop=False
        if sys.argv[1] == "true":
            runmotors = True
        if sys.argv[2] == "true":
            lost_line_stop=True
        Run_Model(runmotors,lost_line_stop)





