# coding=UTF-8
from drawable import Drawable

class Layer(Drawable):
	'''
	Абстрактный класс слоя.

	Аттрибуты:
		visible - видим ли слой
		screen - экран, к которому принадлежит слой
	'''
	def __init__(self):
		Drawable.__init__(self)
		self.visible = True
		self.screen = None

	def on_add_to_screen(self):
		'''
		Метод, вызываемый при добавлении слоя к экрану.
		'''
		pass
