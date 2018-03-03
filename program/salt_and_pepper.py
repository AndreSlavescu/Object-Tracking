import numpy as np
import random 

def add_salt_pepper_noise(image, density):
	height_of_image = len(image);
	width_of_image = len(image[0]);
	total_no_of_pixels = height_of_image * width_of_image;
	no_of_noisy_pixels = int(total_no_of_pixels * density);
	random.seed();
	for i in range(no_of_noisy_pixels):
		noisy_pixel_x = random.randint(1, height_of_image-1);
		noisy_pixel_y = random.randint(1, width_of_image-1);
		noise = random.randint(0, 1);
		if noise == 0:
			image[noisy_pixel_x][noisy_pixel_y] = [0, 0, 0];
		else:
			image[noisy_pixel_x][noisy_pixel_y] = [255, 255, 255];
	return image;

def get_neighbours_for_channel(image, x, y, z, filter_size):
	pixels = list(range(-int(filter_size/2), int(filter_size/2)+1,1));
	result = list();
	for delta_x in pixels:
		for delta_y in pixels:
			neighbour = (x+delta_x, y+delta_y);
			if (neighbour[0] >= 0 and neighbour[0] < len(image)) and (neighbour[1] >= 0 and neighbour[1] < len(image[0])):
				result.append(image[neighbour[0]][neighbour[1]][z]);
	return result;

def remove_salt_pepper_noise(image, filter_size=3):
	new_image = np.copy(image);
	for x in range(1, len(image)-1):
		for y in range(1, len(image[0])-1):
			if np.array_equal(image[x][y], [0, 0, 0]) or np.array_equal(image[x][y], [255, 255, 255]):
				for z in range(0,2):
					box = get_neighbours_for_channel(image, x, y, z, filter_size);
					box.sort();
					new_image[x][y][z] = box[int(len(box)/2)];
	return new_image;