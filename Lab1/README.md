# Lab 1: Face Swap Pro Plus Platinum Edition Deluxe

GitHub: https://github.com/Lord-Lelsers/Advanced-Honors-Comp-Sci/tree/main/Lab1

## Folder Structure

The project is in `Advanced-Honors-Comp-Sci/Lab1/`

- `models/`
	- Information about the neural network used to detect faces
- `test-input/`
	- Images and videos you can use to test the program
- `saves/`
	- Saved output from the program
	- Already contains some examples
- `resources/`
	- Font and images used by pygame GUI
- `/`
	- python files for the program and README

## Chapters

- 3: Loading, Displaying, and Saving
	- We load images (and videos), display them, and can save them
- 4: Image Basics
	- We access and modify sections of pixels
- 5: Drawing
	- In debug mode, we draw rectangle outlines and colored circles
- 6: Image Processing
	- We resize parts of images (the faces) to fit on other parts of the image
	- We also use various bitwise operations and create masks to only use part of an image at a time
- 8: Smoothing and Blurring
	- In blur mode, we blur the connection between a pasted face and the background
- Extra 1: Face Detection
	- We used a pretrained deep neural network to detect faces from an image
- Extra 2: Videos and Camera feed
	- We can take videos or use the camera feed as input and save the output as a video

## Usage

To run the program, run `main.py`.
After that, interact with the pygame window to continue using the program.
The pygame window will launch an OpenCV once `Continue` is clicked on.
You can continue to use the pygame window to change the parameters of the OpenCV in realtime.

## Notes

- OpenCV window FPS vs output/saved FPS
	- The output FPS is the FPS of the input video
	- However, it is not necessarily the FPS of the OpenCV window
	- When save is enabled, the FPS (really the delta time calculation is just `1 / output_fps`)
	- When save is disabled, the FPS is the FPS of the OpenCV window
- Fourcc
	- In our code to determine the fourcc of a video, we use the extension of the video
	- This generally works, but the fourcc can be platform dependent and this might not work on all platforms
	- Our extension to fourcc mapping is as follows:
```
extension_to_fourcc = {
	"avi": "XVID",
	"mp4": "mp4v",
	"mov": "mp4v",
	"mkv": "XVID",
}
```