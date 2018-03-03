import cv2 as vision
import os
import numpy as np


def detect_object(image, mask_low, mask_high):
	# band-pass filter that only allows certain color to pass through
	# inRange function accepts in BGR format not in RGB format
	im_bw = vision.inRange(image, mask_low, mask_high);

	# find the contours that surrounds white regions in black/white image...
	result, contours, hierarchy = vision.findContours(im_bw, vision.RETR_TREE, vision.CHAIN_APPROX_SIMPLE);

	if len(contours) > 0:
		# find the biggest contour and gets the center and radius of the minimum enclosing circle
		(x,y), radius = vision.minEnclosingCircle(max(contours, key=len))

		# draw the enclosing circle around the object in original image...
		vision.circle(image,(int(x),int(y)),int(radius),(255,255,0),2);

	return image;
