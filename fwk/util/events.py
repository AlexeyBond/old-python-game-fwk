# coding=UTF-8

class Events:
	def __init__(self):
		self._handlers = {}
		self._listen = []

		self._init_events()

	def _init_events(self):
		'''
		Приватный метод, внутри которого происходит МАГИЯ!
		'''
		events = []
		classes = (self.__class__,) + self.__class__.__bases__

		# Собираем списки событий по всей иерархии.
		for cls in classes:
			events += [e for e in getattr(cls,'events',()) if e not in events]

		# И для каждого из них
		for event in events:
			self.listen(event)
			# Для каждого класса..
			for cls in classes[::-1]:
				# Если обработчик определён в классе ..
				if event in dir(cls):
					# то берём несвязанный метод-обработчик
					unbound = getattr(cls,event)
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

	def listen(self,event):
		'''
		Слушать событие
		'''
		if event not in self._listen:
			self._listen.append(event)

	def ignore(self,event):
		'''
		Не слушать событие
		'''
		if event in self._listen:
			self._listen.remove(event)

	def listening(self,event):
		'''
		Слушаем ли событие?
		'''
		return event in self._listen

	@staticmethod
	def important(handler):
		'''
		Декоратор, указывающий, что данный обработчик события должен
			быть выполнен как можно раньше.
		'''
		handler._event_pre = True
		return handler
