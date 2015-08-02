# coding=UTF-8

import pyglet.media

_static_sounds = {}

def Play(name):
	'''
	Воспроизводит звук.
	'''
	snd = Preload(name)
	return snd.play() if snd != None else None

def Preload(name,aliases=[]):
	'''
	Загружает звук если он не был ранее загружен и назначает звуку псевдонимы.
	'''
	if name not in _static_sounds:
		try:
			snd = pyglet.media.load(name,streaming=False)
		except Exception as e:
			snd = None
			print 'Could not load sound {name} because of following exception:\n{e}'.format(**locals())
		_static_sounds[name] = snd
	else:
		snd = _static_sounds[name]

	for alias in aliases:
		if (alias not in _static_sounds) or (snd != None):
			_static_sounds[alias] = snd

	return snd
