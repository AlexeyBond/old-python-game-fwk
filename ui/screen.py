# coding=UTF-8
from fwk.ui.drawable import AbstractDrawable

class Screen(AbstractDrawable):
	'''
	Экран.

	Экран опреденяет, поведение приложения - что рисовать в окне, как
		реагировать на события ввода.
	'''

	def init(self,*args,**kwargs):
		self.width = 1
		self.height = 1

		self.layers = []

		self._prevous = None
		self.next = None
		self.keep_prevous = False
		self.exit_required = False

	def draw(self):
		for layer in self.layers:
			if layer._visible:
				layer.draw()

	def resize(self,width,height):
		'''
		Метод вызывается окном при изменении размера. Лучше бы его не
			перегружать, а использовать событие vp:resize.

		О размерах вообще:
		Из всех Drawable о размере окна знает только экран (поля width и
			height). Получение этих свойств у слоя происходит через обращение
			к экрану. Попытка присвоить width или height у слоя может привести
			к непредсказуемым последствиям.
		'''
		oldWidth, oldHeight = self.width, self.height
		self.width, self.height = width, height
		self.trigger('vp:resize',oldWidth,oldHeight)

	def pushLayerFront(self,layer,show=True):
		'''
		Добавляет слой к экрану спереди.

		Порядок обработки событий слоями определяется порядком их добавления.
		'''
		# Спереди - то, что рисуерся последним и добавляется, соответственно, в
		# 	зад списка. Логика.
		self.layers.append(layer)
		layer.trigger('layer:add-to-screen',self)
		layer.show(show)
		return self

	def pushLayerBack(self,layer,show=True):
		'''
		Добавляет слой к экрану сзади.

		Порядок обработки событий слоями определяется порядком их добавления.
		'''
		self.layers.insert(0,layer)
		layer.trigger('layer:add-to-screen',self)
		layer.show(show)
		return self

	def requireExit(self):
		'''
		Вызывается экраном, когда он считает, что пора закрыть окно приложения.
		'''
		self.exit_required = True

	def activate(self,prevous):
		'''
		Метод, вызываемый окном при переключении с экрана prevous на этот.
		'''
		self._prevous = None

		if prevous is not None:
			prevous.hide()
			if self.keep_prevous:
				self._prevous = prevous
				prevous.next = None
			else:
				prevous.trigger('destroy')

	_SCREEN_CLASSES = {}

	@staticmethod
	def ScreenClass(cname):
		'''
		Декоратор, дающий классу экрана короткое обозначение.

		Пример использования:

		Screen.ScreenClass('MySuperScreen')
		class MySuperScreen(Screen):
			...
		'''
		def ScreenClassDecorator(sclass):
			Screen._SCREEN_CLASSES[cname] = sclass
			return sclass
		return ScreenClassDecorator

	@staticmethod
	def new(clazz,*args,**kwargs):
		'''
		Статический метод для создания нового экрана.
		'''
		return Screen._SCREEN_CLASSES[clazz](*args,**kwargs)
