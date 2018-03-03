# Natural lighting
# To test with the android doll, run using the following colors:
# python3 main.py 2a7519 6ba257

# To test with the comet voice ball (bright orange), run using the following colors:
# python3 main.py 7b2803 fb8a33

# Artificial white light
# comet voice ball
# python3 main.py d4680a fec536

import cv2 as vision
import numpy as np
import rgb_to_hsv as r2h
import object_detector
import time
import sys
import os
from salt_and_pepper import add_salt_pepper_noise, remove_salt_pepper_noise
import copy

def convert_hex_to_rgb(hex):
	# this utility code was referred from 
	# https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python

	# this function converts the hexcode sent as arguments to R,G,B array.
	return np.array([int(hex[idx:idx+2], 16) for idx in (0, 2 ,4)])[::-1]

def main(low_mask, high_mask, noise_density):
	while (True):
		print("Menu:")
		print("l - record a live stream")
		print("r - read a saved video")
		print("q - quit")
		c = input("Choose an option from menu: ")
		if c == 'l':
			file_name = input("Enter a file name: ")
			camera = vision.VideoCapture(0)
			# Saving a video in MacOS was a problem..
			# the below link provided useful information about it.
			# http://tsaith.github.io/record-video-with-python-3-opencv-3-on-osx.html
			frame_width = int(camera.get(vision.CAP_PROP_FRAME_WIDTH))
			frame_height = int(camera.get(vision.CAP_PROP_FRAME_HEIGHT))
			codec = vision.VideoWriter_fourcc(*'mp4v')
			video_file = vision.VideoWriter(os.path.join("..","video",file_name+".mp4"),codec, 20.0, (frame_width,frame_height))
			video_file_tracked = vision.VideoWriter(os.path.join("..","video",file_name+"-tracked.mp4"),codec, 20.0, (frame_width,frame_height))
			grab = 1
			mask_low = convert_hex_to_rgb(low_mask)
			mask_high = convert_hex_to_rgb(high_mask)

			total_time_for_object_detection = 0
			print("Options:")
			print("1. Press 'c' key to capture a frame from live stream and process it")
			print("2. Press 'Esc' key to stop live stream.")
			print("Choose your option: ")
			while(True):
				timeTaken = 0
				isFrameReadCorrect, frame = camera.read()
				frame = vision.flip(frame,1) # horizontally flips the frame
				frame_tracked = copy.deepcopy(frame)
				if isFrameReadCorrect:
					start = time.time()
					frame_tracked = object_detector.detect_object(frame_tracked, mask_low, mask_high)
					end = time.time()
					timeTaken = 1/(end-start)
					video_file.write(frame)
					video_file_tracked.write(frame_tracked)
				
				vision.imshow("Live",frame_tracked)
				keyPressed = vision.waitKey(1)
				if keyPressed == 27:
					# 27 denotes Escape key
					if(grab != 1):
						print("Average time to detect object in", str(grab-1), "frames is", str(int(total_time_for_object_detection/(grab-1))), "frames per second")
					print("Closing the live stream. The recorded video is available at",os.path.join("..","video",file_name+".mp4"))
					print("\n\n")
					break
				elif keyPressed == ord('c'): 
					print("Capturing image...")
					path = os.path.join("..","images",file_name, "grab-"+str(grab))
					if not os.path.exists(path):
						os.makedirs(path)
					vision.imwrite(os.path.join(path,"rgb.jpg"),frame)

					print("Converting image from RGB to HSV color space...")
					vision.imwrite(os.path.join(path,"hsv.jpg"), r2h.convert_rgb_to_hsv(frame))

					print("Detecting the colored object...")

					# write the object-detected image to a file...
					vision.imwrite(os.path.join(path,"rgb-contoured.jpg"),frame_tracked)
					total_time_for_object_detection += timeTaken
					print("Total time elapsed:",str(int(timeTaken)),"frames per second")
						
					grab = grab + 1
			vision.destroyAllWindows()
			video_file.release()
			video_file_tracked.release()
			camera.release()

		elif c == 'r':
			file_name = input("Enter the file name: ")
			file = vision.VideoCapture(os.path.join("..","video",file_name+".mp4"))
			count = 0
			print("Options:")
			print("Press 'c' key while the video is playing to capture a frame, add salt and pepper noise and then remove it.")
			print("Press 'Esc' key to quit the video.")
			while(file.isOpened()):
				isFrameReadCorrect, frame = file.read()
				if isFrameReadCorrect:
					vision.imshow(file_name,frame)

				keyPressed = vision.waitKey(1)
				if keyPressed == ord('c'): 
					path = os.path.join("..","images", "noise",file_name+"-"+str(count))
					if not os.path.exists(path):
						os.makedirs(path)
					vision.imwrite(os.path.join(path,"original-frame.jpg"), frame)
					print("Adding salt and pepper noise to the image...")
					img = add_salt_pepper_noise(image=frame, density=noise_density)
					vision.imwrite(os.path.join(path,"sp-noise-added.jpg"), img)

					print("Removing salt and pepper noise from the image...")
					image = remove_salt_pepper_noise(img, filter_size=3)
					vision.imwrite(os.path.join(path,"sp-noise-removed.jpg"), image)
					count = count + 1
				if keyPressed == 27:
					break
			
			file.release()
			vision.destroyAllWindows()
		elif c == 'q':
			break


if len(sys.argv) >= 2:
	low_mask = sys.argv[1]
else:
	low_mask = "025a02"

if len(sys.argv) >= 3:
	high_mask = sys.argv[2]
else:
	high_mask = "78b478"

if len(sys.argv) >= 4:
	noise_density = float(sys.argv[3])
else:
	noise_density = 0.02

main(low_mask, high_mask, noise_density)