# BCI Functions for Electrophysiological Analysis
# Author: Kai Wing Kevin Tang, 2023

import pandas as pd

def simple_moving_average(df, window_size=5):
    moving_average = df['column_name'].rolling(window_size).mean()
    return moving_average

def weight_moving_average(df, window_size=5):
    moving_average = df['column_name'].rolling(window_size).apply(lamda x: (weights*x).sum()/weights.sum())
    return moving_average

def exponential_moving_average(df, window_size=5):
    moving_average= df['column_name'].ewm(span=window_size, adjust=False).mean()
    return moving_average