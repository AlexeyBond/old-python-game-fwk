# coding=UTF-8

class Events(object):
	class Subscribtion:
		def __init__(self,obj,event,callback):
			self.obj = obj
			self.event = event
			self.callback = callback

			self.obj.on(self.event,self.callback)

		def unsubscribe(self):
			self.obj.off(self.event,self.callback)

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

	def subscribe(self,obj,event):
		'''
		Подписаться на событие другого объекта
		'''
		callback = lambda *args, **kwargs: self.trigger(event,*args,**kwargs)
		self._subscriptions.append(Events.Subscribtion(obj,event,callback))

	#TODO: Добавить отписку от отдельных событий/объектов.
	def unsubscribe_all(self):
		'''
		Отписаться от всех подписок на события
		'''
		for subscription in self._subscriptions:
			subscription.unsubscribe()
		self._subscriptions = []

	@staticmethod
	def important(handler):
		'''
		Декоратор, указывающий, что данный обработчик события должен
			быть выполнен как можно раньше.
		'''
		handler._event_pre = True
		return handler
