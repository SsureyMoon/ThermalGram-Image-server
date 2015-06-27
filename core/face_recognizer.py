import os
import cv2
import numpy as np
from sklearn import svm
from sklearn import linear_model, datasets
from sklearn.grid_search import GridSearchCV
from settings import config

# open cv face recognition training set file
haarcascade_xml = \
    os.path.join(config.BASE_DIR, 'core/haarcascade_frontalface_default.xml')
faceCascade = cv2.CascadeClassifier(haarcascade_xml)


def face_recognizer(input_file, rate):

    # read a jpeg file and store data in bgr array
    image = cv2.imread(input_file)

    # image data to resize a face image to original image size
    height, width = image.shape[:2]
    square = height if width > height else width

    # temporary use
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    for scale in np.arange(1.01, 1.5, 0.01):
        # try different parameters over files.
        # stop trying other parameters when it finds a face

        faces = faceCascade.detectMultiScale(
            image,
            scaleFactor=scale,
            minNeighbors=1,
            minSize=(10, 10),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        # assume that there is only one face
        if len(faces) == 1:

            # show original image
            print "file: {0}, scale: {1}, faces: {2}".format(input_file, scale, len(faces))
            print "hit the space on the picture."

            # mark face by green rectangle
            (x, y, w, h) = faces[0]
            orig_face_therm = image[y:y+h, x:x+w]
            orig_face_gray = gray[y:y+h, x:x+w]

            cv2.rectangle(gray, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # To make all faces have same size, we resize the face image as big as the original image size
            res = cv2.resize(orig_face_gray,(square, square), interpolation=cv2.INTER_CUBIC)

            return res

        else:
            return None


