from imageutils import *
from genutils import *
import numpy as np
from PIL import Image
import os
import sys

#Tests for functions from imageutils.py
image = resize_image('usman_pic copy.jpg', 200, 200)
image2 = resize_image('JPEG/good_cup.jpg', 200, 200)

'''
print (resize_image('usman_pic copy.jpg', 200, 200))
print(np.array(image))
print('************')
print(column_vector(image))
'''

'''
#Test for combined vectors and column vectors
image_vector_1 = column_vector(image)
image_vector_2 = column_vector(image2)
combined = combine_vectors(image_vector_1, image_vector_2)
print('image_vector_1: ', image_vector_1)
print('***********')
print('image_vector_2: ', image_vector_2)
print('***********')
print('combined vectors: ', combined)
'''


'''
#Test for load_images
try:
    loaded_images = load_images('JPEG')
    print("Images loaded successfully.")
    print(loaded_images)
except FileNotFoundError:
    print("Directory 'JPEG' not found.")
except Exception as e:
    print(f"Error loading images: {e}")
'''


'''
#Tests for the genutils.py functions
def main():
    required_params = ['input_file', 'output_file']
    optional_params = {'--verbose': 'False', '--mode': 'default'}
    
    try:
        params = parse_command_line_params(required_params, optional_params)
        print("Parsed parameters:", params)
    except ValueError as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
'''

#Test to open a few images from the MNIST set
loaded_images = load_images('trainingSet/2')
image_0 = Image.open('trainingSet/2/img_261.jpg')
image_0.show()
array_0 = np.array(image_0)
#print (array_0)
#print(loaded_images['img_261.jpg'])
print('Length of loaded images:', len(loaded_images))