def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
"""
Create 'perfect' data and use to train
linear model & nn model
"""
import json
import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn import neural_network
from sklearn.model_selection import train_test_split

# def form(x,y):
#     return (np.asarray(x)[:, np.newaxis], np.asarray(y))

# generate the 'perfect' data
x,yLeft,yRight = [[7,13,18,29,46,55,67,74,81,83,92,100,106,113,117,121,127,135,138,141,143,146,150,155,159,171,172,176,184,189,194,202,207,222,230,241,271,275,287,307,322,317,295,283,270,268,253,245,233,249,265,266,263,260,250,234,219,207,197,188,179,172,169,166,161,154,149,143,137,134,125,105,98,83,71,59,46,38,29,9,29,23,23,35],[0.02,0.02,0.01,0.01,0,0,0.02,0.03,0.05,0.07,0.09,0.11,0.15,0.19,0.22,0.24,0.29,0.36,0.39,0.42,0.45,0.49,0.53,0.58,0.62,0.71,0.72,0.75,0.79,0.81,0.84,0.87,0.89,0.93,0.95,0.96,0.99,0.99,1,1,1,1,1,1,1,1,0.99,0.98,0.96,0.95,0.97,0.98,0.98,0.98,0.97,0.95,0.91,0.89,0.85,0.81,0.75,0.7,0.67,0.65,0.62,0.57,0.51,0.44,0.37,0.34,0.29,0.18,0.16,0.11,0.04,0.01,0,-0.01,0.05,0.02,0.05,0.03,0.03,0.02],[0.98, 0.98, 0.99, 0.99, 1, 1, 0.98, 0.97, 0.95, 0.93, 0.91, 0.89, 0.85, 0.81, 0.78, 0.76, 0.71, 0.64, 0.61, 0.58, 0.55, 0.51, 0.47, 0.42, 0.38, 0.29, 0.28, 0.25, 0.21, 0.19, 0.16, 0.13, 0.11, 0.07, 0.05, 0.04, 0.01, 0.01, 0, 0, 0, 0, 0, 0, 0, 0, 0.01, 0.02, 0.04, 0.05, 0.03, 0.02, 0.02, 0.02, 0.03, 0.05, 0.09, 0.11, 0.15, 0.19, 0.25, 0.3, 0.33, 0.35, 0.38, 0.43, 0.49, 0.56, 0.63, 0.66, 0.71, 0.82, 0.84, 0.89, 0.96, 0.99, 1, 1.01, 0.95, 0.98, 0.95, 0.97, 0.97, 0.98]] 

# plt.figure()
# ax = plt.subplot(121)
# ax.scatter(x,yLeft)
# ax = plt.subplot(122)
# ax.scatter(x,yRight)

X = np.asarray(x).reshape(-1,1)
y = []
for i in range(len(yLeft)):
    y.append([yLeft[i],yRight[i]])

xTrain, xTest, yTrain, yTest = train_test_split(X, y,test_size=0.4,shuffle=True)
print(len(xTrain),len(xTest),len(yTrain),len(yTest))
# save models
# with open( 'models/nn/perfect/singleModel.pkl', 'wb' ) as mod:
#     pickle.dump(model, mod)
#     print("saved model")

i = 1
plt.figure()
plt.grid()
plt.title("Perfect X Left vs Right motors")

# sweep over hyperparameters
print("activation, hidden layers, solver, score")

models = {}

for act in ["identity","logistic","tanh","relu"]:
    for hidden_layers in [(1),(5),(10),(1,1),(5,5),(10,10)]:    
        for solve in ["lbfgs", "sgd", "adam"]:
            try:
                nn = neural_network.MLPRegressor(hidden_layers, activation=act,solver=solve)
                model = nn.fit(xTrain,yTrain)
                score = model.score(xTest,yTest)
                if score > 0.9:
                    print(act,hidden_layers,solve,score) 
                    models[str(act)+str(hidden_layers)+str(solve)] = [model,score]
            except:
                pass

# show score results
y_pos = np.arange(len(models.keys()))
plt.bar(y_pos,    [ model[1] for model in models.values() ])
plt.xticks(y_pos, [ key for key in models.keys() ], rotation=90)

i = 1

for m in models:
    plt.title(m)
    model = models[m][0]
    #
    # plot model predictions along with data
    #
    yL = [model.predict([[e]])[0][0] for e in range(320)]
    yR = [model.predict([[e]])[0][1] for e in range(320)]

    # plot perfect data for left motor
    ax = plt.subplot(5,5,i)
    ax.set_xlim([0,320])
    ax.set_ylim([-1,1])
    plt.scatter([x for x in range(320)],yL,c='b')
    plt.scatter(x, yLeft, c='r')

    # plot perfect data for right motor
    ax = plt.subplot(5,5,i)
    ax.set_xlim([0,320])
    ax.set_ylim([-1,1])
    plt.scatter([x for x in range(320)],yR,c='b')
    plt.scatter(x, yRight, c='r')

    i+=1
plt.tight_layout()

plt.show()

with open('models/nn/perfect/singleModel.pkl', 'wb') as f:    
    nn = neural_network.MLPRegressor(hidden_layers, activation=act,solver=solve)
    model = nn.fit(xTrain,yTrain)
    pickle.dump(model,f)
    print('saved model')