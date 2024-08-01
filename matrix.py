import numpy as np
from imageutils import *
from cosine_similarity import *

class DigitMatrices:
    matrices = {}
    def __init__(self):
        None
      
    def add_object(self, DigitMatrix):
        self.matrices[DigitMatrix.digit] = DigitMatrix
    
    def printMatrix(self):
        print(f"Digit: {matrix.digit}")
        print(f"{matrix.cos_similarity}\n\n\n")
        

class DigitMatrix:
    digit = None
    path = ""
    img_dict = {}
    matrix = np.zeros(shape=(1,))
    #cos_similarity = np.zeros(shape=(0,))
    #row_avg = []
    subspace = []

    def __init__(self, path, digit):
        self.path = path
        self.digit = digit
        self.img_dict = load_images(path)
        self.matrix = combine_matrix(self.img_dict)
        self.subspace = self.set_subspace() 

    def set_subspace(self):
        self.subspace = create_sub_simple(self.matrix)
        return self.subspace
    
    def setMatrix(self):
        self.matrix = combine_matrix(self.img_dict)
            
    def getDict(self):
        return self.img_dict
    
    def getMatrix(self):
        return self.matrix
    
    def getSubspace(self):
        return self.subspace
    
    def printMatrix(self):
        print(f"Digit: {self.digit}")
        print(f"Matrix: {self.subspace}\n")
        #print(f"Image Dictionary: {self.img_dict}\n")
    

    '''
    def setRowAverage(self):
        self.row_avg = np.mean(self.cos_similarity, axis=1)
        self.row_avg = np.round(self.row_avg, 2)
   
    def setRepImg(self):
        index = np.argmax(self.row_avg)
        # self.img_dict[index]
        print(f"Representative image index for digit {self.digit}: {index}")
        
    def show_matrix(self):
       generate_html_table(list(self.img_dict.keys), self.cos_similarity)
    '''

#tests cos similarity of a test image across each subspace and chooses the subspace it projects in the most
def predict_class(classes, test_image):
    highest = 0
    predicted_class = None
    for i in range(len(classes)):
        #print (f"Class: {classes[i].digit}")
        projection_vector = classes[i].getSubspace()    #.dot(test_image)
        cos_sim = abs(cosine_similarity(test_image, projection_vector))
        #print(f"cos_sim for {classes[i].digit}: {cos_sim}")
        if cos_sim > highest:
            highest = cos_sim
            predicted_class = classes[i].digit
    return predicted_class