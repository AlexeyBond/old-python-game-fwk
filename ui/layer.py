# coding=UTF-8
from drawable import AbstractDrawable

class Layer(AbstractDrawable):
	'''
	Слой. Из слоёв состоит экран.
	'''
	_SCREEN_EVENTS = [
		'destroy',
		'vp:resize',
		'in:key:press',
		'in:key:release',
		'in:mouse:enter',
		'in:mouse:leave',
		'in:mouse:press',
		'in:mouse:release',
		'in:mouse:drag',
		'in:mouse:move',
		'in:mouse:scroll'
	]

	events = [
		('layer:add-to-screen','on_add_to_screen'),
		('layer:remove-from-screen','on_remove_from_screen')
	]

	def init(self,*args,**kwargs):
		self.screen = None

	@property
	def width(self):
		return self.screen.width

	@property
	def height(self):
		return self.screen.height

	def on_add_to_screen(self,screen):
		self.screen = screen

		self.subscribe(screen,*(self._SCREEN_EVENTS))

		self.trigger('vp:resize',0,0)

	def on_remove_from_screen(self):
		self.unsubscribe(objects=[self.screen])
		self.screen = None
