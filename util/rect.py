# coding=UTF-8

class Rect(object):
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
		minVal = minLimit if minLimit is not None else (maxLimit-size)
		maxVal = maxLimit if maxLimit is not None else (minLimit+size)
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

	@property
	def width(self):
		'''
		Ширина прямоугольника.
		'''
		return self.right - self.left

	@property
	def height(self):
		'''
		Высота прямоугольника.
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
		if curMax == curMin:
			off = size /2
			return curMin - off, curMax + off
		dd = size * (orig - curMin) / (curMax - curMin)
		return (orig - dd),(orig + size - dd)

	def resize(self,width,height,origin=_DEFAULT_ORIGIN):
		'''
		Изменяет размер прямоугольника, масштабируя его вокруг заданной опорной точки.

		Возвращает ссылку на объект, на котором был вызван метод.
		'''
		ox, oy = self.getOriginPoint(origin)
		self.left, self.right = Rect._resize_dimension(self.left,self.right,ox,width)
		self.bottom, self.top = Rect._resize_dimension(self.bottom,self.top,oy,height)

		return self

	def scale(self,scaleX,scaleY=None,origin=_DEFAULT_ORIGIN):
		'''
		Масштабирует прямоугольник по осям X и Y, или одинаково по всем осям,
			если передано одно значение.

		Возвращает ссылку на объект, на котором был вызван метод.
		'''
		if scaleY is None:
			scaleY = scaleX

		return self.resize(self.width*scaleX,self.height*scaleY,origin)

	@staticmethod
	def _moveTo_dimension(curMin,curMax,orig,target):
		dd = target - orig
		return (curMin + dd),(curMax + dd)

	def moveTo(self,x,y,origin=_DEFAULT_ORIGIN):
		'''
		Перемещает прямоугольник так, что заданная опорная точка оказывается
			в указанных координатах.

		Возвращает ссылку на объект, на котором был вызван метод.
		'''
		ox, oy = self.getOriginPoint(origin)
		self.left, self.right = Rect._moveTo_dimension(self.left,self.right,ox,x)
		self.bottom, self.top = Rect._moveTo_dimension(self.bottom,self.top,oy,y)

		return self

	def move(self,dx,dy):
		'''
		Перемещает прямоугольник относительно текущего положения.
		'''
		self.left += dx
		self.right += dx
		self.top += dy
		self.bottom += dy

		return self

	def clone(self):
		'''
		Создаёт копию прямоугольника.
		'''
		return Rect(bottom=self.bottom,top=self.top,left=self.left,right=self.right)

	@staticmethod
	def _inset_dimension(minVal,maxVal,insVal):
		minVal += insVal
		maxVal -= insVal

		if minVal > maxVal:
			midVal = (minVal + maxVal) / 2
			minVal = midVal
			maxVal = midVal

		return minVal, maxVal

	def inset(self,x,y=None):
		'''
		Вдавливает прямоугольник по осям X и Y, или одинаково по всем осям,
			если передано только одно значение.
		Значения могут быть отрицательными.
		Если ширина или высота после изменения координат становятся
			отрицательными, то обе координаты краёв (левого/правого или
			нижнего/верхнего) устанавливаются в среднее между ними значение.

		Возвращает ссылку на объект, на котором был вызван метод.
		'''
		if y is None:
			y = x

		self.left, self.right = Rect._inset_dimension(self.left,self.right,x)
		self.bottom, self.top = Rect._inset_dimension(self.bottom,self.top,y)

		return self

	def extrude(self,x,y=None):
		'''
		Выполняет действие, противоположное действию inset.
		'''
		if y is None:
			y = x

		return self.inset(-x,-y)

	def hasPoint(self,x,y=None):
		'''
		Определяет, принадлежит ли точка прямоугольнику.

		Точка, лежащая на границе прямоугольника, считается принадлежащей ему.
		'''
		if y is None:
			x, y = x

		return	(x >= self.left) and \
				(x <= self.right) and \
				(y >= self.bottom) and \
				(y <= self.top)

	def __eq__(self,other):
		try:
			return	self.left == other.left		\
				and	self.right == other.right	\
				and	self.bottom == other.bottom	\
				and	self.top == other.top
		except AttributeError:
			return False

	def __repr__(self):
		return '<Rect left={left} right={right} bottom={bottom} top={top}>'.format(**self.__dict__)
