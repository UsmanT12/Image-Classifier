imageutils.py is a library that holds function for creating image vectors
genutils.py is a library with one function that parses command-line params into a dict
supportFuncs.py holds functions for training and testing data
ImageClass.py holds the class data for images
ImageClass_helper.py holds the helper functions for the ImageClass class
main.py has the main functions that is run from parsing a commandline script

To run the program:
  Required: enter the the directory to the training and testing sets of classes that hold images for those classes.
  Optional: enter image size, number of classes (2-10), and threshold percent
  Expected Usage: python main.py training_set_path='<directory>' testing_set_path='<directory>' [img_size=<value> num_classes=<value> threshold=<value>]
