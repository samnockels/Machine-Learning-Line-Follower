import time
import json
import pandas as pd
"""
Helper file which provides methods for 
formatting the raw sensor data 
"""

"""
load a dataset
"""
def load( dataset ):
        with open('/Users/samnockels/projects/dissertation/data/'+dataset+'.json', 'r') as f: 
            data = json.load(f)
        return data

"""
Eliminates large groups of 
repeated frames 
"""
def reduce( data ):
    cache = []
    reduced = []
    for frame in data:
        if frame != cache:
            cache = frame
            reduced.append(frame)
    return reduced

"""
Flattens data 

From [[[block1,block2,block3],[left,right]], ...]

into [[block1,[left,right]], [block2,[left,right]] ]
"""
def flatten(data):
    flattened = []
    for frame in data:
        for block in frame[0]:
            flattened.append([[block], frame[1]])
    return flattened

"""
Extract features from raw data

independant: tuple of features to extract from blocks
             each entry will build a list of those features
             # example cases: 'xy' should  build list of [[x,y],[x,y]]
             #                'x' should build list of [[x],[x]]

dependant: tuple of depandant variables to extract (motor values)
             # example cases: 'l' should build list of [[left],[left]]
             # example cases: 'lr' should build list of [[left,right],[left,right]]
"""
def extract(data, independant=(), dependant=(), dependant_match_num_blocks=False):

    # data structure we will return
    variables = {"independant":{}, "dependant":{}}

    # build empty lists for each feature
    for variable in independant:
        variables['independant'][variable] = []
    for variable in dependant:
        variables['dependant'][variable] = []
    
    # iterate over dataset, extracting all required features
    for sample in data:
        blocks = sample[0]
        motors = sample[1]

        # extract independant variables
        for block in blocks:
            for variable in independant:
                if len(variable) == 1:
                    # example: 'x'  should  build list of [[x],[x]]
                    variables['independant'][variable].append([block[blockFeatureToIndex(variable)]])
                else:
                    # example: 'xy'  should  build list of [[x,y],[x,y]]
                    variables['independant'][variable].append([0]*len(variable))
                    for i, var in enumerate(variable):
                        variables['independant'][variable][-1][i] = block[blockFeatureToIndex(var)]

        if dependant_match_num_blocks:
            repeat = len(blocks)
        else:
            repeat = 1

        # extract dependant variables
        for variable in dependant:
            if len(variable) == 1:
                # example: 'l'  should  build list of [[l],[l]]
                for i in range(repeat):
                    variables['dependant'][variable].append([motors[motorFeatureToIndex(variable)]])
            else:
                for i in range(repeat):
                    # example: 'lr'  should  build list of [[l,r],[l,r]]
                    for i in range(len(blocks)):
                        variables['dependant'][variable].append([0]*len(variable))
                        for i, var in enumerate(variable):
                            variables['dependant'][variable][-1][i] = motors[motorFeatureToIndex(var)]

    return variables 

"""
Converts block feature name to index returned by get_blocks API
"""
def blockFeatureToIndex(attr):
    if not attr in ['t','s','x','y','w','h']:
        raise Exception('invalid attribute "'+str(attr)+'"')
    if attr == 't': return 0 # block type 
    if attr == 's': return 1 # block signature (colour)
    if attr == 'x': return 2 # block x coord
    if attr == 'y': return 3 # block y coord
    if attr == 'w': return 4 # block w width
    if attr == 'h': return 5 # block h height
    if attr == 'l': return 0 # left motor value
    if attr == 'r': return 1 # right motor value

"""
Converts motor name to index used 
"""
def motorFeatureToIndex(attr):
    if not attr in ['l','r']:
        raise Exception('invalid attribute "'+str(attr)+'"')
    if attr == 'l': return 0 # left motor value
    if attr == 'r': return 1 # right motor value

"""
Take weighted average x,y for every sample in dataset
"""
def weightedAvg(data,keep_motors=False):
    start_time = time.time()
    newDataset = []
    for frame in data:
        if keep_motors:
            newDataset.append([weightedAvgBlocks(frame[0]),frame[1]])
        else:
            newDataset.append(weightedAvgBlocks(frame[0]))
    print("Took " + str(time.time() - start_time) + " seconds to compute")
    return newDataset

"""
Given the vector of blocks from
pixy, return the weighted average
x,y - taking into account block size
"""
def weightedAvgBlocks(blocks):
    totalX = 0
    totalY = 0
    totalWeight = 0
    for block in blocks:  
        x = block[2]
        y = block[3]
        w = block[4]
        h = block[5]
        weight = w*h
        totalX += x * weight
        totalY += y * weight
        totalWeight += weight
    if totalWeight == 0: 
        totalWeight = 1
    return [totalX/totalWeight, totalY/totalWeight]
    
def toDataFrame(dataset):
    flattened = flatten(dataset)
    newData = []
    for sample in flattened:
        newSample = []
        newSample.append(sample[0][0][0]) # type
        newSample.append(sample[0][0][1]) # sig
        newSample.append(sample[0][0][2]) # x
        newSample.append(sample[0][0][3]) # y
        newSample.append(sample[0][0][4]) # w
        newSample.append(sample[0][0][5]) # h
        newSample.append(sample[1][0]) # left
        newSample.append(sample[1][1]) # right
        newData.append(newSample)
    df = pd.DataFrame(newData)
    df.columns = ["type","sig","x","y","w","h","left","right"]
    return df

def toDataFrameWeighted(weighted_avg_dataset):
    newData = []
    for sample in weighted_avg_dataset:
        newSample = []
        newSample.append(sample[0][0]) # weighted x
        newSample.append(sample[0][1]) # weighted y
        newSample.append(sample[1][0]) # left
        newSample.append(sample[1][1]) # right
        newData.append(newSample) 
    df = pd.DataFrame(newData)
    df.columns = ["x","y","left","right"]
    return df