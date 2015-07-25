# coding=UTF-8
from fwk.ui.layer import Layer
from fwk.util.all import *

class StaticBackgroundLauer(Layer):
	'''
	Слой статического заднего фона.
	'''

	def init(self,imgpath,mode='fit'):
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
		self._mode = mode
		self.texture = LoadTexture(imgpath)

	def on_add_to_screen(self,screen):
		return self._recalc( )

	def _recalc__fit(self):
		return Rect(bottom=0,left=0,width=self.width,height=self.height)

	def _recalc__center(self):
		return self._recalc__fit().resize(width=self.texture.width,height=self.texture.height,origin='center-center')

	def _recalc__scale(self):
		return self._recalc__center() \
			.scale(min(float(self.width) / self.texture.width, float(self.height) / self.texture.height),origin='center-center')

	def _recalc__fill(self):
		return self._recalc__center() \
			.scale(max(float(self.width) / self.texture.width, float(self.height) / self.texture.height),origin='center-center')

	def _recalc(self):
		'''
		Метод, вычисляющий параметры наложения текстуры - коорддинаты и размер.
		'''
		self.texture_rect = getattr(self,'_recalc__'+self._mode)()

	def on_viewport_resize(self,*args):
		return self._recalc( )

	def draw(self):
		'''
		Метод отрисовки.
		'''
		BlitTextureToRect(self.texture,self.texture_rect)

	@property
	def mode(self):
		return self._mode

	@mode.setter
	def mode(self,mode):
		if ('_recalc__'+mode) not in dir(self):
			raise 'Programming error: unsupported background mode: {mode}'.format(**locals())
