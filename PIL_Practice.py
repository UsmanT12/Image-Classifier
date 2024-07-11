#Practice with Pillow library
import numpy as np
from PIL import Image
import os

size_200 = (200, 200)  
image = Image.open('usman_pic copy.jpg')

'''
im = Image.open('usman_pic copy.jpg')
im.show()

#for loop that creates a 200x200 version of all jpg images
for f in os.listdir('.'):
    if f.endswith('.jpg'):
        i = Image.open(f)
        fn, text = os.path.splitext(f)
        
        #adds all images in repo to the 200 folder as a size 200x200
        i.thumbnail(size_200)
        i.save('200/{}_200{}'.format(fn, text))
'''

'''
#create a temporary image then show it
purp = Image.new('RGB', (300, 300), 'purple')
purp.show()
print(purp.size)

#use the rotating and crop functions
rotated = image.rotate(45, expand = True, fillcolor = 'grey')
rotated.show()

crop = image.crop((425, 150, 875, 600))
crop.show()

#Convert image to a matrix
image_matrix = np.array(image)
print(image_matrix)

#Get individual RGB values from the image
#This creates a grey image
red = np.array(image.getchannel('R'))
blue = np.array(image.getchannel('B'))
green = np.array(image.getchannel('G'))

print(red)
print(blue)
print(green)

#grayscale image
gray_array = np.array(image.convert('L'))
'''