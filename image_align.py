"""implementation based on https://www.pyimagesearch.com/2017/05/22/face-alignment-with-opencv-and-python"""
import cv2
import dlib
import numpy as np
from collections import OrderedDict


# For dlib’s 68-point facial landmark detector:
FACIAL_LANDMARKS_68_IDXS = OrderedDict([
	("mouth", (48, 68)),
	("inner_mouth", (60, 68)),
	("right_eyebrow", (17, 22)),
	("left_eyebrow", (22, 27)),
	("right_eye", (36, 42)),
	("left_eye", (42, 48)),
	("nose", (27, 36)),
	("jaw", (0, 17))
])

# For dlib’s 5-point facial landmark detector:
FACIAL_LANDMARKS_5_IDXS = OrderedDict([
	("right_eye", (2, 3)),
	("left_eye", (0, 1)),
	("nose", (4))
])


def load_img(path):
	img = cv2.imread(path)
	return img


def imgCrop(img, point, width, height):
	left = int(point[0] - (width / 2))
	right = int(point[0] + (width / 2))
	upper = int(point[1] - (height / 2))
	lower = int(point[1] + (height / 2))
	cropped_img = img[upper:lower, left:right, :]
	return cropped_img


def imgPad(img, width, height):
	BLACK = [0, 0, 0]
	return cv2.copyMakeBorder(img, width, width, height, height, cv2.BORDER_CONSTANT, value=BLACK)


# Heavily based on https://github.com/jrosebr1/imutils/blob/master/imutils/face_utils/facealigner.py
def align(image, gray, rect, predictor, desiredFaceWidth, desiredFaceHeight=None, desiredLeftEye=(0.35, 0.35)):
	# convert the landmark (x, y)-coordinates to a NumPy array
	shape = predictor(gray, rect)

	# initialize the list of (x, y)-coordinates
	coords = np.zeros((shape.num_parts, 2), dtype="int")

	# loop over all facial landmarks and convert them
	# to a 2-tuple of (x, y)-coordinates
	for i in range(0, shape.num_parts):
		coords[i] = (shape.part(i).x, shape.part(i).y)

	shape = coords

	height, width = image.shape[:2]
	image_center = (width/2, height/2)

	if desiredFaceHeight is None:
		desiredFaceHeight = desiredFaceWidth

	# support for both dlib 68 and 5 facial landmarks
	if (len(shape) == 68):
		# extract the left and right eye (x, y)-coordinates
		(lStart, lEnd) = FACIAL_LANDMARKS_68_IDXS["left_eye"]
		(rStart, rEnd) = FACIAL_LANDMARKS_68_IDXS["right_eye"]
	else:
		(lStart, lEnd) = FACIAL_LANDMARKS_5_IDXS["left_eye"]
		(rStart, rEnd) = FACIAL_LANDMARKS_5_IDXS["right_eye"]

	leftEyePts = shape[lStart:lEnd]
	rightEyePts = shape[rStart:rEnd]

	# compute the center of mass for each eye
	leftEyeCenter = leftEyePts.mean(axis=0).astype("int")
	rightEyeCenter = rightEyePts.mean(axis=0).astype("int")

	# compute the angle between the eye centroids
	dY = rightEyeCenter[1] - leftEyeCenter[1]
	dX = rightEyeCenter[0] - leftEyeCenter[0]
	angle = np.degrees(np.arctan2(dY, dX)) - 180

	# compute the desired right eye x-coordinate based on the
	# desired x-coordinate of the left eye
	desiredRightEyeX = 1.0 - desiredLeftEye[0]

	# determine the scale of the new resulting image by taking
	# the ratio of the distance between eyes in the *current*
	# image to the ratio of distance between eyes in the
	# *desired* image
	dist = np.sqrt((dX ** 2) + (dY ** 2))
	desiredDist = (desiredRightEyeX - desiredLeftEye[0])
	desiredDist *= desiredFaceWidth
	scale = desiredDist / dist

	# compute center (x, y)-coordinates (i.e., the median point)
	# between the two eyes in the input image
	eyesCenter = ((leftEyeCenter[0] + rightEyeCenter[0]) // 2,
		(leftEyeCenter[1] + rightEyeCenter[1]) // 2)

	# grab the rotation matrix for rotating and scaling the face
	M = cv2.getRotationMatrix2D(eyesCenter, angle, scale)

	# rotation calculates the cos and sin, taking absolutes of those.
	abs_cos = abs(M[0,0])
	abs_sin = abs(M[0,1])

	# find the new width and height bounds
	bound_w = int(height * abs_sin + width * abs_cos)
	bound_h = int(height * abs_cos + width * abs_sin)

	# translate face to align center of eyes to the center of the output
	M[0, 2] += bound_w/2 - eyesCenter[0]
	M[1, 2] += bound_h/2 - eyesCenter[1]

	# apply the affine transformation
	output = cv2.warpAffine(image, M, (int(bound_w), int(bound_h)),
		flags=cv2.INTER_CUBIC )

	return output


def show_img(img):
	while True:
		img = cv2.resize(img, (360,480))
		cv2.imshow('image', img)
		c = cv2.waitKey(1)
		if c == 27:  # press ESC key to close
			break
	cv2.destroyAllWindows()


def getTransformedImage(path, width, height):
	img = load_img(path)
	faceWidth = width * 0.5

	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor('shape_predictor_5_face_landmarks.dat')
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	rects = detector(gray, 0)
	for rect in rects:
		#  points of rectangle around face detected
		x = rect.left()
		y = rect.top()
		w = rect.right()
		h = rect.bottom()

		faceAligned = align(img, gray, rect, predictor, desiredFaceWidth=faceWidth)
		faceAligned = imgPad(faceAligned, width, height)
		point = (faceAligned.shape[1]/2, faceAligned.shape[0]/2)
		faceAligned = imgCrop(faceAligned, point, width, height)
		#show_img(faceAligned)

		return faceAligned
	# no face found
	else:
		return None
