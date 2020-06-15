import glob
import os
from image_align import getAlignmentInfo, imgRotate, imgScale, imgCrop, show_img, rotation_detection_dlib, imgPad
import matplotlib
import matplotlib.pyplot as plt
from celluloid import Camera
import cv2
import numpy as np
from tqdm import tqdm
import argparse
matplotlib.use("Agg")


def getImageLocations(root, type, newestFirst):
	"""
	Given a directory will return an array of file paths for images.

	Args:
		root (string): Directory containing images
		type (string): Type of file (e.g. jpg or png)
		newestFirst (bool): Whether to sort images oldest first or newest firsts
	Returns:
		list: Sorted list of file paths to images
	"""
	images = glob.glob(os.path.join(root + '/*.' + type))
	images.sort(key=os.path.getmtime, reverse=newestFirst)

	return images


def makeVideo(images, saveName, imagesPerSecond, width, height, padding):
	"""
	Creates a video from a series of images

	Args:
		images (list): A list of file paths to images
		saveName (string): The name of the file the video is saved as
		imagesPerSecond (int): Number of images displayed in a given second
	"""

	video = cv2.VideoWriter(saveName + '.avi', 0, imagesPerSecond, (width, height))

	for i in tqdm(range(len(images))):
		img, scale, point, angle = getAlignmentInfo(images[i], width, height, padding)
		if (scale == -1) and (point == (-1, -1)) and (angle == -1):
			print("No face found in", images[i])
			continue  # skip image
		#img = cv2.circle(img, (point[0], point[1]), 10, (0, 0, 255), -1)  # Draw dot between eyes
		img = imgRotate(img, point, angle)
		img = imgScale(img, scale)
		# After rotate + scale, point needs updating - recaculate it (this is very slow)
		newXscale, newPoint, newAngle = rotation_detection_dlib(img)
		img = imgPad(img, width, height)  # Ensures the selected resolution is possible
		newPoint = (newPoint[0] + height, newPoint[1] + width)
		img = imgCrop(img, newPoint, width, height)
		#print(img.shape)

		video.write(img)

	cv2.destroyAllWindows()
	video.release()


def main(args):
	"""The main script"""
	root = args.input
	type = args.type
	saveName = args.save
	imagesPerSecond = args.ips
	newestFirst = False
	width = args.width
	height = args.height
	padding = args.padding

	images = getImageLocations(root, type, newestFirst)

	makeVideo(images, saveName, imagesPerSecond, width, height, padding)


# https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
def str2bool(v):
	if isinstance(v, bool):
		return v
	if v.lower() in ('yes', 'true', 't', 'y', '1'):
		return True
	elif v.lower() in ('no', 'false', 'f', 'n', '0'):
		return False
	else:
		raise argparse.ArgumentTypeError('Boolean value expected.')


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--input", help="Folder of images to use", required=True)
	parser.add_argument("--type", choices=['jpg', 'jpeg', 'png'], help="Image file type", required=True)
	parser.add_argument("--save", help="Name of output video (default: output)", default="output")
	parser.add_argument("--ips", help="Images per second in output (default: 8)", type=int, default=8)
	parser.add_argument("--width", help="Width of output video in pixels (default: 7680)", type=int, default=7680)
	parser.add_argument("--height", help="Height of output video in pixels (default: 4320)", type=int, default=4320)
	args = parser.parse_args()

	main(args)
