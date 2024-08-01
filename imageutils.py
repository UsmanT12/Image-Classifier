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
def load_images(directory):
    dict = {}
    
    for i in os.listdir(directory):
        if i.lower().endswith('.jpeg') or i.endswith('.jpg'):
            image_path = os.path.join(directory, i)
            image = Image.open(image_path).convert('L')
            dict[i] = column_vector(np.array(image))
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
def create_sub(matrix):
    transpose = matrix.transpose()
    subspace = np.linalg.inv(transpose.dot(matrix))
    subspace = matrix.dot(subspace)
    subspace = subspace.dot(transpose)
    
    return subspace

#really simple subspace function for an image matrix
def create_sub_simple(matrix):
    averages = []
    for row in matrix:
        average = np.mean(row)
        averages.append(average)
    return averages
    
def project_image(image, subspace):
    projection = subspace.dot(image)
    return projection

#Function for showing an image in a graph
def show_image(img_arr):
    plt.imshow(img_arr, cmap='gray') 
    plt.show() 
    return None