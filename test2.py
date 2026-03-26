from PIL import Image
import numpy as np
from constants import *

def coord_from_pixels(color, image):
	pim = Image.open(image).convert('RGB')
	im  = np.array(pim)
	color = color #RBG
	Y, X = np.where(np.all(im==color,axis=2))
	
	return X, Y
	
print((coord_from_pixels(YELLOW, "test.png"))

	
