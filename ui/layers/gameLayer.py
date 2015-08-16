# coding=UTF-8

from fwk.ui.layer import Layer

from pyglet import gl

class GameLayer(Layer):
	'''
	Слой, рисующий игровой мир с точки зрения камеры.
	'''
	_GAME_SUBSCRIPTION_EVENTS = ['update']

	def init(self,game,camera,*args,**kwargs):
		self._game = game
		self._camera = camera

		for event in GameLayer._GAME_SUBSCRIPTION_EVENTS:
			self._game.subscribe(self,event)

	def on_add_to_screen(self,screen):
		self._camera.size = self.width, self.height
		self.subscribe(screen,'update')

	def on_viewport_resize(self,*a):
		self._camera.size = self.width, self.height

	def draw(self):
		gl.glMatrixMode(gl.GL_MODELVIEW)
		gl.glPushMatrix()
		gl.glLoadIdentity()

		# Обновить информацию о положении камеры (запросить у CameraController-а)
		self._camera.update()

		# Применить трансформацию
		self._camera.applyTransform()

		# Нарисовать спрайты игрового мира
		self._game.drawSprites()

		gl.glPopMatrix()
