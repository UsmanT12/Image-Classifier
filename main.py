import numpy as np
from imageutils import * 
from supportFuncs import *
from DigitMatrix_helper import predict_class
from genutils import parse_command_line
            
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
        usage_message = f"python main.py " + " ".join(f"{param}='<directory>'" for param in required_params)
        if optional_params:
            usage_message += " [" + " ".join(f"{param}=<value>" for param in optional_params) + "]"
        print(f"Expected Usage: {usage_message}")

    return


if __name__ == "__main__":
    main()  