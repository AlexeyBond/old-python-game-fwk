# coding=UTF-8
import math

from fwk.util.events import Events

class GameEntity(Events):
	'''
	Класс игровой сущности.

	Аттрибуты:
		game		- ссылка на объект игрового мира
		position	- координаты центра сущности в игровом мире
		rotation	- поворот сущности #TODO: определиться с еденицами измерения и направлением поворота
		scale		- масштаб спрайта сущности относительно оригинального размера
		sprite		- спрайт
		id			- уникальный идентификатор сущности
	События:
		spawn		- происходит при добавлении сущности в игровой мир
		update		- происходит переодически.
			Аргументы:
				dt		- время, прошедшее с момента, когда событие произошло в прошлый раз.
		destroy		- происходит перед уничтожением сущности.
		hide		- происходит когда сущность скрывается (обработчик: on_hide).
		show		- происходит когда сущность становится видимой (обработчик on_show).
	'''
	def __init__(self):
		Events.__init__(self)

		# <координаты, поворот, масштаб> - трансформация
		self._x, self._y = 0, 0
		self._rotation = 0
		self._scale = 1.0

		# Флаг изменения трансформации
		self._transform_changed = True

		self.game = None
		self.sprite = None
		self.id = None
		self.angularVelocity = 0

	events = [
		'spawn',
		'update',
		'destroy',
		('hide','on_hide'),
		('show','on_show'),
		('transform:move','on_move'),
		('transform:scale','on_scale'),
		('transform:rotate','on_rotate'),
	]

	def getDirection(self):
		'''
		Метод, вычисляющий вектор направления по повороту сущности.
		'''
		#TODO: Разобраться с системами координат/единицами измерения углов и т.д.
		return math.sin(self.rotation),math.cos(self.rotation)

	@property
	def position(self):
		'''
		Свойство, позволяющее получать/изменять пощицию сущности.
		'''
		return self._x, self._y

	@position.setter
	def position(self,val):
		if (self._x, self._y) == val:
			return
		self._x, self._y = val
		self.trigger('transform:move')
		self._transform_changed = True

	@property
	def rotation(self):
		'''
		Свойство, позволяющее получать/изменять поворот сущности.
		'''
		return self._rotation

	@rotation.setter
	def rotation(self,val):
		self._rotation = val
		self.trigger('transform:rotate')
		self._transform_changed = True

	@property
	def scale(self):
		'''
		Свойство, позволяющее получать/изменять масштаб сущности.
		'''
		return self._scale

	@scale.setter
	def scale(self,val):
		self._scale = val
		self.trigger('transform:scale')
		self._transform_changed = True

	def spawn(self):
		# Подписка на событие 'update' игрового мира.
		self.subscribe(self.game,'update')

	def destroy(self):
		# Отказ от всех подписок
		self.unsubscribe_all()
