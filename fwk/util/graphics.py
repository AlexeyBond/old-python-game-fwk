# coding=UTF-8
import pyglet

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

def DrawWireframeRect(rect):
	pyglet.gl.glBegin(pyglet.gl.GL_LINE_LOOP)
	pyglet.gl.glVertex2f(rect.left,rect.top)
	pyglet.gl.glVertex2f(rect.right,rect.top)
	pyglet.gl.glVertex2f(rect.right,rect.bottom)
	pyglet.gl.glVertex2f(rect.left,rect.bottom)
	pyglet.gl.glEnd( )
