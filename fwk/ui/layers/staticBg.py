# coding=UTF-8
from fwk.ui.layer import Layer
from fwk.util import *

class StaticBackgroundLauer(Layer):
	'''
	Слой статического заднего фона.
	'''

	def __init__(self,imgpath,mode='fit'):
		'''
		Конструктор.

		Параметры:
			imgpath - путь к файлу изображения
			mode - одно из следующих значений:
				'fit' - изображение растягивается на весь экран
				'center' - изображение по центру
				'scale' - на весь экран с соблюдением пропорций
				'fill' - на весь экран с соблюдением пропорций
					и полным заполнением пространства
		'''
		Layer.__init__(self)
		self.mode = mode
		self.texture = LoadTexture(imgpath)
		self.recalc( )
		self.tx = 0
		self.ty = 0
		self.tw = self.width
		self.th = self.height

	def recalc(self):
		'''
		Метод, вычисляющий параметры наложения текстуры - коорддинаты и размер.

		Прочтение вслух исходного кода данного метода способно вызвать самого сатану.
		'''
		#TODO: Использовать паттерн "Стратегия" для пущщей абстрактности и читабельности (и чтобы не беспокоить дьявола).
		if self.mode == 'fit':
			self.tx = 0
			self.ty = 0
			self.tw = self.width
			self.th = self.height
			return
		cx = self.width // 2
		cy = self.height // 2
		hw = self.texture.width // 2
		hh = self.texture.height // 2
		if self.mode == 'center':
			self.tx = cx - hw
			self.ty = cy - hw
			self.tw = self.texture.width
			self.th = self.texture.height
		elif (self.mode == 'scale') or (self.mode == 'fill'):
			fill = (self.mode == 'fill')
			tw = float(self.texture.width)
			th = float(self.texture.height)
			sw = float(self.width)
			sh = float(self.height)
			if sh == 0 or sw == 0:
				return
			tr = tw / th
			sr = sw / sh
			if tr == sr:
				self.tx = 0
				self.ty = 0
				self.tw = self.width
				self.th = self.height
			elif (tr > sr) != fill:
				self.tx = 0
				self.tw = self.width
				hh = hh * (sw / tw)
				self.ty = int(cy - hh)
				self.th = int(hh * 2)
			elif (tr < sr) != fill:
				self.ty = 0
				self.th = self.height
				hw = hw * (sh / th)
				self.tx = int(cx - hw)
				self.tw = int(hw * 2)

	def on_resize(self,width,height):
		'''
		Метод, вызываемый при изменении размера.

		Вызывает метод recalc.
		'''
		self.width = width
		self.height = height
		self.recalc( )

	def draw(self):
		'''
		Метод отрисовки.
		'''
		self.texture.blit(x=self.tx,y=self.ty,width=self.tw,height=self.th)
