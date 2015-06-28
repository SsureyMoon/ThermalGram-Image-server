import os
import cv2
import numpy as np
from sklearn import svm
from sklearn import linear_model, datasets
from sklearn.grid_search import GridSearchCV
from settings import config
import pickle

MODEL_FOLDER = os.path.join(config.BASE_DIR, 'data/model')


def linear_regressor(res, rate):

    X = np.reshape(res, -1)
    Y = np.array([int(rate)])

    pkl_file = None
    if os.path.exists(os.path.join(MODEL_FOLDER, "lr_model.pkl")):
        pkl_file = open(os.path.join(MODEL_FOLDER, "lr_model.pkl"), 'rb')
        regr = pickle.load(pkl_file)
        pkl_file.close()
        predicted_rate = regr.predict(X)
    else:
        regr = linear_model.LinearRegression()
        predicted_rate = [2.5, ]

    regr.fit(X, Y)
    pkl_file = open(os.path.join(MODEL_FOLDER, "lr_model.pkl"), 'wb')
    pickle.dump(regr, pkl_file)

    return_value = float(predicted_rate[0])
    if return_value > 5:
        return 5.0
    elif return_value < 0:
        return 0.0
    return float(predicted_rate[0])
