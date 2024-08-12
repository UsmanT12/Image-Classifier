#genutils.lib
import sys

#Generic utility for parsing command-line params into a dict . It should take in lists of required and optional params. Optional params should be mapped to default values in the call. It should only succeed if the command-line satisfies the param requirements. On success, it should return a dict mapping each param to its assigned value. This will be a nice, reusable utility for all your Python programming.
def parse_command_line(required_params, optional_params):
    params_dict = {}
    args = sys.argv[1:]
    default_values = {
        'img_size': (28, 28),
        'num_classes': 2,
        'threshold': 0.015
        }
    
    # Create a usage line for checking if the number of arguments is correct
    usage_message = f"Usage: {sys.argv[0]} " + " ".join(required_params)
    if optional_params:
        usage_message += " [" + " ".join(f"--{param} <value>" for param in optional_params) + "]"
    
    # Check if the number of arguments is correct
    if len(args) < len(required_params):
        raise ValueError(f"Not all required parameters are provided.\n{usage_message}")
    
    # Assign values to required parameters
    for arg in args:
        param = arg.split('=')
        if len(param) != 2:
            print(f"Error: Invalid argument format: {arg}. Expected format is param=value.")
            return {}
        key, value = param[0], param[1]
        if key in optional_params and not value:
            continue
        if key in required_params and not value:
            print(f"Error: Enter the value for {key}.")
            return {}
        if key == 'img_size':
            value = tuple(int(x.strip()) for x in value.strip('()').split(','))
        if key == 'num_classes':
            value = int(value)
            if value < 2 or value > 10:
                print(f"Error: Enter a valid number for num_classes")
                continue
        if key == 'threshold':
            value = float(value)
            if value < 0 or value > 1.0:
                print(f"Error: Enter a valid threshold value between 0 and 1.0")
                continue
        params_dict[key] = value
    
    for param in required_params:
        if param not in params_dict:
            print(f"Error: Missing required parameter: {param}.")
            return {}
    
    for param, default_value in default_values.items():
        if param not in params_dict:
            params_dict[param] = default_value
    
    return params_dict