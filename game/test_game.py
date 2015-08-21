# coding=UTF-8
from unittest import TestCase

from fwk.game.game import Game
from fwk.game.entity import GameEntity

class GameTestCase(TestCase):
	def setUp(self):
		self.game = Game()
		self.e = [GameEntity() for i in range(2)]
		for e in self.e:
			self.game.addEntity(e)

class GameEntityIdTest(GameTestCase):
	def test_set_entity_id(self):
		self.e[0].id = 'qwe'
		self.assertEqual(self.e[0].id,'qwe')
		self.assertEqual(self.e[0],self.game.getEntityById('qwe'))

	def test_reset_entity_id(self):
		self.e[0].id = 'qwe'
		self.e[0].id = None
		self.assertEqual(self.e[0].id,None)
		self.assertEqual(None,self.game.getEntityById('qwe'))
		self.assertEqual(None,self.game.getEntityById(None))

	def test_replace_entity_id(self):
		self.e[0].id = 'qwe'
		self.e[1].id = 'qwe'
		self.assertEqual(self.e[0].id,None)
		self.assertEqual(self.e[1].id,'qwe')
		self.assertEqual(self.e[1],self.game.getEntityById('qwe'))
		self.assertEqual(None,self.game.getEntityById(None))

class GameEntityTaggingTest(GameTestCase):
	def test_set_one_tag(self):
		self.game.setEntityTags(self.e[0],'mytag')
		self.assertEqual(self.game.getEntitiesByTag('mytag').count(self.e[0]),1)
		self.assertEqual(self.game.getEntitiesByTag('mytag').count(self.e[1]),0)

	def test_set_multiple_tags(self):
		mytags = list(['mytag#'+str(i) for i in range(10)])
		self.game.setEntityTags(self.e[0],*mytags)
		for tag in mytags:
			self.assertEqual(self.game.getEntitiesByTag(tag).count(self.e[0]),1)

	def test_tags_remove(self):
		mytags = list(['mytag#'+str(i) for i in range(10)])
		remtags = ['faketag'] + mytags[1:7:2]
		self.game.setEntityTags(self.e[0],*mytags)
		self.game.unsetEntityTags(self.e[0],*remtags)
		for tag in mytags:
			self.assertEqual(self.game.getEntitiesByTag(tag).count(self.e[0]),0 if tag in remtags else 1)
