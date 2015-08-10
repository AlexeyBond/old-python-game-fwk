# coding=UTF-8
import inspect

class Events(object):
	'''
	Базовый класс для классов объектов, на которых могут происходить события.
	Событие состоит из имени события, списка аргументов и списка (в смысле
		словаря) именованых аргументов.
	Когда событие происходит на объекте - происходит последовательный вызов
		всех обработчиков назначеных для обработки события с именем
		произошедшего события на данном объекте. Если объект не слушает
		(listen) событие с данным именем, то не происходит ничего.
	Объект (subscriber) может быть подписан на отдельные события другого
		(publisher) объекта. Это означает, что если событие, с заданным именем
		происходит на объекте publisher, то оно происходит и на объекте
		subscriber.

	Обработчик для события может быть добавлен различными способами:
	1) Явно при помощи вызова on:
		on(<имя_события>,<обработчик>,[<добавить_в_начало>])
		Если посдедний параметр - истина, то обработчик будет добавлен в начало
			списка обработчиков и, когда событие произойдёт, будет вызван до
			всех обработчиков, добавленных на момент вызова on; иначе -
			в конец/после.
	2) Через описание в классе:
		class MyClass(Events):
			events = [
				'boom',
				('boom-boboom','on_bubudum')
			]
		При вызове конструктора класса Events происходит сканнирование всей
			иерархии классов на наличие статических полей с именем events;
			такие поля должны быть списками, содержащими строки и/или кортежи
			из 2-х строк. В случае кортежа - первое значение интерпретируется
			как имя события, а второе - как имя метода-обработчика, а в случае
			строки - имя и события и обработчика считаются равными этой строке.
		Затем происходит поиск по всей иерархии методов с именем метода
			обработчика. И они добавляются в список обработчиков события с
			заданным именем. Добавление происходит при помощи метода on.
			Добавление происходит в конец списка обработчиков, если метод не
			определён с декоратором @Events.before - в случае использования
			этого декоратора - обработчик добасляется в начало списка.
		Так же все события описаные в поле events автоматически слушаются
			объектом после его создания.
		Преимущества такого подхода перед использованием перегрузки методов -
			отсутствие необходимости вызова метода родительского класса в
			методе наследника, а так же возможность легко расширять функционал
			объекта, добавляя примеси, определяющие обработчики событий, не
			теряя гибкости управления порядком выполнения обработчиков.
	'''
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
			if objs != None and (self.publisher not in objs):
				return False
			if events != None and (self.sub_event not in events):
				return False
			return True

		def __repr__(self):
			return '<subscription to event "{pub_event}" of {publisher} as "{sub_event}">'.format(**(self.__dict__))

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
		classes = inspect.getmro(self.__class__)[::-1]

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

	def on(self,event,handler,before=False):
		'''
		Добавляет обработчик события.

		Обработчик, добавленный позже будет выполнен позже.
		(Если не передано неложное значение before - тогда
			обработчик окажется в начале списка.)
		'''
		lst = self._handlers.get(event,[])
		if before:
			lst.insert(0,handler)
		else:
			lst.append(handler)
		self._handlers[event] = lst

		return self

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
			return self

		if event == None:
			for event in self._handlers.keys():
				self.off(event,callback)

		if callback == None:
			self._handlers[event] = []
			return self

		if callback in self._handlers.get(event,[]):
			self._handlers[event].remove(callback)

		return self

	def trigger(self,event,*args,**kwargs):
		'''
		Произойти событие на объекте.
		(выполнить обработчики, если слушаем событие)

		Sorry for my bad russian.
		'''
		if event not in self._listen:
			return self
		lst = self._handlers.get(event,())
		for cb in lst:
			cb(*args,**kwargs)

		return self

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

		return self

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

		return self

	def unsubscribe_all(self):
		'''
		Отписаться от всех подписок на события
		'''
		for subscription in self._subscriptions:
			subscription.disable()
		self._subscriptions = []

		return self

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

		return self

	@staticmethod
	def before(handler):
		'''
		Декоратор, указывающий, что данный обработчик события должен
			быть выполнен как можно раньше.
		'''
		handler._event_pre = True
		return handler

class Schedule(object):
	class Task:
		def __init__(self,time,callback,cargs,ckwargs):
			self._time = time
			self.execute = lambda: callback(*cargs,**ckwargs)

		def __cmp__(self,other):
			return cmp(self._time,other._time)

	'''
	Расписание событий. Позволяет произойти события (или вызвать коллбэк) в
		заданное время.

	Доктор прописал использовать следующим образом:

	e = Events()
	s = Schedule()

	s.scheduleIn(100,e.event('boom',1,2,3,foo='bar'))

	Ну или так:

	s.scheduleAfter(100,lambda x: cow.say('Hello, '+x),'world')
	'''
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

	def scheduleIn(self,time,callcack,*args,**kwargs):
		'''
		Запланировать событие на заданное время.
		'''
		self._tasks.append(Schedule.Task(time,callcack,args,kwargs))
		self._tasks.sort()

		return self

	def scheduleAfter(self,timeDelta,*args,**kwargs):
		'''
		Запланировать событие через заданный промежуток времени после
			текущего момента.
		'''
		return self.scheduleIn(self.currentTime + timeDelta,*args,**kwargs)

	def update(self,dt):
		'''
		Обновляет текущее время в соответствии с прошедшим промежутком
			времени (dt), а так же выполняет все задачи, запланированные
			к новому времени.
		'''
		self.currentTime += dt
		self.perform_until_time(self.currentTime)
