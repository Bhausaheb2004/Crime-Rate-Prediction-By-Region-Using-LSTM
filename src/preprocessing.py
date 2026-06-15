# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 00:11:57 2026

@author: dell
"""

import numpy as np
from sklearn.preprocessing import MinMaxScaler

def create_sequences(data, time_step):
    X, y = [], []
    for i in range(len(data) - time_step):
        X.append(data[i:i+time_step])
        y.append(data[i+time_step])
    return np.array(X), np.array(y)

def scale_data(values):
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(values.reshape(-1,1))
    return scaled, scaler