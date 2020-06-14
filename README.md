# Face-time

### The basic idea

Given a file path to a folder of face images, this script will output a video of aligned and scaled pictures ordered from oldest to newest. The user can enter various parameters according to their needs.

### How to use

usage of this script will require you to have installed Python on your machine and installed all dependencies found in requirements.txt. There are several arguments to pass into the script which are as follows:

```
arguments:
  -h, --help            show this help message and exit
  --input INPUT         Folder of images to use (required)
  --type {jpg,jpeg,png} Image file type (required)
  --save SAVE           Name of output video (default: output)
  --ips IPS             Images per second in output (default: 8)
  --width WIDTH         Width of output video in pixels (default: 7680)
  --height HEIGHT       Height of output video in pixels (default: 4320)
  --padding PADDING     Add padding to the images to guarantee the width and height do not exceed their boundaries (default: True)
```

Example run command `python face_time.py --input=./images --type=jpg --save=saveVideo --ips=16 --width=2000 --height=2500 --padding=False`

Width and height are required to be large otherwise sections of faces in images could be cropped. The default is 8k which seems to work well with photos from modern smartphones. If padding is set to False it is up to the user to ensure the resolution does not extend out of range of the image dimensions. When padding is set to True, this will not be an issue but the time to process images will be greatly increased. You may wish to modify the output video after rendering, in a video editing program of your choice, to be at a lower resolution.

The output video will be an avi file. To turn this into an mp4 (to save on storage space) use a program such as ffmpeg to convert it. If you use ffmpeg the following command will create the new file `ffmpeg -i output.avi output.mp4`.

### How it works

### references
