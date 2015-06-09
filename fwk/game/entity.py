# coding=UTF-8
from fwk.util.events import Events

class GameEntity(Events):
	'''
	Класс игровой сущности.

	Аттрибуты:
		game		- ссылка на объект игрового мира
		x, y		- координаты центра сущности в игровом мире
		rotation	- поворот сущности #TODO: определиться с еденицами измерения и направлением поворота
		scale		- масштаб спрайта сущности относительно оригинального размера
		sprite		- спрайт
		id			- уникальный идентификатор сущности
	'''
	def __init__(self):
		Events.__init__(self)

		self.game = None

		self.x, self.y = 0, 0

		self.rotation = 0

		self.scale = 1.0

		self.sprite = None

		self.id = None

		self._handlers = {}

	events = [
		'spawn',
		'update',
		'destroy'
	]
