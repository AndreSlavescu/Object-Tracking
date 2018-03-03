import numpy

def rgb_to_hsv(pixel):
	# the logic was referred from https://www.rapidtables.com/convert/color/rgb-to-hsv.html
	b = pixel[0]/255
	g = pixel[1]/255
	r = pixel[2]/255
	c_max = max(r,g,b)
	c_min = min(r,g,b)
	delta = (c_max - c_min)

	if (c_max == 0):
		saturation = 0
	else:
		saturation = (delta / c_max);

	if delta == 0:
		hue = 0
	elif c_max == r:
		hue = 60 * (((g - b) / delta) % 6.0)
	elif c_max == g:
		hue = 60 * (((b - r) / delta) + 2.0)
	else:
		hue = 60 * (((r - g) / delta) + 4.0)

	return [int((hue/360)*255),int(saturation*255),int(c_max*255)]

def convert_rgb_to_hsv(image):
	result = list()
	for row in image:
		result_row = list()
		for column in row:
			result_row.append(rgb_to_hsv(column))
		result.append(result_row)
	return numpy.array(result)