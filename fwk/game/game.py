# coding=UTF-8
import math

from fwk.util.events import Events
from fwk.game.entity import GameEntity

class Game(Events):
	'''
	Класс игрового мира. В игровом мире живут игровые сущности.

	Аттрибуты:
		time		- текущее игровое время.
	События:
		update		- происходит переодически; на это событие подписываются
					  (напрямую или опосредованно) все или почти все сущности.
			Аргументы:
				dt		- время, прошедшее с момента, когда событие произошло
						  в прошлый раз.
	'''
	events = [
		'update'
	]

	def __init__(self):
		# Словарь, содержащий множества тэггированных сущностей.
		self._tagged_entities = {}

		# Словарь с батчами спрайтов, где ключом служит z-индекс спрайта.
		self._sprite_batches = {}

	def addEntity(self,entity,show=True):
		entity.game = self
		entity.trigger('spawn')
		entity.show(show)

	def setEntityTags(self,entity,*tags):
		'''
		Добавляет сущность в списки сущностей с заданными тэгами.
		'''
		for tag in tags:
			eset = self._tagged_entities.get(tag,set())
			eset.add(entity)
			self._tagged_entities[tag] = eset

	def unsetEntityTags(self,entity,*tags):
		'''
		Удаляет сущность из списков сущностей с заданными тэгами, если она
			там была.
		'''
		for tag in tags:
			self._tagged_entities.get(tag,set()).discard(entity)

	def clearEntityTags(self,entity):
		'''
		Удаляет сущность из всех списков тэггированных сущностей.
		'''
		for eset in self._tagged_entities.values():
			eset.discard(entity)

	def loadEntities(self,worldDesc):
		'''
		Создаёт сущности по описанию игрового мира.
		'''
		for entdesc in worldDesc.get('entities',[]):
			_class = entdesc['_class']
			eclass = GameEntity.getClass(_class)

			if eclass == None:
				print 'Invalid entity class name given:', _class
				continue

			entity = eclass()
			self.addEntity(entity)
			entity.configure(entdesc)

	def createSprite(self,image,zindex=0,**kwargs):
		'''
		Создаёт новый спрайт и добавляет его к батчу в зависимости от
			z-индекса.

		При отрисовке батчи рисуются начиная с батча с наименьшим z-индексом.

		Аргументы:
			image		- текстура для спрайта.
			zindex		- z-индекс спрайта.
		'''
		if zindex not in self._sprite_batches:
			self._sprite_batches[zindex] = pyglet.graphics.Batch( )

		batch = self._sprite_batches[zindex]

		return pyglet.sprite.Sprite(img=image,batch=batch,**kwargs)

	def drawSprites(self):
		'''
		Выполняет отрисовку батчей спрайтов.
		'''
		for zindex in sorted(self._sprite_batches.keys()):
			self._sprite_batches[zindex].draw()
