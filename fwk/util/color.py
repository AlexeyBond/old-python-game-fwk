# coding=UTF-8

class Color(object):
	'''
	Класс цвета.
	'''
	def __init__(self,*args):
		self._val = 1., 1., 1., 1.
		self._set(args)

	def _set(self,val):
		if type(val) in (tuple,list):
			if len(val) == 4:
				self.rgba = val
			elif len(val) == 3:
				self.rgb = val

	@property
	def rgb(self):
		'''
		Свойство, позволяющее получить/установить значение цвета в системе RGB.

		При получении компоненты всегда находятся в диапазоне [0.0;1.0],
			установить же значение можно используя диапазон [0.0;1.0] - для
			этого - все компоненты - float, либо [0;255] - для этого все
			компоненты int.
		'''
		return self._val[0:3]

	@rgb.setter
	def rgb(self,val):
		assert len(val) == 3
		assert type(val[0]) == type(val[1]) and type(val[1]) == type(val[2])
		assert type(val[0]) in (int, float)
		if type(val[0]) == int:
			val = [(float(_v) / 255.0) for _v in val]
		self._val = val[0], val[1], val[2], 1.

	@property
	def rgba(self):
		'''
		Свойство, позволяющее получить/установить значение цвета в системе RGBA

		Используются те же диапазоны значений компонентов, что и в rgb.
		'''
		return self._val

	@rgba.setter
	def rgba(self,val):
		assert len(val) == 4
		assert type(val[0]) == type(val[1]) \
			and type(val[1]) == type(val[2]) \
			and type(val[2]) == type(val[3])
		assert type(val[0]) in (int, float)
		if type(val[0]) == int:
			val = [(float(_v) / 255.0) for _v in val]
		self._val = val[0], val[1], val[2], val[3]
