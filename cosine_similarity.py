#Functions and tests for cosine similarity of image vectors 
from imageutils import *
import sys

#function that computes the cosine similarity given 2 column vectors
def cosine_similarity(vec1, vec2):
    norm1 = np.linalg.norm(vec1)
    vec1 = vec1 / norm1
    norm2 = np.linalg.norm(vec2)
    vec2 = vec2 / norm2
    flat_vec1 = vec1.flatten()
    flat_vec2 = vec2.flatten()
    dot_product = np.dot(flat_vec1, flat_vec2)
    return dot_product

#function that computes the cosine similarity of n amount of images in the m number set
def cosine_similarity_set(image1, number_set1, number_set2, amount, dict):
    print(amount, 'dot products with ', image1 + '(' + str(number_set1) + ')', 'and', number_set2, 'images:')
    total = 0
    image = Image.open('trainingSet/' + str(number_set1) + '/' + image1)
    image = np.array(image)
    image_vector = column_vector(np.array(image))
    
    dict = load_images('trainingSet/' + str(number_set2))
    for i, (key, value) in enumerate(dict.items()):
        if i == amount:
            break
        dot_product = cosine_similarity(image_vector, value)
        print('Normal dot product w/ ', image1, ' and ', key, ': ', dot_product)
        total += dot_product
    return
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

#Normalized image for img_261.jpg (2)
loaded_images_2 = load_images('trainingSet/2')
image_261 = Image.open('trainingSet/2/img_261.jpg')
array_261 = loaded_images_2['img_261.jpg']
norm_261 = np.linalg.norm(array_261)
normalized_261 = array_261 / norm_261
flat_array_261 = normalized_261.flatten()
flat_normalized_261 = np.array(flat_array_261)
#print('Normalized image array: ', normalized_261)



#compute dot product of img_261.jpg vector with normalized image vector, restults with 1.0 
dot_261 = np.dot(flat_array_261, flat_normalized_261)
#print(dot_261)

#compute dot product of normalized image vector of img_261 and img_271
array_271 = loaded_images_2['img_271.jpg']
norm_271 = np.linalg.norm(array_271)
normalized_271 = array_271 / norm_271
flat_array_271 = normalized_271.flatten()
flat_normalized_271 = np.array(flat_array_271)
dot_271_261 = np.dot(flat_normalized_271, flat_normalized_261)
#print('Normal dot product w/ 261 and 271 = ', dot_271_261)

#compute the dot product of img_261 with 10 images of 9 from the MNIST set
loaded_images_9 = load_images('trainingSet/9')
print('Dot products with 2 and 9 images:')
total_9 = 0
for i, (key, value) in enumerate(loaded_images_9.items()):
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
#print('Average dot product with 2: ', avg_2)
#print('Average dot product with 9: ', avg_9)

loaded_images_1 = {}
cosine_similarity_set('img_261.jpg', 2, 9, 10, loaded_images_1)