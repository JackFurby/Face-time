# Face-time

### The basic idea

The script will be given a file path to a series of images of faces. Each image will then be loaded in from oldest to newest, the face located in the image, and then aligned with the images previously loaded (or just straightened for the first image). All the images will then be saved as a video at some number of photos per second.

### Guide

run `python face_time.py`

The output will be an avi file. To turn this into a mp4 (to save on storage space) use a program such as ffmpeg to convert it `ffmpeg -i output.avi output.mp4`
