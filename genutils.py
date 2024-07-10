#genutils.lib
import sys

    #In the genutils.lib, create a generic utility for parsing command-line params into a dict . It should take in lists of required and optional params. Optional params should be mapped to default values in the call. It should only succeed if the command-line satisfies the param requirements. On success, it should return a dict mapping each param to its assigned value. This will be a nice, reusable utility for all your Python programming.
def parse_command_line_params(required_params, optional_params):
    #Check if the number of argurments is less than the number of required parameters
    if len(sys.argv) - 1 < len(required_params):
        print("Usage: python3 <filename> " + " ".join(required_params) + " " + " ".join(["[" + param + "]" for param in optional_params]))
        sys.exit(1)
        
    #create a dictionary to store the parameters
    params = {}
    args = sys.argv[1:]
    
    # Parse required parameters
    for i, param in enumerate(required_params):
        params[param] = args[i]
    
    #parse optional parameters
    for param, default in optional_params.items():
        if param in args:
            index = args.index(param)
            if index + 1 < len(args):
                params[param] = args[index + 1]
            else:
                params[param] = default
        else:
            params[param] = default
    
    return params 