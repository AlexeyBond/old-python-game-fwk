# coding=UTF-8
import json
import pyglet

from fwk.util.events import Events
from fwk.util.events import Schedule
from fwk.util.geometry import *
from fwk.game.entity import GameEntity

class Game(Events,Schedule):
	'''
	Класс игрового мира. В игровом мире живут игровые сущности.

	Наследуется от класса Events - для использования событий и Schedule - для
		выполнения событий по расписанию (по счастливому совпадению, сигнатура
		и семантика метода update совпадает с событием update игрового мира).

	Аттрибуты:
		currentTime	- текущее игровое время (унаследован от Schedule).
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
		# Возможно, не лучший способ инициализации.
		Events.__init__(self)
		Schedule.__init__(self)

		# Словарь, содержащий множества тэггированных сущностей.
		self._tagged_entities = {}

		# Словарь сущностей, имеющих уникальные идентификаторы.
		self._id_entities = {}

		# Словарь с батчами спрайтов, где ключом служит z-индекс спрайта.
		self._sprite_batches = {}

		# Множество сущностей, трансформация которых была изменена с прошлой отрисовки.
		self._transform_changed_entities = set()

	def addEntity(self,entity,show=True):
		'''
		Добавляет сущность в игровой мир, выполняет на ней событие spawn и
			делает её видимой если третий аргумент (show) - истина.
		'''
		entity.game = self
		entity.trigger('spawn')
		entity.show(show)

	def onSetEntityId(self,entity,_id):
		'''
		Метод, который должен быть вызван сущностью при установке нового
			значения поля id (до фактической его установки).
		'''
		prev = self._id_entities.get(_id,None)

		if prev is not None and prev is not entity:
			prev.id = None

		if entity.id is not None:
			self._id_entities[entity.id] = None
			del self._id_entities[entity.id]

		if _id is not None:
			self._id_entities[_id] = entity

	def getEntityById(self,_id):
		'''
		Метод, позволяющий получить сущность по её уникальному идентификатору.
		'''
		return self._id_entities.get(_id,None)

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

	def getEntitiesByTag(self,tag):
		'''
		Возвращает список сущностей отмеченных заданным тегом.
		'''
		return list(self._tagged_entities.get(tag,()))

	def invalidateEntityTransform(self,entity):
		'''
		Добавляет сущность в список сущностей, трансформация которых была
			изменена. Перед отрисовкой трансформация будет передана спрайтам
			сущностей, а затем список будет очищен.
		'''
		self._transform_changed_entities.add(entity)

	def loadEntities(self,worldDesc):
		'''
		Создаёт сущности по описанию игрового мира.
		'''
		for entdesc in worldDesc.get('entities',[]):
			_class = entdesc['_class']
			eclass = GameEntity.getClass(_class)

			if eclass is None:
				print 'Invalid entity class name given:', _class
				continue

			entity = eclass()
			self.addEntity(entity)
			entity.configure(entdesc)

	def loadFromJSON(self,fileName):
		with open(fileName,'r') as jsfile:
			data = json.load(jsfile)
		self.loadEntities(data)

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

	def applySpriteTransform(self,entity,sprite):
		'''
		Применяет трансформацию сущности к спрайту.
		'''
		sprite.set_position(*(entity.position))
		sprite.scale = entity.scale
		sprite.rotation = entity.rotation

	def transformChangeHook(self,entity):
		'''
		Вызывается сущностью после изменения трансформации.

		Может ограничивать перемещение сущности или зацикливать пространство.
		'''
		pass

	def distance(self,posa,posb):
		'''
		Вычисляет расстояние между двумя точками.

		Может производить нестандартные вычисления для зацикленных пространств.
		'''
		return distance(posa,posb)

	def directionFromTo(self,posFrom,posTo):
		'''
		Вычисляет вектор направления между двумя точками.

		Может производить нестандартные вычисления для зацикленных пространств.
		'''
		return posTo[0] - posFrom[0], posTo[1] - posTo[1]

	def drawSprites(self):
		'''
		Выполняет отрисовку батчей спрайтов.
		'''
		# Обновить трансформацию сущностей
		for entity in self._transform_changed_entities:
			entity.trigger('after-transform-changed')

		self._transform_changed_entities.clear()

		# Собстнна нарисовать спрайты.
		for zindex in sorted(self._sprite_batches.keys()):
			self._sprite_batches[zindex].draw()
