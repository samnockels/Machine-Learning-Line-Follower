"""
Helper module for extracting features from Pixy data 
during data collection
"""
import math
import pprint
import pickle
import json
import numpy as np
import time

class ExtractFeatures():
    """
    n - number of features to extract (n*n matrix)
    width/height - pixy camera resolution
    """
    def __init__(self, n, width = 320, height = 200):
        self.n = n
        self.w = width
        self.h = height

    """
    frame - take frame in the format [[type,sig,x,y,w,h],...]
    """
    def from_frame(self, frame):

        # init matrix of shape (n,n)
        matrix = []
        for i in range(self.n):
            matrix.append([])
            for j in range(self.n):
                matrix[i].append(0)        
                
        # take each block and update matrix
        for block in frame:

            block_x = float(block[2])
            block_y = float(block[3])
            block_w = float(block[4])
            block_h = float(block[5])
            # get all 4 (x,y) corner points
            # top left
            tl_x = block_x - (block_w / 2)
            tl_y = block_y - (block_h / 2)
            # top right
            tr_x = block_x + (block_w / 2)
            tr_y = block_y - (block_h / 2)
            # bottom left
            bl_x = block_x - (block_w / 2)
            bl_y = block_y + (block_h / 2)
            # bottom right
            br_x = block_x + (block_w / 2)
            br_y = block_y + (block_h / 2)
            # activate corner points
            tl = (math.floor((tl_x / self.w) * self.n), math.floor((tl_y / self.h) * self.n))
            tr = (math.floor((tr_x / self.w) * self.n), math.floor((tr_y / self.h) * self.n))
            bl = (math.floor((bl_x / self.w) * self.n), math.floor((bl_y / self.h) * self.n))
            br = (math.floor((br_x / self.w) * self.n), math.floor((br_y / self.h) * self.n))
            # print(tl, tr, bl, br)
            for col in range(tl[0], tr[0] + 1):
                for row in range(tl[1], bl[1] + 1):
                    if(col > self.n - 1): col = self.n - 1
                    if(row > self.n - 1): row = self.n - 1
                    if(col < 0): col = 0
                    if(row < 0): row = 0
                    matrix[row][col] = 1
        return matrix

    def from_data(self,data):
        start_time = time.time()
        X = []
        y = []
        for frame in data:
            blocks = frame[0]
            axes   = frame[1]
            features = np.asarray(self.from_frame(blocks)).flatten()
            X.append(features)
            y.append(axes)
        print("Took " + str(time.time() - start_time) + " seconds to compute")
        return (X,y)

    def from_json(self, jsonFilePath, extractedFilePath):

        extractedData = []

        with open(jsonFilePath, 'r') as f:
            data = json.load(f)

        for frame in data:
            blocks = frame[0]
            axes   = frame[1]
            print(blocks)
            features = self.from_frame(blocks)
            print([features, axes])
            extractedData.append([features, axes])
        
        with open(extractedFilePath, 'w') as f:
            json.dump(extractedData, f)

        return extractedData

        
if __name__ == "__main__":
    # with open("data/1_lap_tank_raw.pkl") as f:
    #     data = pickle.load(f)   
    extract = ExtractFeatures(2)
    # extract.from_json('data/3_lap_tank_raw_b.json', 'extracted.json')
    print('done')
    pprint.pprint(extract.from_frame([[0, 1, 220, 122, 193, 153], [0, 1, 101, 164, 5, 33], [0, 1, 96, 186, 4, 7]]), width=40)
