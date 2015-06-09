#!/usr/bin/python
# coding=UTF-8

import math, random
from fwk.ui.screen import AppScreen
from fwk.ui.console import GAME_CONSOLE
from fwk.ui.layers.staticBg import StaticBackgroundLauer

from fwk.util.all import *

@AppScreen.ScreenClass('STARTUP')
class StartupScreen(AppScreen):
	def __init__(self):
		AppScreen.__init__(self)

		self.addLayer(StaticBackgroundLauer('rc/img/256x256bg.png','scale'))

		GAME_CONSOLE.write('Startup screen created.')

	def on_key_press(self,key,mod):
		GAME_CONSOLE.write('SSC:Key down:',KEY.symbol_string(key),'(',key,') [+',KEY.modifiers_string(mod),']')

	def draw(self):
		AppScreen.draw(self)
		r = Rect(bottom=100,height=30,left=50,width=50)
		DrawWireframeRect(r)
		r.resize(width=100,height=300,origin='bottom-left')
		DrawWireframeRect(r)

# @ScreenClass('STARTUP')
# @ScreenClass('GAME')
# class GameScreen(AppScreen):
# 	def __init__(self):
# 		AppScreen.__init__(self)

# 		self.game = MyGame()
# 		self.game.unpause( )
# 		self.camera = Camera( )

# 		self.addLayer(GameWorldLayer(self.game,self.camera))

# 		GAME_CONSOLE.write('Game screen created.')

# 	def on_resize(self,width,height):
# 		AppScreen.on_resize(self,width,height)

# 		self.camera.set_size(width,height)

# 	def on_mouse_scroll(self,x,y,sx,sy):
# 		self.camera.scale *= 2 ** (sy*0.02)

# 	def on_key_press(self,key,mod):
# 		GAME_CONSOLE.write('SSC:Key down:',KEY.symbol_string(key),'(',key,') [+',KEY.modifiers_string(mod),']')

# 	def on_mouse_press(self,x,y,button,modifiers):
# 		pass

# class MyGame(Game):
# 	def __init__(self):
# 		Game.__init__(self)
# 		self.init_entities( )

# 	def init_entities(self):
# 		pass
