#genutils.lib
import sys

    #Generic utility for parsing command-line params into a dict . It should take in lists of required and optional params. Optional params should be mapped to default values in the call. It should only succeed if the command-line satisfies the param requirements. On success, it should return a dict mapping each param to its assigned value. This will be a nice, reusable utility for all your Python programming.
def parse_command_line_params(required_params, optional_params):
    params_dict = {}
    args = sys.argv[1:]
    default_values = {'image_size': 28,
                      'image_length': 784}
    
    # Create a usage line for checking if the number of arguments is correct
    usage_message = f"Usage: {sys.argv[0]} " + " ".join(required_params)
    if optional_params:
        usage_message += " [" + " ".join(f"--{param} <value>" for param in optional_params) + "]"
    
    # Check if the number of arguments is correct
    if len(args) < len(required_params):
        raise ValueError(f"Not all required parameters are provided.\n{usage_message}")
    
    # Assign values to required parameters
    for i, param in enumerate(required_params):
        params_dict[param] = args[i]

    # Assign values to optional parameters
    for param in optional_params:
        if f"--{param}" in args:
            param_index = args.index(f"--{param}")
            if param_index + 1 < len(args):
                params_dict[param] = args[param_index + 1]
            else:
                raise ValueError(f"Value for optional parameter '{param}' is missing")
        else:
            print(f"Optional parameter --{param} not found, setting to default value")
            params_dict[param] = default_values.get(param, None)
            
    return params_dict