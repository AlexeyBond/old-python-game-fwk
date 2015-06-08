# coding=UTF-8
import pyglet

class GameConsole:
	def __init__(self,nlines=40,fsize=18):
		self.fsize = fsize
		self.nlines = nlines
		self.lines = []
		self.current_line = 0
		self.visible = True
		self.fps_display = pyglet.clock.ClockDisplay()
		for i in range(nlines):
			newln = pyglet.text.Label(text='',font_size=18,x=0,y=0,font_name='Courier New')
			newln.console_line_id = i
			self.lines.append( newln )

	def update_positions(self):
		for ln in self.lines:
			ln.begin_update( )
			lnid = (ln.console_line_id + self.nlines - self.current_line) % self.nlines
			ln.y = lnid * (self.fsize * 1.0) + 10
			ln.end_update( )

	def _insert_line(self,text):
		self.current_line = (self.nlines + self.current_line - 1) % self.nlines
		ln = self.lines[self.current_line]
		ln.begin_update( )
		ln.text = str(text)
		ln.end_update( )

	def insert_line(self,text):
		self._insert_line(text)
		self.update_positions( )

	def insert_text(self,text):
		for ln in text.split('\n'):
			self._insert_line(ln)
		self.update_positions( )

	def write(self,*args):
		text = ''
		for a in args:
			text += str(a)
		print text
		self.insert_text(text)

	def draw(self):
		if self.visible:
			for l in self.lines:
				l.draw( )
			self.fps_display.draw( )

GAME_CONSOLE = GameConsole( )
