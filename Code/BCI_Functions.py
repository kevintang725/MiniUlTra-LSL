# BCI Functions for Electrophysiological Analysis
# Author: Kai Wing Kevin Tang, 2023

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

def simple_moving_average(df, window_size=5):
    moving_average = df['column_name'].rolling(window_size).mean()
    return moving_average

def weight_moving_average(df, window_size=5):
    moving_average = df['column_name'].rolling(window_size).apply(lamda x: (weights*x).sum()/weights.sum())
    return moving_average

def exponential_moving_average(df, window_size=5):
    moving_average= df['column_name'].ewm(span=window_size, adjust=False).mean()
    return moving_average

def find_trigger_index(df):
    df_trigger_index = pd.DataFrame()
    for i in range(df):
        if df['column_name'](i) == 1:
            df_trigger_index = df_trigger_index.append({'Index':i}, ignore_index=True)
    return df_trigger_index

def train_LDA(data_path, names, n_components=1):
    dataset = pd.read_csv(data_path, names)
    X = dataset.iloc[:, 0:len(names) - 1]
    Y = dataset.iloc[:,len(names)]

    X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    sc = StandardScaler()
    X_train = sc.fittransform(X_train)
    X_test = sc.transform(X_test)

    lda = LDA(n_components=n_components)
    X_train = lda.fit_transform(X_train, Y_train)
    X_test = lda.transform(X_test)

def train_RandomForest(data_path, names, max_depth=2, random_state=0):
    dataset = pd.read_csv(data_path, names)
    X = dataset.iloc[:, 0:len(names) - 1]
    Y = dataset.iloc[:,len(names)]

    X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    classifier = RandomForestClassifier(max_depth=max_depth, random_state=random_state)
    classifier.fit(X_train, Y_train)
    Y_pred = classifier.predict(X_test)

    cm = confusion_matrix(Y_test, Y_pred)
    print(cm)
    print('Accuracy:' + str(accuracy_score(Y_test, Y_pred)))

    return(





