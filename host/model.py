"""
Handles querying different models using the same raw pixy data
where models require the data to be in a specific format 
""" 
import sys
import pickle
import numpy as np
from sklearn import neural_network    
sys.path.append('/Users/samnockels/projects/dissertation/learning')
import format
import extract_features


class Model:
    
    def __init__(self, file_path, left_right=False, matrix=False, matrix_size=2):
        self.left_right = left_right
        self.matrix = matrix
        self.matrix_size = matrix_size
        if left_right:
            with open(file_path+'left.pkl', 'rb') as f:
                self.lm = pickle.load(f)
            with open(file_path+'right.pkl', 'rb') as f:
                self.rm = pickle.load(f)
        else:
            with open(file_path, 'rb') as f:
                self.model = pickle.load(f)

    """
    Makes prediction for motors based on vector of blocks as input
    returns list in the format [left motor, right motor]
    """
    def predict(self, blocks):
            
        if self.matrix:
            # extract into matrix
            ext = extract_features.ExtractFeatures(self.matrix_size)
            extracted = np.asarray(ext.from_frame(blocks)).flatten().tolist()

            # make and return prediction
            return [self.lm.predict([extracted])[0], self.rm.predict([extracted])[0]]
        else:
            x,y = format.weightedAvgBlocks(blocks)
            if self.left_right:
                return [self.lm.predict([[x,y]])[0], self.rm.predict([[x,y]])[0]]
            else:
                return self.model.predict([[x,y]])[0].tolist()