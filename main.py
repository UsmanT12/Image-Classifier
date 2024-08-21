import numpy as np
from imageutils import * 
from supportFuncs import *
from ImageClass_helper import predict_class
from genutils import parse_command_line
            
def main():
    required_params = ['training_set_path', 'testing_set_path']
    optional_params = ['img_size', 'num_classes', 'threshold']
    default_values = {
        'img_size': (28, 28),
        'num_classes': 2,
        'threshold': 0.015
        }
    params_dict = parse_command_line(required_params, optional_params)
   
    if params_dict:
        # Validate and convert parameters
        for key, value in params_dict.items():
            if key == 'num_classes':
                value = int(value)
                if value < 2 or value > 10:
                    print(f"Error: Entered an invalid number of classes")
                    print(f"Expected: a number between 2 and 10")
                    return
            elif key == 'threshold':
                value = float(value)
                if value < 0 or value > 1.0:
                    print(f"Error: Entered an invalid threshold value")
                    print(f"Expected: value between 0 and 1.0")
                    return
            elif key == 'img_size':
                value = tuple(int(x.strip()) for x in value.split(','))
            params_dict[key] = value
        # Assign default values to optional parameters    
        for param, default_value in default_values.items():
            if param not in params_dict:
                params_dict[param] = default_value
             
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