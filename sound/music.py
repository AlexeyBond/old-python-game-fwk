# coding=UTF-8

import pyglet.media

_music_sources = {}
_music_player = None

def Play(name,loop=True):
	'''
	Играет музыку. Зацикливает, если loop=True (по-умолчанию - True).
	'''
	global _music_player

	if _music_player is None:
		_music_player = pyglet.media.Player()

	_music_player.pause()
	_music_player.next()
	try:
		_music_player.queue(pyglet.media.load(name,streaming=True))
	except Exception as e:
		print 'Couldn\'t play mysic from {name} because of exception:\n{e}'.format(**locals())
		return
	_music_player.eos_action = pyglet.media.Player.EOS_LOOP if loop else pyglet.media.Player.EOS_STOP
	_music_player.play()
