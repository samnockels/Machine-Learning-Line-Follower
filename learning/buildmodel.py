import os
import pickle
import format
from pandas import DataFrame
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import extract_features

from sklearn.model_selection import learning_curve
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def load_dataset(datasets, reduce_data=False, take_weighted_average=False, extract=False, num_features=3):

    if take_weighted_average and extract:
        raise Exception("Cannot take weighted average and extract features")

    # Load datasets here 
    if type(datasets) == str:
        dataset = format.load(datasets)
    else:
        dataset = []
        for i, d in enumerate(datasets):
            data = format.load(d)
            print("Dataset " + str(i+1) + ", " + str(len(data)) + " samples")
            dataset += data

    if reduce_data:
        dataset = format.reduce(dataset) 

    # preprocess? or use raw data?
    if take_weighted_average:
        # weighted average x,y coord
        df = format.toDataFrameWeighted(format.weightedAvg(dataset,keep_motors=True))
    elif extract:
        print("Extracting features")
        # extract frames into feature matrix
        ext = extract_features.ExtractFeatures(num_features)
        ext_X, ext_y = ext.from_data(dataset)
        df = DataFrame(np.column_stack((ext_X, ext_y)))
        df.columns = [*np.linspace(1,num_features*num_features,num_features*num_features),"left","right"]
    else:
        # raw data
        df = format.toDataFrame(dataset)
    return df

def save(model,folder,name):
    os.makedirs(folder, exist_ok=True)
    os.makedirs(folder, exist_ok=True)
    with open(folder+'/'+name, 'wb') as f:
        pickle.dump(model,f)
    print('saved model to ['+folder+'/'+name+']')
    
def develop_model( X, targety, estimator, name="", plot_heatmap=False, plot_learning=False ):
    
    #
    # Cross Validation with increasing amounts of data
    # to show accuracy plateau
    #    
    if plot_learning:
        plt.figure()
        train_size_percentages = np.linspace(0.01,1,40)
        train_sizes, train_scores, test_scores = learning_curve(estimator,X,targety,train_sizes=train_size_percentages, cv=12)
        train_scores_mean = np.mean(train_scores, axis=1)
        train_scores_std = np.std(train_scores, axis=1)
        test_scores_mean = np.mean(test_scores, axis=1)
        test_scores_std = np.std(test_scores, axis=1)
        plt.grid()
        plt.fill_between(range(0,40), train_scores_mean - train_scores_std,
                         train_scores_mean + train_scores_std, alpha=0.1,
                         color="r")
        plt.fill_between(range(0,40), test_scores_mean - test_scores_std,
                         test_scores_mean + test_scores_std, alpha=0.1, color="g")
        plt.plot(range(0,40), train_scores_mean, 'o-', color="r",
                 label="Training score")
        plt.plot(range(0,40), test_scores_mean, 'o-', color="g",
                 label="Cross-validation score")

        plt.xlabel("Number of laps")
        plt.ylabel("Model Accuracy")
        plt.legend(loc="best")
    
    
    #
    # Train actual model
    #
    model = estimator.fit( X, targety )
    
    #
    # Plot heatmap of predictions
    #
    if plot_heatmap:        

        try:
            num_targets = len(model.predict([[0,0]])[0])
        except TypeError as te:
            num_targets = 1

        for target in range(num_targets):

            # build matrix of predictions for every x,y coord
            # in 0 <= x <= 320, 0 <= y <= 200
            predictions = []

            for y in np.arange(0,200,20):
                y_pred  = []
                for x in np.arange(0,320,20):
                    if num_targets > 1:
                        y_pred.append( model.predict([[x,y]])[0][target] )
                    else:
                        y_pred.append( model.predict([[x,y]])[0] )
                predictions.append(y_pred)

            # plot predictions on heatmap
            plt.figure(dpi=80,figsize=(9,6))    
            hm = sns.heatmap(predictions,vmin=0,vmax=100,annot=True, cbar=True, fmt=".0f", xticklabels=np.arange(0,320,20), yticklabels=np.arange(0,200,20))
            plt.xlabel("x Coordinate of line")
            plt.ylabel("y Coordinate of line")
            plt.title(name)
        
    return model