# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 00:11:30 2026

@author: dell
"""

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

def build_lstm_model(time_step, n_features=1):
    model = Sequential()
    model.add(LSTM(64, return_sequences=True, input_shape=(time_step, n_features)))
    model.add(Dropout(0.2))
    model.add(LSTM(64))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    return model