# coding=UTF-8
import math

from fwk.util.events import Events

import fwk.game.entity_mixin as _entity_mixins

class GameEntity(Events):
	'''
	Класс игровой сущности.

	Аттрибуты/свойства:
		game		- ссылка на объект игрового мира
		position	- координаты центра сущности в игровом мире
		rotation	- поворот сущности #TODO: определиться с еденицами
					  измерения и направлением поворота
		scale		- масштаб спрайта сущности относительно
					  оригинального размера
		sprite		- спрайт
		id			- уникальный идентификатор сущности
	События:
		spawn		- происходит при добавлении сущности в игровой мир
		update		- происходит переодически.
			Аргументы:
				dt		- время, прошедшее с момента, когда событие произошло
						  в прошлый раз.
		destroy		- происходит перед уничтожением сущности.
		hide		- происходит когда сущность скрывается
					  (обработчик: on_hide).
		show		- происходит когда сущность становится видимой
					  (обработчик on_show).
	'''
	def __init__(self):
		Events.__init__(self)

		# <координаты, поворот, масштаб> - трансформация
		self._x, self._y = 0, 0
		self._rotation = 0
		self._scale = 1.0

		# Флаг изменения трансформации
		self._transform_changed = True

		# Флаг видимости
		self._visible = False

		self.game = None
		self.sprite = None
		self.id = None

	events = [
		'spawn',
		'update',
		'destroy',
		('hide','on_hide'),
		('show','on_show')
	]

	def getDirection(self):
		'''
		Метод, вычисляющий вектор направления по повороту сущности.
		'''
		#TODO: Разобраться с системами координат/единицами измерения углов и т.д.
		return math.sin(self.rotation),math.cos(self.rotation)

	@property
	def visible(self):
		'''
		Свойство, указывающее, видима ли сущность
		'''
		return self._visible

	@visible.setter
	def visible(self,visible):
		if visible != self.visible:
			self.show(visible)

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
		self._transform_changed = True

	def spawn(self):
		# Подписка на событие 'update' игрового мира.
		self.subscribe(self.game,'update')

	def destroy(self):
		# Отказ от всех подписок
		self.unsubscribe_all()

	def show(self,show=True):
		'''
		Показывает сущность
		'''
		if (not show) != (not self.visible):
			self.trigger('show' if show else 'hide')

	def hide(self,hide=True):
		'''
		Скрывает сущность
		'''
		return self.show(not hide)

	def on_show(self):
		self._visible = True

	def on_hide(self):
		self._visible = False

	def addTags(self,*tags):
		pass

	def clearTags(self,*tags):
		pass

	def configure(self,config):
		'''
		Конфигурирует сущность в соответствии с заданным набором пар
			ключ-значение. Используется при загрузке уровня.

		Фактически выполняет присвоение аттрибутов при помощи setattr.
		Игнорирует ключи, начинающиеся с '_'.
		'''
		for key,value in config.items():
			if not key.startswith('_')
				setattr(self,key,value)

	_classDefs = {}

	@staticmethod
	def defineClass(className):
		'''
		Декоратор, присваивающий классу сущностей обозначение, используемое
			при загрузке уровня.
		'''
		def _decorator(eclass):
			if GameEntity not in eclass.__bases__:
				raise Exception('Programming error: @GameEntity.defineClass decorator used on non-entity class {}.'.format(eclass.__name__))
			GameEntity._classDefs[className] = eclass
			return eclass
		return _decorator

	@staticmethod
	def getClass(className):
		'''
		Метод, позволяющий найти класс сущностей по обозначению, присвренному
			декоратором defineClass.
		'''
		return GameEntity._classDefs.get(className,None)

	mixin = _entity_mixins
