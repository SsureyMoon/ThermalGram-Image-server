import os
import cv2
import numpy as np


# input image file path
image_dir = "./reference"
input_files = ['IMG_12.JPEG', 'IMG_15.JPEG', 'IMG_17.JPEG']

# open cv face recognition training set file
haarcascade_xml = 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(haarcascade_xml)

for input_file in input_files:
    # loop over input image files

    # read a jpeg file and store data in bgr array
    file_path = os.path.join(image_dir, input_file)
    image = cv2.imread(file_path)
    height, width = image.shape[:2]
    # image data to resize a face image to original image size
    square = height if width > height else width
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    for scale in np.arange(1.01, 1.1, 0.01):
        # try different parameters over files.
        # stop trying other parameters when it finds a face

        faces = faceCascade.detectMultiScale(
            image,
            scaleFactor=scale,
            minNeighbors=1,
            minSize=(5, 5),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        # assume that there is only one face
        if len(faces) == 1:

            # show original image
            cv2.imshow("Face", image)
            cv2.waitKey(0)
            print "file: {0}, scale: {1}, faces: {2}".format(file_path, scale, len(faces))
            print "hit the space on the picture."

            # mark face by green rectangle
            (x, y, w, h) = faces[0]
            orig_face=image[y:y+h, x:x+w]
            rectangled = image
            cv2.rectangle(rectangled, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.imshow("Face", rectangled)
            cv2.waitKey(0)

            # To make all faces have same size, we resize the face image as big as the original image size
            res = cv2.resize(orig_face,(square, square), interpolation = cv2.INTER_CUBIC)
            cv2.imshow("Face", res)
            cv2.waitKey(0)
            break
