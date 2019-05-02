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

def run():

	# store collected data in this list
	data = []

	# initialise Pixy and Controller 
	print("Initialising Pixy...")
	pixy = get_blocks.Pixy()
	print("Initialising PS4 Controller...")
	controller = ps4controller.PS4Controller(True)

	# countdown 
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
			# !! must be called regularly in order to
			# !! clear both pixy & controller queue
			
			controllerData = controller.poll()
			axes = controllerData[0]
			xButton = controllerData[1]

			# if x button pressed, stop data collection
			if xButton == 1:
				raise KeyboardInterrupt

			# control motors with controller data 
			motor1 = axes[1] * -100
			motor2 = axes[4] * -100
			explorerhat.motor.one.speed(motor1)	
			explorerhat.motor.two.speed(motor2)

			# store data
			blocks = pixy.poll()
			frame = (blocks, [motor1, motor2]) 
			data.append( frame )

		except KeyboardInterrupt:

			# stop motors
			explorerhat.motor.one.speed(0)	
			explorerhat.motor.two.speed(0)

			# save collected data as 'data.json' 
			if( raw_input("Local save?").upper() == "Y" ):
				print("Saving data...")
				with open("data.json", 'w') as out:
					json.dump(data, out)
			print("Done")
			sys.exit(0)

## Entry point
if __name__ == '__main__':
	run()