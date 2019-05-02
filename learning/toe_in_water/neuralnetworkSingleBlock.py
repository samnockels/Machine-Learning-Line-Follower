"""
Train a neural network to map the relationship between pixy & PS4 controller data
"""
import pprint
import pickle
import json
import subprocess
import numpy as np
from sklearn import neural_network
from sklearn.model_selection import train_test_split

DATASET      = "direction_throttle"
MODEL_NAME   = "neuralNetworkRaw"
PROJECT_BASE = "/Users/samnockels/projects/dissertation"

def train(X,y):
    # split into training & testing
    xTrain, xTest, yTrain, yTest = train_test_split(X, y,test_size=0.4,shuffle=True)

    # nn with 6 neurons in single hidden layer
    nn = neural_network.MLPRegressor((6,6), activation='relu')
    nn.fit(xTrain,yTrain)
    print("Model Accuracy:" + str(nn.score(xTest,yTest)))
    return nn


def train_with_increasing_amounts( featureX, y ):
    # train models on increasing amounts of data
    for i in range(1,3):
        
        # take a portion of data to train with
        split = int(len(featureX)/i)

        # split into training & testing
        xTrain, xTest, yTrain, yTest = train_test_split(featureX[:split],y[:split],test_size=0.4,shuffle=True)

        # # # nn with 6 neurons in single hidden layer
        nn = neural_network.MLPRegressor((9,9), activation='relu')
        nn.fit(xTrain,yTrain)

        print()
        print()
        print("Using " + str(round(split/len(featureX), 2)*100) + "% of the data")
        # # validate model with test data
        print("Model Accuracy:" + str(nn.score(xTest,yTest)))

def save(nn):
    # save model
    with open( PROJECT_BASE+'/models/nn/'+MODEL_NAME+'.pkl', 'wb' ) as model:
        pickle.dump(nn, model)
    print("Model Saved to: ["+PROJECT_BASE+'/models/nn/'+MODEL_NAME+'.pkl'+"]")


if __name__ == "__main__":

    # get raw data
    raw = []
    with open( PROJECT_BASE+'/data/'+DATASET+'.json', 'rb' ) as f:
        raw = json.load(f)

    # form into x & y
    X = []
    y = []
    for frame in raw:
        X.append(frame[0][0])  # block 1 only
        y.append(frame[1])  # controller axes

    # train
    save( train(X, y) )
