#genutils.lib
import sys

    #Generic utility for parsing command-line params into a dict . It should take in lists of required and optional params. Optional params should be mapped to default values in the call. It should only succeed if the command-line satisfies the param requirements. On success, it should return a dict mapping each param to its assigned value. This will be a nice, reusable utility for all your Python programming.
def parse_command_line_params(required_params, optional_params):
    params_dict = {}
    args = sys.argv[1:]
    
    #Check if the number of arguments is correct
    if len(args) < len(required_params):
        raise ValueError("Not all required parameters are provided")
    
    # Assign values to required parameters
    for i, param in enumerate(required_params):
        params_dict[param] = args[i]

    # Assign values to optional parameters
    for param, default_value in optional_params.items():
        if param in args:
            params_dict[param] = args[args.index(param) + 1]
        else:
            params_dict[param] = default_value

    return params_dict