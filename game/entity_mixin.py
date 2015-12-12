# coding=UTF-8
'''
Модуль содержит набор классов-примесей для игровых сущностей.
'''

from fwk.util.events import Events
from fwk.game.camera import CameraController
from fwk.util.animation import AnimationsList
from fwk.util.graphics import LoadTexture
from fwk.util.graphics import ApplyTextureAnchor

class Movement:
	'''
	Примесь, делающая сущность подвижной.

	Добавляет свойства:
		velocity		- вектор скорости движения сущности
		angularVelocity	- скорость вращения сущности

	При обновлении позиция и поворот сущности будут изменяться в соответствии
		с её скоростями.
	'''
	#TODO: Test it.
	@Events.before
	def spawn(self):
		self._velocity_x, self._velocity_y = 0, 0
		self._velocity_angular = 0

	def update(self,dt):
		x, y = self.position
		a = self.rotation

		x += self._velocity_x * dt
		y += self._velocity_y * dt
		a += self._velocity_angular * dt

		self.position = x, y
		self.rotation = a

	@property
	def velocity(self):
		return self._velocity_x, self._velocity_y

	@velocity.setter
	def velocity(self,value):
		self._velocity_x, self._velocity_y = value

	@property
	def angularVelocity(self):
		return self._velocity_angular

	@angularVelocity.setter
	def angularVelocity(self,value):
		self._velocity_angular = value

class Attached:
	'''
	Примесь, позволяющая привязать трансформацию сущности к другой сущности.
	Привязанная сущность будет двигаться вместе с сущностью, к которой
		она привязана.
	'''
	#TODO: Test it.
	@Events.before
	def spawn(self):
		self._parent = None

	def attach(self,parent,props=('position','rotation','scale'),events=('update','destroy')):
		'''
		Привязать сущность к новой родительской сущности.
		'''
		self._attach_props = props
		self._attach_events = events
		self._parent = parent

		self.unsubscribe_all()

		eparent = self._parent or self.game
		for event in self._attach_events:
			self.subscribe(eparent,event)

	def update(self,dt):
		if self._parent is None:
			return

		for prop in self._attach_props:
			value = getattr(self._parent,prop)
			setattr(self,prop,value)

class CameraTarget(CameraController):
	'''
	Примесь, делающая сущность объектом, управляющим камерой, а именно -
		передающим камере некоторые из своих свойств.

	Аттрибуты:
		cameraInitials	- словарь значений свойств камеры, устанавливаемых при
							её подключении.
		cameraAttachMap	- словарь, определяющий связь свойств камеры и
							сущности: ключи - имена свойств камеры, а значения
							- имена свойств сущности.
	'''
	#TODO: Test it.
	@Events.before
	def spawn(self):
		self.cameraAttachMap = {'focus':'position','rotation':'rotation'}
		self.cameraInitials = {'scale':1.0,'scale_x':1.0,'scale_y':1.0}

	def initCamera(self,camera):
		for prop, val in self.cameraInitials.items():
			setattr(camera,prop,val)
		self.updateCamera(camera)

	def updateCamera(self,camera):
		for cam_prop, my_prop in self.cameraAttachMap.items():
			setattr(camera,cam_prop,getattr(self,my_prop))

class Sprite:
	'''
	Примесь, рисующая сущность в виде спрайта.
	'''
	@Events.before
	def spawn(self):
		self._z_index = getattr(self,'z_index',0)
		self._sprite = None
		self._sprite_anchor = 'default'

	@property
	def sprite(self):
		return self._sprite.image if self._sprite is not None else None

	@sprite.setter
	def sprite(self,val):
		img = val
		if type(img) in (str,unicode):
			img = LoadTexture(img,anchor=self._sprite_anchor)

		if self._sprite is None:
			self._sprite = self.game.createSprite(img,zindex=self._z_index)
			self._sprite.visible = self.visible
		else:
			self._sprite.image = img

	@property
	def spriteAnchor(self):
		return self._sprite_anchor

	@spriteAnchor.setter
	def spriteAnchor(self,val):
		self._sprite_anchor = val
		if self._sprite:
			ApplyTextureAnchor(self._sprite.image,self._sprite_anchor)

	def on_show(self):
		if self._sprite is not None:
			self._sprite.visible = True

	def on_hide(self):
		if self._sprite is not None:
			self._sprite.visible = False

	def on_destroy(self):
		if self._sprite is not None:
			self._sprite.delete()

	def after_transform_changed(self):
		if self._sprite is not None:
			self.game.applySpriteTransform(self,self._sprite)

class Animation(Sprite):
	'''
	Примись, анимирующая спрайтовую сущность.
	'''
	def spawn(self):
		self._animations_list = None
		self._animation = None

	@property
	def animations(self):
		'''
		Свойство, возвращающее список анимаций.

		Установить можно передав имя JSON-файла с анимацией, словарь с
			описанием анимации или загруженный список анимаций.
		'''
		return self._animations_list

	@animations.setter
	def animations(self,val):
		if type(val) in (str,unicode):
			self._animations_list = AnimationsList.fromJSONFile(val)
		elif type(val) is AnimationsList:
			self._animations_list = val
		else:
			self._animations_list = AnimationsList(dict(val))

		if self._animation:
			self.animation = self._animation

	@property
	def animation(self):
		return self._animation

	@animation.setter
	def animation(self,val):
		self._animation = val
		if self._animations_list is not None:
			self.sprite = self._animations_list[val]
