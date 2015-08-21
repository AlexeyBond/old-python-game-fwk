# coding=UTF-8
from fwk.util.all import *

class AbstractDrawable(Events):
	'''
	Интерфейс для чего-то, что можно нарисовать в окне.

	События:
		vp:resize(on_resize)
			- Происходит после изменения размера.
				Параметры - oldWidth, oldHeight - старые ширина и высота.
		show(on_show)
		hide(on_hide)
			- Происходят при скрытии/показывании.
		init- Происходит при создании объекта
				Аргументы - аргументы, с которыми был вызван конструктор.
		update
			- Происходит переодически. Единственный аргумент - время (в
				секундах), прошедшее с прошлого раза.
		destroy
			- Происходит при уничтожении объекта

	События ввода:
		in:key:press(on_key_press)
		in:key:release(on_key_release)
		in:mouse:enter(on_mouse_enter)
		in:mouse:leave(on_mouse_leave)
		in:mouse:press(on_mouse_press)
		in:mouse:release(on_mouse_release)
		in:mouse:drag(on_mouse_drag)
		in:mouse:move(on_mouse_move)
		in:mouse:scroll(on_mouse_scroll)
	'''

	events = [
		'init',
		'update',
		('destroy','on_destroy'),
		('vp:resize','on_viewport_resize'),
		('show','on_show'),
		('hide','on_hide'),
		('in:key:press','on_key_press'),
		('in:key:release','on_key_release'),
		('in:mouse:enter','on_mouse_enter'),
		('in:mouse:leave','on_mouse_leave'),
		('in:mouse:press','on_mouse_press'),
		('in:mouse:release','on_mouse_release'),
		('in:mouse:drag','on_mouse_drag'),
		('in:mouse:move','on_mouse_move'),
		('in:mouse:scroll','on_mouse_scroll')
	]

	def __init__(self,*args,**kwargs):
		Events.__init__(self)

		self._visible = False

		self.trigger('init',*args,**kwargs)

	def show(self,show=True):
		'''
		'''
		if show != self._visible:
			self._visible = show
			self.trigger('show' if show else 'hide')
		return self

	def hide(self,hide=True):
		'''
		'''
		return self.show(not hide)

	def draw(self):
		'''
		'''
		pass
