# coding=UTF-8

class Rect:
	'''
	Класс прямоугольника.
	'''
	_ORIGINS_TABLE = {
		# [left->right, bottom->top]
		'bottom-left': [0,0],
		'top-left': [0,1],
		'bottom-right': [1,0],
		'top-right': [1,1],
		'center-center': [0.5,0.5]
	}
	_DEFAULT_ORIGIN = 'top-left'

	@staticmethod
	def _init_dimension(minLimit,maxLimit,size):
		minVal = minLimit if minLimit != None else (maxLimit-size)
		maxVal = maxLimit if maxLimit != None else (minLimit+size)
		return min(minVal, maxVal), max(minVal, maxVal)

	def __init__(self,bottom=None,top=None,left=None,right=None,width=None,height=None):
		'''
		Конструктор.

		Принимает параметры для горизонтальных и вертикальных размера/положения:
			<bottom,top,height> - по вертикали
			<left,right,width>  - по горизонтали

		Для каждой группы размеров должно быть задано 2 значения.
		Если задано 3 - то игнорируются width и height для горизонтали и
			вертикали соответственно.

		Начало координат находится внизу слева. Ось X направлена вправо, ось Y - вверх.
		'''
		try:
			self.bottom, self.top = Rect._init_dimension(bottom,top,height)
			self.left, self.right = Rect._init_dimension(left,right,width)
		except Exception as e:
			print 'Looks like not enough of parameters to create a rectangle.'
			print 'I`ve got:',str(locals())
			raise e

	def getWidth(self):
		'''
		Возвращает ширину прямоугольника.
		'''
		return self.right - self.left

	def getHeight(self):
		'''
		Возвращает высоту прямоугольника.
		'''
		return self.top - self.bottom

	def getOriginPoint(self,origin):
		'''
		Возвращает фактические координаты опорной точки.

		Опорная точка может быть описана строкой ('bottom-left', 'top-right',
			'center-center', и т.д.) или абсолютными координатами (список из
			2-х значений).
		'''
		if type(origin) in (str,unicode):
			orig = Rect._ORIGINS_TABLE[origin]
			origx = self.left * (1.0 - orig[0]) + self.right * orig[0]
			origy = self.bottom * (1.0 - orig[1]) + self.top * orig[1]
			return origx, origy
		return origin[0],origin[1]

	@staticmethod
	def _resize_dimension(curMin,curMax,orig,size):
		dd = size * (orig - curMin) / (curMax - curMin)
		return (orig - dd),(orig + size - dd)

	def resize(self,width,height,origin=_DEFAULT_ORIGIN):
		'''
		Изменяет размер прямоугольника, масштабируя его вокруг заданной опорной точки.
		'''
		ox, oy = self.getOriginPoint(origin)
		self.left, self.right = Rect._resize_dimension(self.left,self.right,ox,width)
		self.bottom, self.top = Rect._resize_dimension(self.bottom,self.top,oy,height)

	@staticmethod
	def _moveTo_dimension(curMin,curMax,orig,target):
		dd = target - orig
		return (curMin + dd),(curMax + dd)

	def moveTo(self,x,y,origin=_DEFAULT_ORIGIN):
		'''
		Перемещает прямоугольник так, что заданная опорная точка оказывается
			в указанных координатах.
		'''
		ox, oy = self.getOriginPoint(origin)
		self.left, self.right = Rect._moveTo_dimension(self.left,self.right,ox,x)
		self.bottom, self.top = Rect._moveTo_dimension(self.bottom,self.top,oy,y)

	def clone(self):
		'''
		Создаёт копию прямоугольника.
		'''
		return Rect(bottom=self.bottom,top=self.top,left=self.left,right=self.right)
