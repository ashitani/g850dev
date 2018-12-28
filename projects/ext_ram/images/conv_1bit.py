
import glob
#import PIL
#from PIL import Image, ImageFilter
import os
import cv2

import numpy as np

source_path="spaceship"
dest_path="spaceship_1bit"
frame_decimation=1

index = 1
out_index=0
nega=True

while(True):
    f=source_path+"/%04d.png"% index
    fb=os.path.basename(f)

    im = cv2.imread(f,0) # load as grayscale

    if type(im)==type(None):
        break

    if nega==True:
        _,im = cv2.threshold(im,180,255,cv2.THRESH_BINARY_INV)
    else:
        _,im = cv2.threshold(im,10,255,cv2.THRESH_BINARY)
    im = (im.astype(np.uint8))*255*255 #??
    #print(np.max(im))

    print(out_index)
    cv2.imwrite(dest_path+"/%04d.png"%out_index, im)
    index+=frame_decimation
    out_index+=1
