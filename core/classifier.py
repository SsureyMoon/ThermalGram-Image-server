import os
import cv2
import numpy as np
from sklearn import svm
from sklearn import linear_model, datasets
from sklearn.grid_search import GridSearchCV

# input image file path
image_dir = "./reference"
input_files = ['IMG_12.JPEG', 'IMG_15.JPEG', 'IMG_17.JPEG',
               'IMG_20.JPEG', 'IMG_22.JPEG', 'IMG_25.JPEG',
                'IMG_26.JPEG', 'IMG_28.JPEG']
rates_from_user = [1, 2, 5,
                   2.5, 2.5, 4.5,
                   2, 4]

# open cv face recognition training set file
haarcascade_xml = 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(haarcascade_xml)

enum = 0
for input_file in input_files:
    # loop over input image files

    # read a jpeg file and store data in bgr array
    file_path = os.path.join(image_dir, input_file)
    image = cv2.imread(file_path)

    height, width = image.shape[:2]
    # image data to resize a face image to original image size
    square = height if width > height else width

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    cv2.imshow("Face", gray)
    cv2.waitKey(0)

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
            cv2.imshow("Face", gray)
            # cv2.waitKey(0)
            print "file: {0}, scale: {1}, faces: {2}".format(file_path, scale, len(faces))
            print "hit the space on the picture."

            # mark face by green rectangle
            (x, y, w, h) = faces[0]
            orig_face_therm = image[y:y+h, x:x+w]
            orig_face_gray = gray[y:y+h, x:x+w]

            cv2.rectangle(gray, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.imshow("Face", gray)

            # To make all faces have same size, we resize the face image as big as the original image size
            res = cv2.resize(orig_face_gray,(square, square), interpolation = cv2.INTER_CUBIC)

            X = np.reshape(res, -1)

            print rates_from_user[enum]
            Y = np.array([rates_from_user[enum]])
            enum = enum + 1
            # cv2.waitKey(0)
            regr = linear_model.LinearRegression()

            regr.fit(X, Y)

            rates = regr.predict(X)
            print "predictied rate: ", rates
            # clf = GridSearchCV(SVR(kernel='rbf', class_weight='auto'), param_grid)
            # clf = clf.fit(X_train_pca, y_train)
            # clf = svm.SVR()
            # clf.fit(X, y)
            res = cv2.resize(orig_face_therm,(square, square), interpolation = cv2.INTER_CUBIC)
            print cv2
            cv2.imshow("Face rate:" + str(rates), res)
            cv2.waitKey(0)
            break
