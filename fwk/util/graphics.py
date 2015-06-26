# coding=UTF-8
import pyglet

from fwk.util.color import Color

def ApplyTextureAnchor(texture,anchor='default'):
	'''
	Функция, устанавливающая "якорь"(anchor) текстуры.

	Возможные варианты:
		"default" - не делает ничего
		"center" - по центру текстуры
		(x,y) или [x,y] - в точке {x;y}
	'''
	if anchor == 'center':
		texture.anchor_x = texture.width // 2
		texture.anchor_y = texture.height // 2
	elif type(anchor) in (tuple,list):
		texture.anchor_x = anchor[0]
		texture.anchor_y = anchor[1]

def LoadTexture(name,anchor='default'):
	'''
	Функция, загружающая текстуру.
	Параметры:
		name - имя текстуры (путь к файлу)
		anchor - "якорь" (см. ApplyTextureAnchor)
	'''
	tex = pyglet.resource.image(name).get_texture( )
	ApplyTextureAnchor(tex,anchor)
	return tex

def DrawWireframeRect(rect,color=Color()):
	verts = (
		rect.left, rect.top,
		rect.right, rect.top,
		rect.right, rect.bottom,
		rect.left, rect.bottom)
	pyglet.graphics.draw(4,pyglet.gl.GL_LINE_LOOP,('v2f',verts),('c4f',color.rgba*4))

def BlitTextureToRect(texture,rect):
	texture.blit(x=rect.left,y=rect.bottom,width=rect.width,height=rect.height)
