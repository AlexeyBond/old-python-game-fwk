# coding=UTF-8
from pyglet import gl

class Camera(object):
	'''
	Камера. Опрелеляет, как и какую часть игрового мира видит игрок.
	Свойства:
		focus		- точка в координатах игрового мира, которая будет
						находиться в центре экрана.
		size = (width, height)
					- размеры экрана
		rotation	- поворот камеры. Направление в игровом мире,
						соответствующее этому повороту, будет изображено как
						направление, соответствующее нулевому повороту в
						экранных координатах.
		scale		- зум камеры, применяемый к обоим измерениям.
		(scale_x, scale_y)
					- дополнительный зум камеры для отдельных измерений.
						Позволяет создать искажения пропорций.
	'''
	def __init__(self):
		self._focus_x = 0
		self._focus_y = 0

		self.width = 1
		self.height = 1

		self.rotation = 0

		self.scale_x = 1
		self.scale_y = 1
		self.scale = 1

		self._controller = None

	@property
	def focus(self):
		'''
		Точка, которая окажется в центре экрана.
		'''
		return self._focus_x, self._focus_y

	@focus.setter
	def focus(self,val):
		self._focus_x, self._focus_y = val

	@property
	def size(self):
		'''
		Размер экрана
		'''
		return self.width, self.height

	@size.setter
	def size(self,val):
		self.width, self.height = val

	def applyTransform(self):
		'''
		Применяет необходимые преобразования к матрице трансформации OpenGL.
		'''
		# 4 - переместить (0,0) в (width/2,height/2)
		gl.glTranslatef(self.width / 2,self.height / 2,0)

		# 3 - поворот вокруг (0,0)
		gl.glRotatef(self.rotation,0,0,1)

		# 2 - масштабирование относительно (0,0)
		gl.glScalef(self.scale_x * self.scale,self.scale_y * self.scale,1)

		# 1 - переместить (focus_x,focus_y) в (0,0)
		gl.glTranslatef(-self._focus_x,-self._focus_y,0)

	def setController(self,controller):
		'''
		Установить управляющий объект для камеры.
		'''
		if controller != None:
			controller.initCamera(self)
		self._controller = controller

	def update(self):
		'''
		Запросить новые параметры у управляющего объекта.
		'''
		if self._controller != None:
			self._controller.updateCamera(self)

	def unproject(self,screenPoint):
		'''
		По экранным координатам определяет координаты соответствующей им точки
			в игровом мире.
		'''
		pass #TODO: Do

	def project(self,gamePoint):
		'''
		По координатам точки в игровом мире определяет координаты
			соответствующей им точки на экране.
		'''
		pass #TODO: Do

class CameraController(object):
	'''
	Интерфейс объекта, управляющего камерой.
	'''
	def initCamera(self,camera):
		'''
		Вызывается однократно при подключении к камере.

		По умолчанию вызывает updateCamera.
		'''
		return self.updateCamera(camera)

	def updateCamera(self,camera):
		'''
		Вызывается перед отрисовкой каждого кадра с использованием камеры.
		'''
		raise 'CameraController.updateCamera() not overloaded.'
