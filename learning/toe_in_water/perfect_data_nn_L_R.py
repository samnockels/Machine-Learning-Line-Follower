"""
Create 'perfect' data and use to train
linear model & nn model
"""
import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn import neural_network

# def form(x,y):
#     return (np.asarray(x)[:, np.newaxis], np.asarray(y))

# generate the 'perfect' data
xLeft,yLeft =   [[319,156,94,62,17,78,45,117,133,149,190,215,248,271,295],[0.94,0.95,0.04,0.07,0.06,0.08,0.07,0.2,0.48,0.72,0.97,0.97,0.96,0.96,0.95]] 
xRight,yRight = [[8,22,47,84,124,140,145,155,166,189,229,267,307,290,316],[0.94,0.94,0.91,0.91,0.89,0.79,0.57,0.37,0.18,0.09,0.06,0.04,0.03,0.04,0.02]] 
#
# train 2 linear models, one for each motor
#
def form(x,y):
    return (np.asarray(x)[:, np.newaxis], np.asarray(y))

# x -> left motor
nn = neural_network.MLPRegressor((5,5), activation="relu")
modelL = nn.fit(np.asarray(xLeft).reshape(-1,1),np.asarray(yLeft).reshape(-1,1)) 

# x -> right motor
nn = neural_network.MLPRegressor((5,5), activation="relu")
modelR = nn.fit(np.asarray(xRight).reshape(-1,1),np.asarray(yRight).reshape(-1,1)) 

# save models
with open( 'models/nn/perfect/left.pkl', 'wb' ) as model:
    pickle.dump(modelL, model)
    print("saved left model")
with open( 'models/nn/perfect/right.pkl', 'wb' ) as model:
    pickle.dump(modelR, model)
    print("saved right model")

if False:
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