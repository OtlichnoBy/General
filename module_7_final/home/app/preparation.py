import numpy as np
import pandas as pd 
from sklearn import preprocessing 
import sklearn.preprocessing as pp


def normalize_data(df):
        
    scaler = preprocessing.RobustScaler()
    scaler.fit_transform(df)
    df_scaler = scaler.transform(df)
    
    return df_scaler