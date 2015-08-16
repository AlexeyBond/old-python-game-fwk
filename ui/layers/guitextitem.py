from guiItem import GUIItemLayer
from fwk.util.events import Events
import pyglet

class GUITextItem(GUIItemLayer):
	@Events.before
	def init(self,text='',font='Courier New',fontSize=36,**kwargs):
		self._label = pyglet.text.Label(text=text,font_name=font,font_size=fontSize,
			anchor_x='left',anchor_y='baseline')

	def on_layout_updated(self):
		rect = self.rect
		if self.layout.get('force-size',False):
			rect = rect.clone()
		rect.resize(self._label.content_width,36,'center-center');
		self._label.x = rect.left
		self._label.y = rect.bottom
		rect.extrude(*self.layout.get('padding',(0,0)))

	def draw(self):
		GUIItemLayer.draw(self)
		self._label.draw()

	@property
	def text(self):
		return self._label.text

	@text.setter
	def text(self,val):
		self._label.begin_update()
		self._label.text = val
		self._label.end_update()
