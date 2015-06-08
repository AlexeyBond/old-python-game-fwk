# coding=UTF-8

class Drawable:
	'''
	Абстрактный класс для экранов и слоёв.

	Имеет размеры (width, height), метод их изменения (resize),
	и метод отрисовки.
	'''
	def __init__(self):
		self.height = 0
		self.width = 0

	def resize(self,width,height):
		'''
		Метод, изменяющий размеры.

		Если размеры действительно изменяются, то вызывает on_resize
		с новыми значениями размеров в качестве параметров
		(фактические размеры изменяются после вызова on_resize)
		'''
		if self.width != width or self.height != height:
			self.on_resize(width,height)
			self.width = width
			self.height = height

	def draw(self):
		'''
		Метод отрисовки.

		Не принимает параметров.
		'''
		pass

	def on_resize(self,width,height):
		'''
		Метод, вызываемый при фактическом изменении размеров.

		Новые размеры передаются как параметры. Старые размеры
		хранятся полях объекта.
		'''
		pass
