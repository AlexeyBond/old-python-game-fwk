# coding=UTF-8
import pyglet
from pyglet.gl import *

from fwk.ui.screen import Screen
from console import GAME_CONSOLE as Console
from fwk.util.all import *

class MainWindow(pyglet.window.Window):
	'''
	Класс главного окна
	'''

	def __init__(self):
		pyglet.window.Window.__init__(self,resizable=True)

		self.init_opengl( )

		# Ограничение частоты кадров
		pyglet.clock.set_fps_limit(60)
		pyglet.clock.schedule(self._update)

		Console.write('-- Starting --')

		self.cur_screen = None
		self.change_screen(Screen.new('STARTUP'))

	def init_opengl(self):
		'''
		Метод предварительной настройки OpenGL
		'''
		glClearColor(0.01, 0.1, 0.01, 1.0)

	def setup_projection(self,width,height):
		'''
		Настройка матрицы проекции и вьюпорта под размеры окна
		'''
		glViewport(0,0,width,height)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity( )
		glOrtho(0,width,0,height,-1,1)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity( )

	def change_screen(self,screen):
		'''
		Метод переключения экрана.

		Принимает ссылку на новый экран.
		Активирует экран и изменяет его размер под размер окна.
		'''
		screen.activate(self.cur_screen)
		self.cur_screen = screen
		self.cur_screen.resize(self.width,self.height)

	_EVENTS_PYGLET_TO_DRAWABLE_MAP = {
		'on_key_press'		: 'in:key:press',
		'on_key_release'	: 'in:key:release',
		'on_mouse_drag'		: 'in:mouse:drag',
		'on_mouse_enter'	: 'in:mouse:enter',
		'on_mouse_leave'	: 'in:mouse:leave',
		'on_mouse_motion'	: 'in:mouse:move',
		'on_mouse_press'	: 'in:mouse:press',
		'on_mouse_release'	: 'in:mouse:release',
		'on_mouse_scroll'	: 'in:mouse:scroll'
	}

	def dispatch_event(self, event_type, *args):
		'''
		Диспечер событий.
		'''
		if event_type in MainWindow._EVENTS_PYGLET_TO_DRAWABLE_MAP:
			self.cur_screen.trigger(MainWindow._EVENTS_PYGLET_TO_DRAWABLE_MAP[event_type],*args)
			#TODO: Сделать обработку screen.next и screen.exit_required без привязки к событиям.
			if self.cur_screen.exit_required:
				self.close( )
			elif self.cur_screen.next != None:
				self.change_screen(self.cur_screen.next)
		super(MainWindow,self).dispatch_event(event_type,*args)

	def _update(self,dt):
		self.cur_screen.trigger('update',dt)

	def on_draw(self):
		'''
		Метод отрисовки содержимого окна.
		'''
		# Очистить окно
		self.clear( )

		# На всякий случай ещё и так
		glClear(GL_COLOR_BUFFER_BIT)

		# Рисуем текущий зкран
		self.cur_screen.draw( )

		# И консольку сверху
		Console.draw( )

	def on_resize(self,width,height):
		'''
		Метод, вызываемый при изменении размеров окна.
		'''
		Console.write( 'Window resized: %sx%s'%(width,height) )
		self.setup_projection(width,height)
		self.cur_screen.resize(width,height)

	def on_key_press(self,key,mod):
		'''
		Метод, вызываемый при нажатии клавиши на клавиатуре.
		'''
		if key in (KEY.QUOTELEFT,KEY.ASCIITILDE):
			Console.visible = not Console.visible
		elif key == KEY.ESCAPE and mod == KEY.MOD_CTRL:
			self.close( )

	def on_close(self):
		'''
		Обработка закрытия окна [X]рестикомъ.
		'''
		print 'Window closed by user'
		exit(0)
