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
    for i in range(len(classes)):
        projection_vector = project_image(test_image, classes[i].embedding) #classes[i].getSubspace().dot(test_image)
        cos_sim = abs(cosine_similarity(test_image, projection_vector))
        if cos_sim > highest:
            highest = cos_sim
            predicted_class = classes[i].digit
    return predicted_class

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

#create subspace of a class with the column image matrix
def create_sub(A):
    A_transpose = np.transpose(A)
    AT_A = np.dot(A_transpose, A)
    AT_A_inv = np.linalg.pinv(AT_A)
    A_AT_A_inv = np.dot(A, AT_A_inv)
    embedding_matrix = np.dot(A_AT_A_inv, A_transpose)
    
    return embedding_matrix