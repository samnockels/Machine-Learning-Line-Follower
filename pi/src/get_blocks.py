from pixy import *
from ctypes import *
import pprint
import os

class Pixy():
    frame = 0
    blocks = None
    class Blocks (Structure):
        _fields_ = [ ("type", c_uint),
                     ("signature", c_uint),
                     ("x", c_uint),
                     ("y", c_uint),
                     ("width", c_uint),
                     ("height", c_uint),
                     ("angle", c_uint) ]
    def __init__(self):
        pixy_init()
        self.blocks = BlockArray(100)
    def poll(self):
        count = pixy_get_blocks(100, self.blocks)
        if count == 0:
            return []
        l = []
        for index in range (count):
            b = self.blocks[index]
            l.append([b.type,b.signature,b.x,b.y,b.width,b.height])
        return l
