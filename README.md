# Face-time

### The basic idea

Given a file path to a folder of face images, this script will output a video of aligned and scaled pictures ordered from oldest to newest (based on the file name). The user can enter various parameters according to their needs.

### How to use

usage of this script will require you to have installed Python on your machine and installed all dependencies found in requirements.txt. There are several arguments to pass into the script which are as follows:

```
arguments:
  -h, --help            show this help message and exit
  --input INPUT         Folder of images to use (required)
  --type {jpg,jpeg,png} Image file type (required)
  --save SAVE           Name of output video (default: output)
  --ips IPS             Images per second in output (default: 8)
  --width WIDTH         Width of output video in pixels (default: 3840)
  --height HEIGHT       Height of output video in pixels (default: 2160)
```

Example run command `python face_time.py --input=./images --type=jpg --save=saveVideo --ips=16 --width=2000 --height=2500`

Alignment of faces from frame to frame seems to work best with higher resolutions. The default is 4k. If you have issues with a lower resolution then you may wish to lower the resolution in a separate video editing program with the output video from this script.

The output video will be an avi file. To turn this into an mp4 (to save on storage space) use a program such as ffmpeg to convert it. If you use ffmpeg the following command will create the new file `ffmpeg -i output.avi output.mp4`.

If there are multiple faces in the picture then the middle face will be selected.

### How it works

### references
