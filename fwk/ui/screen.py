# coding=UTF-8
from drawable import Drawable

class AppScreen(Drawable):
	'''
	Абстрактный класс экрана.

	Аттрибуты:
		layers - список слоёв, из которых состоит экран
		next - экран, к которому необходимо перейти при первой же возможности
		need_exit - необходимо ли завершить работу приложения.
		keep_prevous - необходимо ли хранить ссылку на предидущий экран
		prevous - ссылка на предидущий экран либо None
	'''

	SCREEN_CLASSES = {}

	@staticmethod
	def new(classname,*args,**kwargs):
		'''
		Статический метод, создающий новый экран по короткому обозначению класса.
		'''
		if classname in AppScreen.SCREEN_CLASSES:
			return AppScreen.SCREEN_CLASSES[classname](*args,**kwargs)
		else:
			return None

	def __init__(self):
		Drawable.__init__(self)

		self.layers = []
		self.next = None
		self.need_exit = False
		self.keep_prevous = False
		self.prevous = None

	def activate(self,prevous):
		'''
		Метод, активирующий экран.
		'''
		if prevous != None and not self.keep_prevous:
			prevous.exit( )
			prevous.next = None
		else:
			if self.prevous != None:
				self.prevous.exit( )
			self.prevous = prevous

	def on_activate(self):
		'''
		Метод, вызываемый когда экран становится активным.
		'''
		pass

	def set_next(self,classname,*args,**kwargs):
		'''
		Метод, создающий новый экран, который затем станет активным
		'''
		self.next = AppScreen.new(classname,*args,**kwargs)

	def go_back(self):
		'''
		Вернуться к предидущему экрану, если ссылка сохранена
		'''
		if self.prevous != None:
			self.next = self.prevous

	def dispatch_event(self,event_type,*args):
		'''
		Диспечер событий.
		'''
		if event_type in dir(self):
			getattr(self,event_type)(*args)
		for layer in self.layers:
			if event_type in dir(layer):
				getattr(layer,event_type)(*args)

	def draw(self):
		'''
		Метод отрисовки.
		'''
		for layer in self.layers:
			if layer.visible:
				layer.draw( )

	def on_resize(self,width,height):
		'''
		Метод, вызываемый при изменении размера.
		Изменяет размеры слоёв.
		'''
		for layer in self.layers:
			layer.resize(width,height)

	def addLayer(self,layer):
		'''
		Метод, добавляющий слой к экрану.
		Вызывает on_add_to_screen у слоя.
		'''
		self.layers.append(layer)
		layer.screen = self
		layer.on_add_to_screen()
		layer.resize(self.width,self.height)

	def exit(self):
		'''
		Метод, вызываемый при уничтожении экрана.
		'''
		if self.prevous != None:
			self.prevous.exit( )

	@staticmethod
	def ScreenClass(cname):
		'''
		Декоратор, дающий классу экрана короткое обозначение.

		Пример использования:

		AppScreen.ScreenClass('MySuperScreen')
		class MySuperScreen(AppScreen):
			...
		'''
		def ScreenClassDecorator(sclass):
			AppScreen.SCREEN_CLASSES[cname] = sclass
			return sclass
		return ScreenClassDecorator
