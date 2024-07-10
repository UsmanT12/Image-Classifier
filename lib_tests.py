from imageutils import *
from genutils import *
import numpy as np
from PIL import Image
import os
import sys

#Tests for functions from imageutils.py
image = Image.open('usman_pic copy.jpg')
'''
print (resize_image('usman_pic copy.jpg', 200, 200))
print(np.array(image))
print('************')
print(column_vector(image))
'''

'''
#Test for load_images
try:
    loaded_images = load_images('JPEG')
    print("Images loaded successfully.")
    print(loaded_images)
except FileNotFoundError:
    print("Directory 'JPEG' not found.")
except Exception as e:
    print(f"Error loading images: {e}")
'''

