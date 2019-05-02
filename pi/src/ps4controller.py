#! /usr/bin/env python

import os
import pprint
import pygame

class PS4Controller():
    
    controller = None
    axis_data  = None
    pp = pprint.PrettyPrinter(width=10)

    # initialise pygame
    def __init__(self, headless = False):     
        # if no display
        if( headless ):    
            os.environ["SDL_VIDEODRIVER"] = "dummy" # or maybe 'fbcon'
            screen = pygame.display.set_mode((1,1))
        pygame.display.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        # initialise axis cache
        self.axis_data = []
        for i in range(self.controller.get_numaxes()):
            self.axis_data.append(0)
            
    # poll and cache axis data 
    def poll(self):      
        pygame.event.get()
        for axis in range(self.controller.get_numaxes()):
            self.axis_data[axis] = round(self.controller.get_axis(axis),2)
        return (self.axis_data, self.controller.get_button(0))
        
    # print cached axis data to screen
    def out(self):
        os.system('clear')
        self.pp.pprint(self.axis_data)

if __name__ == '__main__':
    ps4 = PS4Controller()