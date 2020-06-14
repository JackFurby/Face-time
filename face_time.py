import glob
import os
from image_align import getAlignmentInfo, imgRotate, imgScale, imgCrop, show_img, rotation_detection_dlib
import matplotlib
import matplotlib.pyplot as plt
from celluloid import Camera
import cv2
import numpy as np
from tqdm import tqdm
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


def makeVideo(images, saveName, imagesPerSecond):
	"""
	Creates a video from a series of images

	Args:
		images (list): A list of file paths to images
		saveName (string): The name of the file the video is saved as
		imagesPerSecond (int): Number of images displayed in a given second
	"""
	#fig = plt.figure()
	#fig, ax = plt.subplots(nrows=1, ncols=1)
	#camera = Camera(fig)

	# 4608, 3456

	width = 2200
	height = 2750

	video = cv2.VideoWriter(saveName + '.avi', 0, imagesPerSecond, (width, height))

	for i in tqdm(range(len(images))):
		img, scale, point, angle = getAlignmentInfo(images[i])
		#img = cv2.circle(img, (point[0], point[1]), 10, (0, 0, 255), -1)  # Draw dot on center of eyes
		img = imgRotate(img, point, angle)
		img = imgScale(img, scale)
		# After rotate + scale, point moves - recaculate it (this is very slow)
		newXscale, newPoint, newAngle = rotation_detection_dlib(img)
		img = imgCrop(img, newPoint, width, height)
		img = np.array(img)
		#print(img.shape)

		video.write(img)

	cv2.destroyAllWindows()
	video.release()

	#animation = camera.animate()
	#animation.save(saveName + '.mp4', fps=imagesPerSecond)


def main():
	"""The main script"""
	root = "./images"
	type = "jpg"
	saveName = "output"
	imagesPerSecond = 16
	newestFirst = False

	images = getImageLocations(root, type, newestFirst)

	makeVideo(images, saveName, imagesPerSecond)


if __name__ == "__main__":
	main()
