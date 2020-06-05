

def getImageLocations(path, oldestFirst):
	"""
	Given a directory will return an array of file paths for images.

	Args:
		path (string): Directory containing images
		oldestFirst (bool): Whether to sort images oldest first or newest firsts
	Returns:
		list: Sorted list of file paths to images
	"""

	pass


def makeVideo(images, saveName, imagesPerSecond):
	"""
	Creates a video from a series of images

	Args:
		images (list): A list of file paths to images
		saveName (string): The name of the file the video is saved as
		imagesPerSecond (int): Number of images displayed in a given second
	"""


def main():
	"""The main script"""
	path = "./images"
	saveName = "output"
	imagesPerSecond = 16
	oldestFirst = True

	images = getImageLocations(path, oldestFirst)

	makeVideo(images, saveName, imagesPerSecond)


if __name__ == "__main__":
	main()
