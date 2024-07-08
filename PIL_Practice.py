#Practice with Pillow library
import numpy as np
from PIL import Image
import os

size_200 = (200, 200)  

im = Image.open('usman_pic copy.jpg')
im.show()
for f in os.listdir('.'):
    if f.endswith('.jpg'):
        i = Image.open(f)
        fn, text = os.path.splitext(f)
        
        #adds all images in repo to the 200 folder as a size 200x200
        i.thumbnail(size_200)
        i.save('200/{}_200{}'.format(fn, text))
        
