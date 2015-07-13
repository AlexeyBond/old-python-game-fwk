# coding=UTF-8

class Events(object):
	class Subscribtion:
		def __init__(self,publisher,subscriber,event):
			self.publisher = publisher
			self.subscriber = subscriber
			self.pub_event = event
			self.sub_event = event

		def enable(self):
			self.publisher.on(self.pub_event,self._callback)

		def disable(self):
			self.publisher.off(self.pub_event,self._callback)

		def _callback(self,*args,**kwargs):
			self.subscriber.trigger(self.sub_event,*args,**kwargs)

		def isLike(self,objs,events):
			if obj != None and (self.publisher not in objs):
				return False
			if event != None and (self.sub_event not in events):
				return False
			return True

	def __init__(self):
		self._handlers = {}
		self._listen = []
		self._subscriptions = []

		self._init_events()

	def _init_events(self):
		'''
		Приватный метод, внутри которого происходит МАГИЯ!
		'''
		events = []
		classes = ((self.__class__,) + self.__class__.__bases__)[::-1]

		# Собираем списки событий по всей иерархии.
		for cls in classes:
			events += [pair for pair in [ (e if type(e) in (tuple,list) else [e,e]) for e in getattr(cls,'events',())] if pair not in events]

		# И для каждого из них
		for pair in events:
			event = pair[0]
			handler = pair[1]
			self.listen(event)
			# Для каждого класса..
			for cls in classes:
				# Если обработчик определён в классе ..
				if handler in dir(cls):
					# то берём несвязанный метод-обработчик
					unbound = getattr(cls,handler)
					# Связываем и устанавливаем
					self.on(event,unbound.__get__(self),getattr(unbound,'_event_pre',False))

	def on(self,event,handler,important=False):
		'''
		Добавляет обработчик события.

		Обработчик, добавленный позже будет выполнен позже.
		(Если не передано неложное значение important - тогда
			обработчик окажется в начале списка.)
		'''
		lst = self._handlers.get(event,[])
		if important:
			lst.insert(0,handler)
		else:
			lst.append(handler)
		self._handlers[event] = lst

	def off(self,event=None,callback=None):
		'''
		Убирает обработчик события/убирает все обработчики события/убирает
			все обработчики всех событий.

		Аргументы:
			event		- событие
			callback	- обработчик
		'''
		# Just an optimisation
		if event == None and callback == None:
			self._handlers = {}
			return

		if event == None:
			for event in self._handlers.keys():
				self.off(event,callback)

		if callback == None:
			self._handlers[event] = []
			return

		if callback in self._handlers.get(event,[]):
			self._handlers[event].remove(callback)

	def trigger(self,event,*args,**kwargs):
		'''
		Произойти событие на объекте.
		(выполнить обработчики, если слушаем событие)

		Sorry for my bad russian.
		'''
		if event not in self._listen:
			return
		lst = self._handlers.get(event,())
		for cb in lst:
			cb(*args,**kwargs)

	def event(self,name,*args,**kwargs):
		'''
		Возвращает callable-объект, при вызове которого на данном объекте
			произойдёт заданное собыьие с заданными параметрами.

		Вызов
		myEvents.event('boom',1,foo='bar')(2,3,bar='baz')

		эквивалентен вызову
		myEvents.trigger('boom',1,2,3,foo='bar',bar='baz')
		'''
		def _event(*args_i,**kwargs_i):
			kwa = {}
			kwa.update(kwargs)
			kwa.update(kwargs_i)
			return self.trigger(name,*(args+args_i),**kwa)
		return _event

	def listen(self,event,listen=True):
		'''
		Слушать событие. Или не слушать если listen=False
		'''
		if (event in self._listen) != listen:
			getattr(self._listen,'append' if listen else 'remove')(event)

	def ignore(self,event,ignore=True):
		'''
		То же, что и listen, только наоборот.
		'''
		return self.listen(event,not ignore)

	def listening(self,event):
		'''
		Слушаем ли событие?
		'''
		return event in self._listen

	def subscribe(self,obj,*events):
		'''
		Подписаться на событие другого объекта
		'''
		for event in events:
			if type(event) in (tuple,list):
				self.subscribe(obj,*event)
			else:
				subscribtion = Events.Subscribtion(obj,self,event)
				subscribtion.enable()
				self._subscriptions.append(subscribtion)

	def unsubscribe_all(self):
		'''
		Отписаться от всех подписок на события
		'''
		for subscription in self._subscriptions:
			subscription.disable()
		self._subscriptions = []

	def unsubscribe(self,objects=None,events=None):
		'''
		Отписаться от отдельных объектов/событий
		'''
		#TODO: Добавить тесты.
		selected = []
		for subscription in self._subscriptions:
			if subscription.isLike(objects,events):
				selected.append(subscription)
		for ssub in selected:
			ssub.disable()
			self._subscriptions.remove(ssub)

	@staticmethod
	def important(handler):
		'''
		Декоратор, указывающий, что данный обработчик события должен
			быть выполнен как можно раньше.
		'''
		handler._event_pre = True
		return handler

class Shedule(object):
	class Task:
		def __init__(self,time,callback,cargs,ckwargs):
			self._time = time
			self.execute = lambda: callback(*cargs,**ckwargs)

		def __cmp__(self,other):
			return self._time.__cmp__(other._time)

	'''
	Расписание событий. Позволяет произойти события (или вызвать коллбэк) в
		заданное время.

	Доктор прописал использовать следующим образом:

	e = Events()
	s = Shedule()

	s.sheduleIn(100,e.event('boom',1,2,3,foo='bar'))

	Ну или так:

	s.sheduleAfter(100,lambda x: cow.say('Hello, '+x),'world')
	'''
	#TODO: Добавить тесты.
	def __init__(self):
		self._tasks = []
		self.currentTime = 0

	def perform_until_time(self,time):
		'''
		Выполнить все задачи, запланированные до заданного времени.
		'''
		while len(self._tasks) > 0:
			task = self._tasks[0]
			if task._time > time:
				return
			task.execute()
			self._tasks.remove(task)

	def sheduleIn(self,time,callcack,*args,**kwargs):
		'''
		Запланировать событие на заданное время.
		'''
		self._tasks.append(Shedule.Task(time,callcack,args,kwargs))
		self._tasks.sort()

	def sheduleAfter(self,timeDelta,*args,**kwargs):
		'''
		Запланировать событие через заданный промежуток времени после
			текущего момента.
		'''
		return self.sheduleIn(self.currentTime + timeDelta,*args,**kwargs)

	def update(self,dt):
		'''
		Обновляет текущее время в соответствии с прошедшим промежутком
			времени (dt), а так же выполняет все задачи, запланированные
			к новому времени.
		'''
		self.currentTime += dt
		self.perform_until_time(self.currentTime)
