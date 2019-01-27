from PIL import Image
from ctypes import c_float

class MapGen:

	def __init__(self, engine, imagePath):

		self.image = Image.open(imagePath)
		self.image_rgb = self.image.convert('RGB')

		if self.image.width == 0:
			print('Map failed to load!')
			return

		for y in range(128):
			for x in range(128):
				pixelRGB = self.image_rgb.getpixel((x,y))
				if pixelRGB != (255,255,255):
					engine.set_cell(x,y,c_float(1.0),1)
				else:
					engine.set_cell(x,y,c_float(0.0),0)

 
