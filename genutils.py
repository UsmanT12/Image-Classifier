#genutils.lib
import sys

#Generic utility for parsing command-line params into a dict . It should take in lists of required and optional params. Optional params should be mapped to default values in the call. It should only succeed if the command-line satisfies the param requirements. On success, it should return a dict mapping each param to its assigned value. This will be a nice, reusable utility for all your Python programming.
def parse_command_line(required_params, optional_params):
    params_dict = {}
    args = sys.argv[1:]
    
    # Check if the number of arguments is correct
    if len(args) < len(required_params):
        print(f"Error: Missing required arguments.")
        return None
    
    # Assign values to required parameters
    for arg in args:
        param = arg.split('=')
        if len(param) != 2:
            print(f"Error: Invalid argument format")
            return None
        key, value = param[0], param[1]
        if key not in optional_params and key not in required_params:
            print(f"Error: Invalid parameter: {key}")
            return None
        elif key in optional_params and not value:
            continue
        elif key in required_params and not value:
            print(f"Error: Enter the value for {key}. first")
            return None
        params_dict[key] = value
    
    #Check if all required parameters are present
    for param in required_params:
        if param not in params_dict:
            print(f"Error: Missing required parameter: {param}.")
            return None

    return params_dict