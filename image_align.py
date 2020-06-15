"""implementation based on https://github.com/HikkaV/Precise-face-alignment/blob/master/face_alignment.py"""
import cv2
import numpy as np
import dlib
import time
import imutils


def load_img(path):
	img = cv2.imread(path)
	return img


def get_eyes_nose_dlib(shape):
	nose = shape[4][1]
	left_eye_x = int(shape[3][1][0] + shape[2][1][0]) // 2
	left_eye_y = int(shape[3][1][1] + shape[2][1][1]) // 2
	right_eyes_x = int(shape[1][1][0] + shape[0][1][0]) // 2
	right_eyes_y = int(shape[1][1][1] + shape[0][1][1]) // 2
	return nose, (left_eye_x, left_eye_y), (right_eyes_x, right_eyes_y)


def rotate_point(origin, point, angle):
	ox, oy = origin
	px, py = point

	qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
	qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
	return qx, qy


def is_between(point1, point2, point3, extra_point):
	c1 = (point2[0] - point1[0]) * (extra_point[1] - point1[1]) - (point2[1] - point1[1]) * (extra_point[0] - point1[0])
	c2 = (point3[0] - point2[0]) * (extra_point[1] - point2[1]) - (point3[1] - point2[1]) * (extra_point[0] - point2[0])
	c3 = (point1[0] - point3[0]) * (extra_point[1] - point3[1]) - (point1[1] - point3[1]) * (extra_point[0] - point3[0])
	if (c1 < 0 and c2 < 0 and c3 < 0) or (c1 > 0 and c2 > 0 and c3 > 0):
		return True
	else:
		return False


def distance(a, b):
	return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def cosine_formula(length_line1, length_line2, length_line3):
	cos_a = -(length_line3 ** 2 - length_line2 ** 2 - length_line1 ** 2) / (2 * length_line2 * length_line1)
	return cos_a


def shape_to_normal(shape):
	shape_normal = []
	for i in range(0, 5):
		shape_normal.append((i, (shape.part(i).x, shape.part(i).y)))
	return shape_normal


def imgRotate(img, nose_center, angle):
	rotated = imutils.rotate_bound(img, angle)
	return rotated


def imgScale(img, scale):
	width = int(img.shape[1] * scale)
	height = int(img.shape[0] * scale)
	dim = (width, height)
	return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)


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


def rotation_detection_dlib(img, eyeXDist=720):
	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor('shape_predictor_5_face_landmarks.dat')
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	rects = detector(gray, 0)
	for rect in rects:
		x = rect.left()
		y = rect.top()
		w = rect.right()
		h = rect.bottom()
		shape = predictor(gray, rect)
		shape = shape_to_normal(shape)
		nose, left_eye, right_eye = get_eyes_nose_dlib(shape)
		center_of_forehead = ((left_eye[0] + right_eye[0]) // 2, (left_eye[1] + right_eye[1]) // 2)
		xScale = eyeXDist / (right_eye[0] - left_eye[0])  # Value in which to scale image to keep distance between eyes a constant (eyeXDist)
		center_pred = (int((x + w) / 2), int((y + y) / 2))
		length_line1 = distance(center_of_forehead, nose)
		length_line2 = distance(center_pred, nose)
		length_line3 = distance(center_pred, center_of_forehead)
		cos_a = cosine_formula(length_line1, length_line2, length_line3)
		angle = np.arccos(cos_a)
		rotated_point = rotate_point(nose, center_of_forehead, angle)
		rotated_point = (int(rotated_point[0]), int(rotated_point[1]))
		if is_between(nose, center_of_forehead, center_pred, rotated_point):
			angle = np.degrees(-angle)
		else:
			angle = np.degrees(angle)
		return xScale, rotated_point, angle
	# No face found
	else:
		return -1, (-1, -1), -1


def show_img(img):
	while True:
		img = cv2.resize(img, (360,480))
		cv2.imshow('image', img)
		c = cv2.waitKey(1)
		if c == 27:  # press ESC key to close
			break
	cv2.destroyAllWindows()


def getAlignmentInfo(path, width, height, padding=True):
	img = load_img(path)
	xScale, rotated_point, angle = rotation_detection_dlib(img)
	return img, xScale, rotated_point, angle
