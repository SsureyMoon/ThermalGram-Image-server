from __future__ import division
import os
import cv2
import numpy as np
from sklearn import svm
from sklearn import linear_model, datasets
from sklearn.grid_search import GridSearchCV
import pickle

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

IMAGE_FOLDER = os.path.join(BASE_DIR, 'data/image')
MODEL_FOLDER = os.path.join(BASE_DIR, 'data/model')

input_file = os.path.join(IMAGE_FOLDER, "IMG_17.JPEG")

BASE_ZONE1 = (np.array([0, 10, 50],np.uint8), np.array([100/2, 255, 255],np.uint8))
BASE_ZONE2 = (np.array([(-100+360)/2, 10, 50],np.uint8), np.array([360/2, 255, 255],np.uint8))
SCORE1_ZONE1 = (np.array([0, 10, 50],np.uint8), np.array([20, 255, 255],np.uint8))
SCORE1_ZONE2 = (np.array([(-20 + 360)/2, 10, 50],np.uint8), np.array([360/2, 255, 255],np.uint8))
SCORE2_ZONE1 = (np.array([21, 10, 50],np.uint8), np.array([50, 255, 255],np.uint8))


def thermal_grader(input_file, ext):
    image = cv2.imread(input_file)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    threshed_base1 = cv2.inRange(hsv, BASE_ZONE1[0], BASE_ZONE1[1])
    threshed_base2 = cv2.inRange(hsv, BASE_ZONE2[0], BASE_ZONE2[1])
    base_area = threshed_base1 + threshed_base2
    cv2.imwrite(os.path.join(IMAGE_FOLDER, "base."+ext),base_area)

    threshed1_1 = cv2.inRange(hsv, SCORE1_ZONE1[0], SCORE1_ZONE1[1])
    threshed1_2 = cv2.inRange(hsv, SCORE1_ZONE2[0], SCORE1_ZONE2[1])
    point_1_area = threshed1_1 + threshed1_2
    cv2.imwrite(os.path.join(IMAGE_FOLDER, "point1."+ext), point_1_area)

    threshed2_1 = cv2.inRange(hsv, SCORE2_ZONE1[0], SCORE2_ZONE1[1])
    point_2_area = threshed2_1
    cv2.imwrite(os.path.join(IMAGE_FOLDER, "point2."+ext), point_2_area)

    total_base = sum(sum(base_area/255))
    total_hot = 0.75*sum(sum(point_1_area/255)) + 1.25*sum(sum(point_2_area/255))

    hot = 5.5*(total_hot/total_base)
    return_value = 5 if hot > 5 else hot
    return return_value

if __name__ == "__main__":
    print thermal_grader(input_file)