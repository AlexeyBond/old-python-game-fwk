# coding=UTF-8
from fwk.ui.layer import Layer
from fwk.util import *

### Слой, рисующий элемент гуя.
class GUIItemLayer(Layer):
	# offset_* - отступ элемента по оси.
	#  Если 0 - элемент распологается по центру.
	#  Если < 0 - отступ от края с большей координатой.
	def __init__(self,offset_x,offset_y,width,height,pad_x=0,pad_y=0):
		Layer.__init__(self)

		self.offset_x = offset_x
		self.offset_y = offset_y

		self.pad_x = pad_x
		self.pad_y = pad_y

		self.mouse_in = False

		# Прямоугольник (x,y,ширина,высота)
		self.rect = [0,0,width,height]

		self.update_rect( )

	# Проверяет, находится ли точка в прямоугольнике элемента
	def pointInRect(self,x,y):
		return (x >= self.rect[0]) and (
				x <= (self.rect[2]+self.rect[0])) and (
				y >= self.rect[1]) and (
				y <= (self.rect[3]+self.rect[1]))
	#
	def draw(self):
		if GAME_CONSOLE.visible:
			glBegin(GL_LINE_LOOP)
			glVertex2i(self.rect[0],self.rect[1])
			glVertex2i(self.rect[0]+self.rect[2],self.rect[1])
			glVertex2i(self.rect[0]+self.rect[2],self.rect[1]+self.rect[3])
			glVertex2i(self.rect[0],self.rect[1]+self.rect[3])
			glEnd( )

	#
	def on_resize(self,width,height):
		if self.offset_x == 0:
			self.rect[0] = width // 2 - self.rect[2] // 2
		elif self.offset_x < 0:
			self.rect[0] = width + self.offset_x - self.rect[2]
		else:
			self.rect[0] = self.offset_x

		if self.offset_y == 0:
			self.rect[1] = height // 2 - self.rect[3] // 2
		elif self.offset_y < 0:
			self.rect[1] = height + self.offset_y - self.rect[3]
		else:
			self.rect[1] = self.offset_y

		self.rect[0] += self.pad_x
		self.rect[1] += self.pad_y

	#
	def update_rect(self):
		GUIItemLayer.on_resize(self,self.width,self.height)

	#
	def move(self,offset_x,offset_y):
		self.offset_x = offset_x
		self.offset_y = offset_y
		self.update_rect( )

	#
	def setSize(self,width,height):
		self.rect[2] = width
		self.rect[3] = height
		self.update_rect( )

	#
	def on_mouse_motion(self,x,y,dx,dy):
		ni = self.pointInRect(x,y)

		if self.mouse_in and (not ni):
			self.on_element_mouse_leave( )
			self.mouse_in = False
		elif (not self.mouse_in) and ni:
			self.on_element_mouse_enter( )
			self.mouse_in = True

	def on_element_mouse_leave(self):
		GAME_CONSOLE.write('Mouse leave!')

	def on_element_mouse_enter(self):
		GAME_CONSOLE.write('Mouse enter!')
