# coding=UTF-8

from fwk.util.rect import Rect
from fwk.util.graphics import LoadTexture
from pyglet.image import AnimationFrame, Animation
import json

class AnimationsList:
	'''
	Список анимаций.

	Создаёт анимации по описанию и хранит их.
	Созданные анимации - стандартные анимации pyglet-а и могут быть
		использованы вместо текстур для спрайтов.

	Описание имеет вид:

	{'<имя_анимации>':<кадры>, ...}

	<кадры> ::= [<кадр>, ...]

	<кадр> ::= {
		'img': '<имя_изображения>',
		't': '<продолжительность_кадра>',
		'rect': <регион_изображения>,
		'anchor': <якорь>
	}

	Регион изображения может быть задан объектом класса Rect, или словарём,
		содержимого которого достаточно для создания такого объекта. Если
		регион не задан, то используется всё изображение целиком.
	По полю anchor - см. fwk.util.graphics.LoadTexture
	'''
	#TODO: Test it
	def __init__(self,source):
		self._initialized = False
		self._animations = {}
		self._source = source

	def _parseRect(self,desc):
		if isinstance(desc,Rect):
			return desc

		return Rect(**dict(desc))

	def _parseFrame(self,desc):
		image_name = str(desc['img'])
		duration = float(desc['t'])
		anchor = str(desc.get('anchor','default'))

		image = LoadTexture(image_name,anchor=anchor)

		if 'rect' in desc:
			image_rect = self._parseRect(desc['rect'])
			image = image.get_region(
				image_rect.left,image_rect.bottom,
				image_rect.width,image_rect.height).get_texture()

		return AnimationFrame(image,duration)

	def _parseAnimation(self,desc):
		frames = []
		for fdesc in desc:
			frames.append(self._parseFrame(fdesc))
		return Animation(frames)

	def preload(self):
		'''
		Загружает изображения и создаёт анимации если этого ещё не было сделано.
		'''
		if self._initialized:
			return
		self._initialized = True

		for name, desc in self._source.items():
			self._animations[name] = self._parseAnimation(desc)

	def __getitem__(self,name):
		'''
		Возвращает анимацию с заданным именем.

		Если анимации не были загружены, то пытается загрузить (используя метод
			preload).
		Бросает KeyError если такой анимации нет.
		'''
		self.preload()
		return self._animations[name]

	@staticmethod
	def fromJSONFile(fileName):
		'''
		Создаёт список анимаций из JSON-файла.
		'''
		with open(fileName) as dataFile:
			description = json.load(dataFile)

		return AnimationsList(description)
