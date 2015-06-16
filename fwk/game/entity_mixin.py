# coding=UTF-8
'''
Модуль содержит набор классов-примесей для игровых сущностей.
'''

from fwk.util.events import Events

class Movement:
	'''
	Примесь, делающая сущность подвижной.

	Добавляет свойства:
		velocity		- вектор скорости движения сущности
		angularVelocity	- скорость вращения сущности

	При обновлении позиция и поворот сущности будут изменяться в соответствии
		с её скоростями.
	'''
	@Events.important
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
	@Events.important
	def spawn(self):
		self._parent = None

	def attach(self,parent,props=['position','rotation','scale'],events=['update','destroy']):
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
		if self._parent == None:
			return

		for prop in self._attach_props:
			value = getattr(self._parent,prop)
			setattr(self,prop,value)
