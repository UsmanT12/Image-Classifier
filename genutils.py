#genutils.lib
import sys

#Generic utility for parsing command-line params into a dict . It should take in lists of required and optional params. Optional params should be mapped to default values in the call. It should only succeed if the command-line satisfies the param requirements. On success, it should return a dict mapping each param to its assigned value. This will be a nice, reusable utility for all your Python programming.
def parse_command_line(required_params, optional_params):
    params_dict = {}
    args = sys.argv[1:]
    default_values = {'img_size': (28, 28),
                      'num_classes': ['0', '4']}
    
    # Create a usage line for checking if the number of arguments is correct
    usage_message = f"Usage: {sys.argv[0]} " + " ".join(required_params)
    if optional_params:
        usage_message += " [" + " ".join(f"--{param} <value>" for param in optional_params) + "]"
    
    # Check if the number of arguments is correct
    if len(args) < len(required_params):
        raise ValueError(f"Not all required parameters are provided.\n{usage_message}")
    
    # Assign values to required parameters
    for param in args:
        param = param.split('=')
        if not param[1] and param[0] in optional_params:
            break
        if not param[1] and param[0] in required_params:
            print(f"Error: Enter the value for {param[0]}.")
            return {}
        if param[0] == 'imgSize':
            param[1] = tuple(int(x.strip())for x in param[1].split(','))
            print(f"param 1 = {param[1]}")
        if param[0] == 'num_classes':
            num_classes = int(param[1])
            if num_classes < 2 or num_classes > 10:
                print(f"Error: Enter a valid number for num_classes")
                continue
        if param[0] == 'classes':
           param[1]=[x.strip() for x in param[1].split(',')]
           print(f"classes{param[1]}")
        params_dict[param[0]] = param[1]
    
    for param in required_params:
        if param not in params_dict:
            print(f"Error: Missing required parameter: {param}.")
            return {}
    for param, default_value in default_values.items():
        if param not in params_dict:
            params_dict[param] = default_value
            print(f"assigned default value for {param}")
            
    return params_dict

'''
def main():
    required_params = ['class_path_1', 'class_path_2']
    optional_params = ['imgSize']
    
    try:
        result = parse_command_line(required_params, optional_params)
        print("Test case result:", result)
    except Exception as e:
        print("Test case failed:", e)

if __name__ == "__main__":
     main()
'''