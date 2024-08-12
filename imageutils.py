#imageutils.libs
import numpy as np
import os
from PIL import Image

#Resizes and grayscales an image
def resize_image(image1, size1, size2):
    #create the correct size tuple and resize image
    image = Image.open(image1)

    if size2 == None:
        image = image.resize((size1, size1))
    elif size1 != None and size2 != None:
        image = image.resize((size1, size2))
    
    #Grayscale image
    gray_array = np.array(image.convert('L'))
    return gray_array
    
#Creates a column vector from a 2D array
def column_vector(array):
    arr = np.array(array)
    column_vector = arr.reshape(-1, 1)
    return column_vector

#Loads a directory full of JPEG images into a dict (filename -> vectorized image)
def load_images(directory, size1, size2):
    dict = {}
    
    for i in os.listdir(directory):
        if i.lower().endswith('.jpeg') or i.endswith('.jpg'):
            image_path = os.path.join(directory, i)
            resized_image = resize_image(image_path, size1, size2)
            dict[i] = column_vector(resized_image)
    return dict


#Load images vectors into a 2D matrix, with each image vector as a column
def combine_matrix(dict):
    arr = []
    
    for i in dict.values():
        arr.append(i)
    arr = np.column_stack(arr)
    return arr

#Combines vectorized images into a matrix where every image is a column
def combine_vectors(vector1, vector2):
    matrix = np.hstack((vector1, vector2))
    return matrix

#create subspace of a class with the column image matrix
def create_sub(A):
    if A.size == 0:
        raise ValueError("Input matrix A is empty")

    A_transpose = np.transpose(A)
    AT_A = np.dot(A_transpose, A)
    AT_A_inv = np.linalg.pinv(AT_A)
    A_AT_A_inv = np.dot(A, AT_A_inv)
    embedding_matrix = np.dot(A_AT_A_inv, A_transpose)
    
    return embedding_matrix
    
def project_image(image, embedding):
    projection = np.dot(embedding, image)
    return projection

#Function for showing an image in a graph
def show_image(img_arr):
    plt.imshow(img_arr, cmap='gray') 
    plt.show() 
    return None


#really simple subspace function for an image matrix
def create_sub_simple(matrix):
    averages = []
    for row in matrix:
        average = np.mean(row)
        averages.append(average)
    return averages