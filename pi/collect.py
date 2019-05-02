"""
Manage collecting data from onboard Pixy & PS4 controller
"""
import os
import sys
import time
import json
import pprint
import pickle
import explorerhat
sys.path.insert(0,'/home/pi/pixy/build/libpixyusb_swig/')
import get_blocks
import ps4controller

#
# main loop will poll pixy & controller
#
def run():
	data = []
	print("Initialising Pixy...")
	pixy = get_blocks.Pixy()
	print("Initialising PS4 Controller...")
	controller = ps4controller.PS4Controller(True)
	print("Starting 3")
	time.sleep(1)
	print("Starting 2")
	time.sleep(1)
	print("Starting 1")
	time.sleep(1)
	print("Go")
	i = 0
	while True:
		try:
			i += 1
			print(i)
			blocks = []
			motor1 = 0
			motor2 = 0
			xButton = 0

			# get blocks & controller input
			# !! the following must be called regularly in order to
			# !! clear both pixy & controller queue
			
			controllerData = controller.poll()
			axes = controllerData[0]
			xButton = controllerData[1]
			# print(blocks, axes)

			if xButton == 1:
				raise KeyboardInterrupt

			# control motors with controller data 
			if True:
				motor1 = axes[1] * -100
				motor2 = axes[4] * -100
			else:
				throttle = (axes[5]+1)*25
				direction = axes[3] * 75
				motor1 = throttle + direction
				motor2 = throttle - direction

			explorerhat.motor.one.speed(motor1)	
			explorerhat.motor.two.speed(motor2)

			# store data
			blocks = pixy.poll()
			frame = (blocks, [motor1, motor2]) 
			data.append( frame )

		except KeyboardInterrupt:

			explorerhat.motor.one.speed(0)	
			explorerhat.motor.two.speed(0)

			if( raw_input("Local save?").upper() == "Y" ):
				print("Saving data...")
				with open("data.json", 'w') as out:
					json.dump(data, out)
			print("Done")
			sys.exit(0)

if __name__ == '__main__':
	run()