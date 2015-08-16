# coding=UTF-8

from guiItem import GUIItemLayer
from fwk.util.events import Events
from fwk.util.graphics import *
import pyglet

'''
Этот модуль просто пропитан магией числа 9.

Некоторые части кода обфусцированы дабы усилить атмосферу мистики в области
	видимости данного модуля.
'''

__all__ = ['_9Tiles','GUI9TileItem']

class _9Tiles:
	_MAGIC_1 = ((0,None,False),(1,None,True),(None,1,False))
	def _magic_2(self,min_,max_,_sz_,n):
		alpha, omega, patronum = self._MAGIC_1[n]
		return (min_ + alpha * _sz_ if alpha is not None else 0) + \
				(max_ - omega * _sz_ if omega is not None else 0), \
				((max_ - min_) - 2 * _sz_ if patronum else _sz_)

	def _magic_3(self,n,rect):
		a,b = self._magic_2(rect.left,rect.right,self._t_width,n % 3)
		c,d = self._magic_2(rect.bottom,rect.top,self._t_height,n // 3)
		self._tile[n].blit(x=a,y=c,width=b,height=d)

	def _magic_inito(self,textureRect):
		self._tile = []
		for i in range(9):
			a,b = self._magic_2(textureRect.left,textureRect.right,self._t_width,i % 3)
			c,d = self._magic_2(textureRect.bottom,textureRect.top,self._t_height,i // 3)
			self._tile.append(self._texture.get_region(a,c,self._t_width,self._t_height).get_texture())

	def __init__(self,texture,rect):
		self._texture = texture
		self._t_width = rect.width // 3
		self._t_height = rect.height // 3
		self._magic_inito(rect)

	def draw(self,rect):
		for i in range(9):
			self._magic_3(i,rect)

	def getMinSize(self):
		return self._t_width * 2, self._t_height * 2

class GUI9TileItem(GUIItemLayer):
	def init(self,tiles,**kwargs):
		self._9tiles = tiles

	def on_layout_updated(self):
		self._refresh_layout()

	def _refresh_layout(self):
		if not self._9tiles:
			return
		minw, minh = self._9tiles.getMinSize()
		self.rect.resize(max(minw,self.rect.width),max(minh,self.rect.height),'center-center')

	def draw(self):
		if self._9tiles:
			self._9tiles.draw(self.rect)
