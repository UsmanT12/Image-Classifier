import numpy as np
from imageutils import * 
from matrix import *
from cosine_similarity import *
from genutils import parse_command_line
        
def precompute_classes_MNIST(training_set_path, testing_set_path):
    print("precompute_classes_MNIST")
    trained_arr = [
        DigitMatrix(f"{training_set_path}/0", '0'),
        DigitMatrix(f"{training_set_path}/1", '1'),
        DigitMatrix(f"{training_set_path}/2", '2'),
        DigitMatrix(f"{training_set_path}/3", '3'),
        DigitMatrix(f"{training_set_path}/4", '4'),
        DigitMatrix(f"{training_set_path}/5", '5'),
        DigitMatrix(f"{training_set_path}/6", '6'),
        DigitMatrix(f"{training_set_path}/7", '7'),
        DigitMatrix(f"{training_set_path}/8", '8'),
        DigitMatrix(f"{training_set_path}/9", '9')
    ]
    test_arr = [
        DigitMatrix(f"{testing_set_path}/0", '0'),
        DigitMatrix(f"{testing_set_path}/1", '1'),
        DigitMatrix(f"{testing_set_path}/2", '2'),
        DigitMatrix(f"{testing_set_path}/3", '3'),
        DigitMatrix(f"{testing_set_path}/4", '4'),
        DigitMatrix(f"{testing_set_path}/5", '5'),
        DigitMatrix(f"{testing_set_path}/6", '6'),
        DigitMatrix(f"{testing_set_path}/7", '7'),
        DigitMatrix(f"{testing_set_path}/8", '8'),
        DigitMatrix(f"{testing_set_path}/9", '9')
    ]
    print("precompute_classes_MNIST done")
    return trained_arr, test_arr

def precompute_classes(training_set_path, testing_set_path):
    trained_arr = []
    test_arr = []

    # Populate trained_arr
    train_dirs = sorted([d for d in os.listdir(training_set_path) if os.path.isdir(os.path.join(training_set_path, d))])
    for dir_name in train_dirs:
        digit = dir_name.split('/')[-1]
        trained_arr.append(DigitMatrix(f"{training_set_path}/{digit}", digit))

    # Populate test_arr
    test_dirs = sorted([d for d in os.listdir(testing_set_path) if os.path.isdir(os.path.join(testing_set_path, d))])
    for dir_name in test_dirs:
        digit = dir_name.split('/')[-1]
        test_arr.append(DigitMatrix(f"{testing_set_path}/{digit}", digit))

    return trained_arr, test_arr

def test_class(trained_arr, test_arr):
    correct_predictions = 0
    total_predictions = 0
    unique_classes = set([matrix.digit for matrix in trained_arr])
    class_accuracy = {str(i): {'correct': 0, 'total': 0} for i in unique_classes}
    
    for test_matrix in test_arr:
        for image_vector in test_matrix.img_dict.values():
            predicted = predict_class(trained_arr, image_vector)
            actual = test_matrix.digit
            print(f"Predicted class: {predicted}, Actual class: {actual}")
            if predicted == actual:
                correct_predictions += 1
                class_accuracy[actual]['correct'] += 1
            class_accuracy[actual]['total'] += 1
            total_predictions += 1

    accuracy = correct_predictions / total_predictions
    print(f"Correct predictions: {correct_predictions}")
    print(f"Wrong predictions: {total_predictions - correct_predictions}")
    print(f"Total predictions: {total_predictions}")
    print(f"Overall Accuracy: {accuracy * 100:.2f}%")
    
    for digit, stats in class_accuracy.items():
        class_acc = (stats['correct'] / stats['total']) * 100 if stats['total'] > 0 else 0
        print(f"Accuracy for class {digit}: {class_acc:.2f}%")
 
def precompute_classes_dogs_cats(training_set_path, testing_set_path):
     trained_arr = [
        DigitMatrix(f"{training_set_path}/cats", 'cats'),
        DigitMatrix(f"{training_set_path}/dogs", 'dogs'),
     ]
     
     test_arr = [
        DigitMatrix(f"{testing_set_path}/cats", 'cats'),
        DigitMatrix(f"{testing_set_path}/dogs", 'dogs'),
     ]
     
     return trained_arr, test_arr
            

def main(training_set_path, testing_set_path):
    #required_params = ['trainingSet', 'testingSet']
    #optional_params = ['imgSize']
    params_dict = parse_command_line(required_params, optional_params)
    
    trained_arr, test_arr = precompute_classes(training_set_path, testing_set_path)
    test_class(trained_arr, test_arr)


if __name__ == "__main__":
    #training_set_path = "dog_cat_trainingSet"
    #testing_set_path = "dog_cat_testSet"
    #training_set_path = "trainingSet"
    #testing_set_path = "testSet"
    training_set_path = input("Enter the path to the training set: ")
    testing_set_path = input("Enter the path to the testing set: ")
    main(training_set_path, testing_set_path)  
