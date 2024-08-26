imageutils.py is a library that holds function for creating image vectors
genutils.py is a library with one function that parses command-line params into a dict

To run the program:
  Required: enter the the directory to the training and testing sets of classes that hold images for those classes.
  Optional: enter image size, number of classes (2-10), and threshold percent
  Expected Usage: python main.py training_set_path='<directory>' testing_set_path='<directory>' [img_size=<value> num_classes=<value> threshold=<value>]
