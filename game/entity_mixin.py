# coding=UTF-8
'''
Модуль содержит набор классов-примесей для игровых сущностей.
'''

from fwk.util.events import Events
from fwk.game.camera import CameraController

class Movement:
	'''
	Примесь, делающая сущность подвижной.

	Добавляет свойства:
		velocity		- вектор скорости движения сущности
		angularVelocity	- скорость вращения сущности

	При обновлении позиция и поворот сущности будут изменяться в соответствии
		с её скоростями.
	'''
	#TODO: Test it.
	@Events.before
	def spawn(self):
		self._velocity_x, self._velocity_y = 0, 0
		self._velocity_angular = 0

	def update(self,dt):
		x, y = self.position
		a = self.rotation

		x += self._velocity_x * dt
		y += self._velocity_y * dt
		a += self._velocity_angular * dt

		self.position = x, y
		self.rotation = a

	@property
	def velocity(self):
		return self._velocity_x, self._velocity_y

	@velocity.setter
	def velocity(self,value):
		self._velocity_x, self._velocity_y = value

	@property
	def angularVelocity(self):
		return self._velocity_angular

	@angularVelocity.setter
	def angularVelocity(self,value):
		self._velocity_angular = value

class Attached:
	'''
	Примесь, позволяющая привязать трансформацию сущности к другой сущности.
	Привязанная сущность будет двигаться вместе с сущностью, к которой
		она привязана.
	'''
	#TODO: Test it.
	@Events.before
	def spawn(self):
		self._parent = None

	def attach(self,parent,props=('position','rotation','scale'),events=('update','destroy')):
		'''
		Привязать сущность к новой родительской сущности.
		'''
		self._attach_props = props
		self._attach_events = events
		self._parent = parent
		self.unsubscribe_all()
		for event in self._attach_events:
			self.subscribe(parent,event)

	def update(self,dt):
		if self._parent is None:
			return

		for prop in self._attach_props:
			value = getattr(self._parent,prop)
			setattr(self,prop,value)

class CameraTarget(CameraController):
	'''
	Примесь, делающая сущность объектом, управляющим камерой, а именно -
		передающим камере некоторые из своих свойств.

	Аттрибуты:
		cameraInitials	- словарь значений свойств камеры, устанавливаемых при
							её подключении.
		cameraAttachMap	- словарь, определяющий связь свойств камеры и
							сущности: ключи - имена свойств камеры, а значения
							- имена свойств сущности.
	'''
	#TODO: Test it.
	@Events.before
	def spawn(self):
		self.cameraAttachMap = {'focus':'position','rotation':'rotation'}
		self.cameraInitials = {'scale':1.0,'scale_x':1.0,'scale_y':1.0}

	def initCamera(self,camera):
		for prop, val in self.cameraInitials.items():
			setattr(camera,prop,val)
		self.updateCamera(camera)

	def updateCamera(self,camera):
		for cam_prop, my_prop in self.cameraAttachMap.items():
			setattr(camera,cam_prop,getattr(self,my_prop))
