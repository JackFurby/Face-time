import glob
import os
from image_align import show_img, getTransformedImage
import cv2
from tqdm import tqdm
import argparse


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


def makeVideo(images, saveName, imagesPerSecond, width, height):
	"""
	Creates a video from a series of images

	Args:
		images (list): A list of file paths to images
		saveName (string): The name of the file the video is saved as
		imagesPerSecond (int): Number of images displayed in a given second
		width (int): Output video resolution width
		height (int): Output video resolution height
	"""

	video = cv2.VideoWriter(saveName + '.avi', 0, imagesPerSecond, (width, height))

	for i in tqdm(range(len(images))):

		img = getTransformedImage(images[i], width, height)

		if type(img) == type(None):
			print("No face found in", images[i])
			continue  # skip image

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

	images = getImageLocations(root, type, newestFirst)

	makeVideo(images, saveName, imagesPerSecond, width, height)


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
	parser.add_argument("--width", help="Width of output video in pixels (default: 3840)", type=int, default=3840)
	parser.add_argument("--height", help="Height of output video in pixels (default: 2160)", type=int, default=2160)
	args = parser.parse_args()

	main(args)
