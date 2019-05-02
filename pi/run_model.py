"""
Run a model on the robot, using an external machine

1. Send pixy data to machine with the model,
2. Receive the prediction 
3. Send prediction as input to both motors
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

        self.outputToMotors = motors
        self.lostLineStop = lostLineStop
        
        # Initialise pygame (in headless mode)
        pygame.init()
        os.environ["SDL_VIDEODRIVER"] = "dummy" # or maybe 'fbcon'
        screen = pygame.display.set_mode((1,1))

        # Initiialise Pixy
        print("Initialising Pixy...")
        self.pixy = get_blocks.Pixy()

        # Make connection to server (external machine with model)
        self.server = ipc.IPC()
        self.server.connect('samsmac', 12955)

        # run loop
        self.run()

    # loop which takes input from pixy and sends blocks to 
    # server before receiving prediction controlling motors
    def run(self):

        raw_input("Press any key to begin...")

        start_time = time.time()

        searching = False
        predictions = 0
        lost_line_count = 0
        time_without_blocks = -1
    
        while True:
            try:                
                # Poll Pixy for data
                blocks = self.pixy.poll()                
                print(str(len(blocks)) + " blocks")

                # blocks found?
                if len(blocks) > 0:

                    # reset vars
                    time_without_blocks = -1
                    searching = False
                    
                    # 1. Send blocks to server
                    self.server.send(blocks)

                    # 2. block until received prediction for motors
                    prediction = self.server.recv()
                    if not prediction:
                        break

                    # decode response
                    motor1 = prediction[0]
                    motor2 = prediction[1]

                    # just for protection 
                    # (model could output greater than 100 or less than -100)
                    if motor1 > 100:  motor1 = 100
                    if motor1 < -100: motor1 = -100
                    if motor2 > 100:  motor2 = 100
                    if motor2 < -100: motor2 = -100

                    # 3. write to motors
                    if self.outputToMotors:
                        explorerhat.motor.one.speed(motor1)
                        explorerhat.motor.two.speed(motor2)
                        predictions+=1 

                else:
                    # no blocks found

                    # stop rover from moving, 
                    # and display debugging message

                    if self.lostLineStop:
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

    print("USAGE: python3 run_mode.py <output to motors?> <stop or pause when line lost>")

    if len(sys.argv) > 1:
        runmotors=False
        lost_line_stop=False
        if sys.argv[1] == "true":
            runmotors = True
        if sys.argv[2] == "true":
            lost_line_stop=True
        Run_Model(runmotors,lost_line_stop)






