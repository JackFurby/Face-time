import glob
import os
from image_align import getAlignmentInfo, imgRotate, show_img
import matplotlib
import matplotlib.pyplot as plt
from celluloid import Camera
import cv2
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
	fig = plt.figure()
	fig, ax = plt.subplots(nrows=1, ncols=1)
	camera = Camera(fig)

	for image in images:
		img, scale, point, angle = getAlignmentInfo(image)
		img = imgRotate(img, point, angle)
		#img = imgScale(img, scale)
		ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
		#plt.imshow(img)
		camera.snap()

	animation = camera.animate()
	animation.save(saveName + '.mp4', fps=imagesPerSecond)


def main():
	"""The main script"""
	root = "./images"
	root = "./imgTest"
	type = "jpg"
	saveName = "output"
	imagesPerSecond = 16
	newestFirst = False

	images = getImageLocations(root, type, newestFirst)

	makeVideo(images, saveName, imagesPerSecond)


if __name__ == "__main__":
	main()
