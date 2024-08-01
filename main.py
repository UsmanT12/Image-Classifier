import numpy as np
from imageutils import * 
from matrix import *
from cosine_similarity import *

def main():
    one = DigitMatrix("trainingSet/1", '1')
    two = DigitMatrix("trainingSet/2", '2')
    three = DigitMatrix("trainingSet/3", '3')
    four = DigitMatrix("trainingSet/4", '4')
    five = DigitMatrix("trainingSet/5", '5')
    six = DigitMatrix("trainingSet/6", '6')
    seven = DigitMatrix("trainingSet/7", '7')
    eight = DigitMatrix("trainingSet/8", '8')
    nine = DigitMatrix("trainingSet/9", '9')
    zero = DigitMatrix("trainingSet/0", '0')
    trained_arr = [zero, one, two, three, four, five, six, seven, eight, nine]
    
    test_zero = DigitMatrix("testSet/0", '0')
    test_one = DigitMatrix("testSet/1", '1')
    test_two = DigitMatrix("testSet/2", '2')
    test_three = DigitMatrix("testSet/3", '3')
    test_four = DigitMatrix("testSet/4", '4')
    test_five = DigitMatrix("testSet/5", '5')
    test_six = DigitMatrix("testSet/6", '6')
    test_seven = DigitMatrix("testSet/7", '7')
    test_eight = DigitMatrix("testSet/8", '8')
    test_nine = DigitMatrix("testSet/9", '9')
    test_arr = [test_zero, test_one, test_two, test_three, test_four, test_five, test_six, test_seven, test_eight, test_nine]
    
    correct_predictions = 0
    total_predictions = 0
    class_accuracy = {str(i): {'correct': 0, 'total': 0} for i in range(10)}
    
    for test_matrix in test_arr:
        for image_vector in test_matrix.img_dict.values():  # Assuming each DigitMatrix has a 'dict' attribute with image vectors
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
    print(f"Accuracy: {accuracy * 100:.2f}%")

    for digit, stats in class_accuracy.items():
        class_acc = (stats['correct'] / stats['total']) * 100 if stats['total'] > 0 else 0
        print(f"Accuracy for class {digit}: {class_acc:.2f}%")


if __name__ == "__main__":
    main()