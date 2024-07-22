#Functions and tests for cosine similarity of image vectors 
import sys
import numpy as np

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
    #print(amount, 'dot products with ', image1 + '(' + str(number_set1) + ')', 'and', number_set2, 'images:')
    total = 0
    image = Image.open('trainingSet/' + str(number_set1) + '/' + image1)
    image = np.array(image)
    image_vector = column_vector(np.array(image))
    
    dict = load_images('trainingSet/' + str(number_set2))
    for i, (key, value) in enumerate(dict.items()):
        if i == amount:
            break
        dot_product = cosine_similarity(image_vector, value)
        #print('Normal dot product w/ ', image1, ' and ', key, ': ', dot_product)
        total += abs(dot_product)
    average = total / amount
    print('Average cosine similarity of image', image1, '(' + str(number_set1) + ')', 'with class', str(number_set2), 'with', amount, ' images: ', average, '\n')
    return

#function that computes the cosine similarities of the different images in the same set
def cosine_similarity_same_set(number_set, amount, dict):
    total = 0
    dict = load_images('trainingSet/' + str(number_set))
    comparisons = 0
    
    for i, (key, value) in enumerate(dict.items()):
        if i >= amount:
            break
        for j, (key2, value2) in enumerate(dict.items()):
            if j >= i or j >= amount:
                continue
            image1_vector = column_vector(np.array(value))
            image2_vector = column_vector(np.array(value2))
            dot_product = cosine_similarity(image1_vector, image2_vector)
            #print('Normal dot product w/ ', key, ' and ', key2, ': ', dot_product)
            total += abs(dot_product)
            comparisons += 1
            #print(key, dot_product)

    average = total / comparisons
    print('Average cosine similarity of', number_set, 'class with same set of ', amount, 'images', average, '\n')
    return

#function that returns the subspace matrix for a class given the column image matrix
def subspace(matrix):
    transpose = matrix.transpose()
    transpose = transpose.dot(matrix)
    transpose = np.linalg.inv(transpose)
    transpose = matrix.dot(transpose)
    final_matrix = transpose.dot(matrix.transpose())
    return final_matrix

#function that computes the cosine simmilarities for a table when given a matrix
def analysis_all(matrix):
    # Compute the dot product of the transposed matrix and the original matrix
    dot_product = np.dot(matrix.T, matrix)
    
    # Calculate the norms of each column vector in the matrix
    norms = np.linalg.norm(matrix)
    norms = norms.reshape(-1, 1)
    
    # Compute the cosine similarity matrix
    cos_similarity = dot_product / (norms @ norms.T)
    cos_similarity = np.round(cos_similarity, 2)
    
    return cos_similarity