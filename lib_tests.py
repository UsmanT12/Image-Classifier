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



#Tests for the genutils.py functions
def main():
    required_params = ['input_file', 'output_file']
    optional_params = ['image_size', 'image_length']
    
    try:
        params = parse_command_line_params(required_params, optional_params)
        print("Parsed parameters:", params)
    except ValueError as e:
        print("Error:", e)

if __name__ == "__main__":
    main()


'''
***************************
'''

'''
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
'''

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
dict = load_images('trainingSet/2')
arr = combine_matrix(dict)
#print(arr)
'''

'''
#Image column vector matrix test
arr1 = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]]
arr2 = [[16, 17, 18, 19, 20], [21, 22, 23, 24, 25], [26, 27, 28, 29, 30]]
arr3 = [[31, 32, 33, 34, 35], [36, 37, 38, 39, 40], [41, 42, 43, 44, 45]]
arr4 = [[46, 47, 48, 49, 50], [51, 52, 53, 54, 55], [56, 57, 58, 59, 60]]

column_vector1 = column_vector(arr1)
column_vector2 = column_vector(arr2)
column_vector3 = column_vector(arr3)
column_vector4 = column_vector(arr4)

dict1 = {'1': column_vector1, '2': column_vector2, '3': column_vector3, '4': column_vector4}

#print(column_vector1)
array_test = combine_matrix(dict1)
print(array_test)
'''