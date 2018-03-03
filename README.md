# Program to detect object from a frame in a live stream
This project is a part of academic curriculum.

#### System Requirements:
1. Laptop or a desktop with webcam set up. (Requires permission to use webcam. The project does not communicate anything remotely. All things happen only locally :) )

#### Instructions to run the program:
1. Install python3 if not available in your system
2. Install opencv-python package using pip installer.
3. Go the program directory and run the following command:
`python3 main.py <lower_end_of_range> <higher_end_of_range>`

#### Description about the command-line arguments:
main.py is the driver program that starts the app.
`lower_end_of_range` is the lower end of the range of colors to be detected.
`higher_end_of_range` is the higher end of the range of colors to be detected.

#### Why LOWER_END_OF_RANGE and UPPER_END_OF_RANGE?
The program begins by opening the webcam or any other primary camera of the system where it is run.

The user has to choose either `l` or `r` or `q` to either start recording a live stream or read a recorded video or quit the application respectively.

Live stream ( l ):
On pressing `c` (for capture) key, the program captures a frame and does the following:
1. It saves the captures frame (in RGB) format as an image file (rgb.jpg).
2. It converts the RGB image to HSV format and saves it as a new image file (hsv.jpg).
3. It then detects the object using the color range specified in the command-line arguments as `lower_end_of_range` and `higher_end_of_range`. This produces a black and white image (not a grayscale but a binary black/white image). The area where the object is present is in white and the other areas will be black.
4. It saves the object-tracked image as a new image file (rgb-contoured.jpg).

On pressing `Esc` key with the focus on the live streaming window, the live stream recording stops.

Read a recorded video ( r ):
On pressing `c`, the program captures a frame and does the following:
1. The program then adds salt and pepper noise with density 0.02 to the original RGB image and saves it as a new image file (sp-noise-added.jpg).
2. The program then applies the median filter algorithm to remove the salt and pepper noise and saves the result of the algorithm as a new image (sp-noise-removed.jpg).

On pressing `Esc` key with the focus on the video playback window, the video playback stops.

**Note:** The accuracy of the program depends on the range of the colors specified in the command line argument while running the program.
