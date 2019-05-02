"""
Create 'perfect' data and use to train
linear model & nn model
"""
import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from mlxtend.regressor import LinearRegression

# def form(x,y):
#     return (np.asarray(x)[:, np.newaxis], np.asarray(y))

# generate the 'perfect' data
X = np.linspace(0,320,50)
leftMotor = np.linspace(-0.1,1,50)
rightMotor = np.linspace(1,-0.1,50)

#
# train 2 linear models, one for each motor
#
def form(x,y):
    return (np.asarray(x)[:, np.newaxis], np.asarray(y))

# x -> left motor
lr = linear_model.LinearRegression()
modelL = lr.fit(X.reshape(-1,1),leftMotor.reshape(-1,1)) 

# x -> right motor
lr = linear_model.LinearRegression()
modelR = lr.fit(X.reshape(-1,1),rightMotor.reshape(-1,1)) 

# save models
os.makedirs('models/linear_regression/perfect', exist_ok=True)
with open( 'models/linear_regression/perfect/left.pkl', 'wb' ) as model:
    pickle.dump(modelL, model)
    print("saved left model")
with open( 'models/linear_regression/perfect/right.pkl', 'wb' ) as model:
    pickle.dump(modelR, model)
    print("saved right model")

if True:
    #
    # plot model predictions along with data
    #

    # plot perfect data for left motor
    plt.figure()
    plt.grid()
    plt.title("Perfect X Left Motor")
    ax = plt.gca()
    ax.set_xlim([0,320])
    ax.set_ylim([-1,1])
    plt.scatter(X,leftMotor)
    plt.plot([0,320],[modelL.predict([[0]])[0],modelL.predict([[320]])[0]] , color='red') 

    # plot perfect data for right motor
    plt.figure()
    plt.grid()
    plt.title("Perfect X Right Motor")
    ax = plt.gca()
    ax.set_xlim([0,320])
    ax.set_ylim([-1,1])
    plt.scatter(X,rightMotor)
    plt.plot([0,320],[modelR.predict([[0]])[0],modelR.predict([[320]])[0]] , color='red') 
    plt.show()