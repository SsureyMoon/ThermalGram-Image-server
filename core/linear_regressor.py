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
    # cv2.waitKey(0)
    pkl_file = None
    if os.path.exists(os.path.join(MODEL_FOLDER, "lr_model.pkl")):
        pkl_file = open(os.path.join(MODEL_FOLDER, "lr_model.pkl"), 'rb')
        regr = pickle.load(pkl_file)
        pkl_file.close()
    else:
        regr = linear_model.LinearRegression()

    regr.fit(X, Y)
    predicted_rate = regr.predict(X)
    pkl_file = open(os.path.join(MODEL_FOLDER, "lr_model.pkl"), 'wb')
    pickle.dump(regr, pkl_file)

    return float(predicted_rate[0])
