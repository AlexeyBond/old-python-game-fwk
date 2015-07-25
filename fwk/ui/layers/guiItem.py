# coding=UTF-8
from copy import copy

from fwk.ui.layer import Layer
from fwk.util.all import *

class GUIItemLayer(Layer):
	'''
	Слой - элемент графического интерфейса пользователя.
	'''

	events = [
		('ui:hover-start','on_hover_start'),
		('ui:hover-end','on_hover_end'),
		('ui:focus-start','on_focus_start'),
		('ui:focus-end','on_focus_end'),
		('ui:click','on_click')
	]

	def init(self,layout):
		self._layout = layout

		self.hover = False
		self.focus = False

	def on_add_to_screen(self,screen):
		self._updateLayout(**(self._layout))

	@staticmethod
	def _updateLayoutDim(vpSize,elMin,elMax,elSize):
		elMax = vpSize - elMax if elMax != None else None
		if (elMax == None) and (elMin == None):
			hvsz = vpSize / 2
			hesz = elSize / 2
			elMin = hvsz - hesz
			elMax = hvsz + hesz
		return elMin, elMax, elSize

	def _updateLayout(self,top=None,bottom=None,left=None,right=None,width=None,height=None,offset_x=0,offset_y=0):
		left, right, width = GUIItemLayer._updateLayoutDim(self.width,left,right,width)
		bottom, top, height = GUIItemLayer._updateLayoutDim(self.height,bottom,top,height)

		self._gui_item_rect = Rect(top=top,bottom=bottom,left=left,right=right,width=width,height=height)
		self._gui_item_rect.move(offset_x, offset_y)

	@property
	def layout(self):
		'''
		Свойство, возвращающее текущее расположение элемента (на самом деле -
			копию его), и позволяющее установит новое.

		Расположение (layout) элемента представляет из себя словарь со
			следующими полями:
			<top,bottom,left,right>
					- координаты краёв элемента относительно соответствующих
						краёв родительского элемента (экрана). Если обе
						координаты отсутствуют или равны None, то элемент
						распологается по центру.
			<height,width>
					- высота и ширина элемента. Используются если координат
						недостаточно.
			<offset_x,offset_y>
					- отступы элемента по осям x и y.
		'''
		return copy(self._layout)

	@layout.setter
	def layout(self,layout):
		self._updateLayout(**layout)
		self._layout = layout

	def on_viewport_resize(self,*a):
		self._updateLayout(**(self._layout))

	def _updateHoverStatus(self,curX,curY):
		hoverStatusNew = self._gui_item_rect.hasPoint(curX,curY)
		if hoverStatusNew != self.hover:
			self.hover = hoverStatusNew
			return self.trigger('ui:hover-start' if hoverStatusNew else 'ui:hover-end')

	def on_mouse_enter(self,x,y):
		return self._updateHoverStatus(x,y)

	def on_mouse_leave(self,x,y):
		self.hover = False
		self.focus = False

	def on_mouse_move(self,x,y,dx,dy):
		return self._updateHoverStatus(x,y)

	def on_mouse_press(self,x,y,button,mod):
		if self._gui_item_rect.hasPoint(x,y):
			self.focus = True
			return self.trigger('ui:focus-start')

	def on_mouse_release(self,x,y,button,mod):
		if self.focus:
			self.focus = False
			self.trigger('ui:focus-end')
			if self._gui_item_rect.hasPoint(x,y):
				self.trigger('ui:click',x,y)
		return self._updateHoverStatus(x,y)

	def draw(self):
		color = Color(255,255,255)
		if self.focus:
			color.rgb = (255,0,0)
		elif self.hover:
			color.rgb = (0,255,0)
		DrawWireframeRect(self._gui_item_rect,color)
