import numpy as np
from imageutils import * 
from matrix import *
from cosine_similarity import *
from genutils import parse_command_line
        
def precompute_classes(training_set_path, testing_set_path, size, num_classes, threshold):
    trained_arr = []
    test_arr = []
    num = 0

    # Populate trained_arr
    train_dirs = sorted([d for d in os.listdir(training_set_path) if os.path.isdir(os.path.join(training_set_path, d))])
    for dir_name in train_dirs:
        if num >= num_classes:
            num = 0
            break
        digit = dir_name.split('/')[-1]
        trained_arr.append(DigitMatrix(f"{training_set_path}/{digit}", digit, size, threshold))
        num += 1
    
    num = 0    
    # Populate test_arr
    test_dirs = sorted([d for d in os.listdir(testing_set_path) if os.path.isdir(os.path.join(testing_set_path, d))])
    for dir_name in test_dirs:
        if num >= num_classes:
            num = 0
            break
        digit = dir_name.split('/')[-1]
        test_arr.append(DigitMatrix(f"{testing_set_path}/{digit}", digit, size, threshold))
        num += 1

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
    
    for digit in sorted(class_accuracy.keys()):
        stats = class_accuracy[digit]
        class_acc = (stats['correct'] / stats['total']) * 100 if stats['total'] > 0 else 0
        print(f"Accuracy for class {digit}: {class_acc:.2f}% ({stats['correct']}/{stats['total']})")
            

def main():
    required_params = ['training_set_path', 'testing_set_path']
    optional_params = ['img_size', 'num_classes', 'threshold']
    params_dict = parse_command_line(required_params, optional_params)
   
    if params_dict:
        training_set_path = params_dict['training_set_path']
        testing_set_path = params_dict['testing_set_path']
        size = params_dict['img_size']
        num_classes = params_dict['num_classes']
        threshold = params_dict['threshold']
        
        trained_arr, test_arr = precompute_classes(training_set_path, testing_set_path, size, num_classes, threshold)
        test_class(trained_arr, test_arr)
    else:
        print("Empty dictionary returned")


if __name__ == "__main__":
    main()  