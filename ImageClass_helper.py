import numpy as np
from supportFuncs import *

#Projects image onto a subspace    
def project_image(image, embedding):
    projection = np.dot(embedding, image)
    return projection

#tests cos similarity of a test image across each subspace and chooses the subspace it projects in the most
def predict_class(classes, test_image):
    highest = 0
    predicted_class = None
    image_norm = np.linalg.norm(test_image)
    test_image = test_image / image_norm
    
    for i in range(len(classes)):
        projection_vector = project_image(test_image, classes[i].embedding)
        length = np.linalg.norm(projection_vector)
        if length > highest:
            highest = length
            predicted_class = classes[i].name
    return predicted_class

#create subspace of a class with the column image matrix
def create_subspace(A):
    A_transpose = np.transpose(A)
    AT_A = np.matmul(A_transpose, A)
    AT_A_inv = np.linalg.inv(AT_A)
    A_AT_A_inv = np.matmul(A, AT_A_inv)
    embedding_matrix = np.matmul(A_AT_A_inv, A_transpose)
    
    return embedding_matrix

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