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
    loaded_images_2 = load_images('JPEG')
    print("Images loaded successfully.")
    print(loaded_images_2)
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
loaded_images_2 = load_images('trainingSet/2')
image_261 = Image.open('trainingSet/2/img_261.jpg')
#image_261.show()
array_261 = np.array(image_261)
#print (array_261)
#print(loaded_images_2['img_261.jpg'])
#print('Length of loaded images:', len(loaded_images_2))


#Normalized image for img_261.jpg (2)
array_261 = loaded_images_2['img_261.jpg']
norm_261 = np.linalg.norm(array_261)
normalized_261 = array_261 / norm_261
flat_array_261 = normalized_261.flatten()
flat_normalized_261 = np.array(flat_array_261)
#print('Normalized image array: ', normalized_261)



#compute dot product of img_261.jpg vector with normalized image vector, restults with 1.0 
dot_261 = np.dot(flat_array_261, flat_normalized_261)
#print(dot_261)


#compute dot product of normalized image vector of im_261 and img_271
array_271 = loaded_images_2['img_271.jpg']
norm_271 = np.linalg.norm(array_271)
normalized_271 = array_271 / norm_271
flat_array_271 = normalized_271.flatten()
flat_normalized_271 = np.array(flat_array_271)
dot_271_261 = np.dot(flat_normalized_271, flat_normalized_261)
#print('Normal dot product w/ 261 and 271 = ', dot_271_261)



#compute the dot product of img_261 with 10 other images of 2 from the MNIST set
print('Dot products with 2 and other 2 images:')
total_2 = 0
for i, (key, value) in enumerate(loaded_images_2.items()):
    if i == 10:
        break
    norm = np.linalg.norm(value)
    normalized_vector = value / norm
    flat_vector = normalized_vector.flatten()
    dot_product = np.dot(flat_normalized_261, flat_vector)
    print('Normal dot product w/ img_261.jpg and ', key, ': ', dot_product)
    total_2 += dot_product
avg_2 = total_2 / 10
print('\n')
    
#compute the dot product of img_261 with 10 images of 9 from the MNIST set
loaded_images_8 = load_images('trainingSet/9')
print('Dot products with 2 and 9 images:')
total_9 = 0
for i, (key, value) in enumerate(loaded_images_8.items()):
    if i == 10:
        break
    norm = np.linalg.norm(value)
    normalized_vector = value / norm
    flat_vector = normalized_vector.flatten()
    dot_product = np.dot(flat_normalized_261, flat_vector)
    print('Normal dot product w/ img_261.jpg and ', key, ': ', dot_product)
    total_9 += dot_product
avg_9 = total_9 / 10
print('\n', )
print('Average dot product with 2: ', avg_2)
print('Average dot product with 9: ', avg_9)
