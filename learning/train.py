"""
All training is done here

split     - develops 2 models, one for each motor
combined  - develops 1 model for both motors
"""
import os
import json
import pickle
import pprint
import numpy as np
from sklearn import linear_model
from sklearn import neural_network
from sklearn.model_selection import cross_validate
from sklearn.model_selection import train_test_split

class Train:

    """
    Linear regression model (split)
    """
    def linear_regression_split(self,X,yLeft,yRight):

        # fit model for left motor
        xTrain, xTest, yTrain, yTest = train_test_split(X, yLeft, test_size=0.4, shuffle=True)
        lm = linear_model.LinearRegression()
        lm.fit(xTrain, yTrain)
        # score left motor model
        accuracy = lm.score(xTest,yTest)
        cval = cross_validate(lm,X,yLeft)
        for score in cval: cval[score] = cval[score].tolist()
        leftScore = {"model":"Left Motor","accuracy":accuracy,"cross_validation":cval}

        # fit model for right motor
        xTrain, xTest, yTrain, yTest = train_test_split(X, yRight, test_size=0.4, shuffle=True)
        rm = linear_model.LinearRegression()
        rm.fit(xTrain, yTrain)
        # score right motor model
        accuracy = rm.score(xTest,yTest)
        cval = cross_validate(rm,X,yRight)
        for score in cval: cval[score] = cval[score].tolist()
        rightScore = {"model":"Right Motor","accuracy":accuracy,"cross_validation":cval}

        # return models
        return (lm,rm,[leftScore,rightScore])

    """
    Linear model using SGD (split)
    """
    def gradient_descent_split(self,X,yLeft,yRight):
        
        maxIterations = np.ceil(10**6 / len(yLeft))

        # fit model for left motor
        xTrain, xTest, yTrain, yTest = train_test_split(X, yLeft, test_size=0.4, shuffle=False)
        lm = linear_model.SGDRegressor(max_iter=maxIterations)
        lm.fit(xTrain,yTrain)
        leftScore = lm.score(xTest,yTest)
        print("left score", leftScore, lm.n_iter_)

        xTrain, xTest, yTrain, yTest = train_test_split(X, yRight, test_size=0.4, shuffle=False)
        rm = linear_model.SGDRegressor(max_iter=maxIterations)
        rm.fit(xTrain,yTrain)
        rightScore = rm.score(xTest,yTest)
        print("right score",rightScore, rm.n_iter_)

        return (lm,rm,[leftScore,rightScore])

    """
    Neural Network (split)
    """    
    def neural_network_split(self,X,yLeft,yRight,hidden_layers=(5,5),act="relu",solve="sgd"):

        # fit left model
        xTrain, xTest, yTrain, yTest = train_test_split(X, yLeft, test_size=0.4, shuffle=True)
        nn = neural_network.MLPRegressor(hidden_layers, activation=act, solver=solve)
        lm = nn.fit(xTrain,yTrain)
        leftScore = lm.score(xTest,yTest)

        # fit right model
        xTrain, xTest, yTrain, yTest = train_test_split(X, yRight, test_size=0.4, shuffle=True)
        nn = neural_network.MLPRegressor(hidden_layers, activation=act, solver=solve)
        rm = nn.fit(xTrain,yTrain)
        rightScore = rm.score(xTest,yTest) 

        return (lm,rm,[leftScore,rightScore])

    """
    Neural Network (combined)
    """    
    def neural_network_combined(self,X,y,hidden_layers=(5,5),act="relu",solve="sgd"):

        xTrain, xTest, yTrain, yTest = train_test_split(X, y, test_size=0.4, shuffle=True)
        
        nn = neural_network.MLPRegressor(hidden_layers, activation=act, solver=solve)
        model = nn.fit(xTrain,yTrain)
        score = model.score(xTest,yTest)
        print(act,hidden_layers,solve,score) 

        return (model, score)
                        