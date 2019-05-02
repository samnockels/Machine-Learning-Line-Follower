"""
Linear regression for each motor
"""

import json
import pickle
from sklearn import linear_model
from sklearn.model_selection import train_test_split

DATASET      = "3_lap_tank_raw"
PROJECT_BASE = "/Users/samnockels/projects/dissertation"

if __name__ == "__main__":

    with open('reduced.json', 'r') as f:
        data = json.load(f)

    # reduce so each entry is for one block only, 
    # & form into X and y
    X = []
    yLeft = []
    yRight = []
    for frame in data:
        for block in frame[0]:
            X.append([block[2],block[3]])
            yLeft.append(frame[1][0])
            yRight.append(frame[1][1])

    # fit model for left motor
    xTrain, xTest, yTrain, yTest = train_test_split(X, yLeft, test_size=0.1, shuffle=True)
    lm = linear_model.LinearRegression()
    lm.fit(xTrain, yTrain)
    print("Left Motor accuracy: " + str(lm.score(xTest,yTest)))

    # for model for right motor
    xTrain, xTest, yTrain, yTest = train_test_split(X, yRight, test_size=0.1, shuffle=True)
    rm = linear_model.LinearRegression()
    rm.fit(xTrain, yTrain)
    print("Right Motor accuracy: " + str(rm.score(xTest,yTest)))

    # save models
    with open( PROJECT_BASE+'/models/linearDouble/left.pkl', 'wb' ) as model:
        pickle.dump(lm, model)
    with open( PROJECT_BASE+'/models/linearDouble/right.pkl', 'wb' ) as model:
        pickle.dump(rm, model)
        
    print("Models Saved")
    