# import the necessary packages
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
help="path to input image")
args = vars(ap.parse_args())

PREDICTOR = "shape_predictor_68_face_landmarks.dat"

def get_face_landmarks(image):

    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(PREDICTOR)


    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # detect faces in the grayscale image
    rects = detector(gray, 1)

    landmarks = []

    # loop over the face detections
    for (i, rect) in enumerate(rects):
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        landmarks.append(shape)


        for (x, y) in shape:
            cv2.circle(image, (x, y), 1, (0, 0, 255), -1)

    return landmarks


# load the input image, resize it, and convert it to grayscale
image = cv2.imread(args["image"])
# image = imutils.resize(image, width=500)
print(get_face_landmarks(image))
cv2.imshow("Output", image)
cv2.waitKey(0)
