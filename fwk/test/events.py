# coding=UTF-8
from unittest import TestCase
from mock import Mock

from fwk.util.events import Events

class EventsTest(TestCase):
	def setUp(self):
		self.events = Events()
		self.assertTrue(self.events != None)

class EventsBindTest(EventsTest):
	def setUp(self):
		EventsTest.setUp(self)
		self.callback0 = Mock()
		self.callback1 = Mock()

	def test_listen_trigger(self):
		self.events.on('boom',self.callback0)
		# No event if not listening
		self.events.trigger('boom',1,2,3)
		self.assertEqual(self.callback0.call_count,0)
		self.assertFalse(self.events.listening('boom'))

		# Event if listening
		self.events.listen('boom')
		self.assertTrue(self.events.listening('boom'))
		self.events.trigger('boom',1,2,3)
		self.callback0.assert_called_with(1,2,3)

		self.callback0.reset_mock()

		# Again no event when ignoring
		self.events.ignore('boom')
		self.assertFalse(self.events.listening('boom'))
		self.events.trigger('boom',1,2,3)
		self.assertEqual(self.callback0.call_count,0)

	def test_on_off(self):
		self.events.listen('bams')

		self.events.on('bams',self.callback1)
		self.events.off(event='bams')
		self.events.trigger('bams',1,2,3)
		self.assertEqual(self.callback0.call_count,0)

		self.events.on('bams',self.callback1)
		self.events.off(event='bams',callback=self.callback1)
		self.events.trigger('bams',1,2,3)
		self.assertEqual(self.callback0.call_count,0)

		self.events.on('bams',self.callback1)
		self.events.off(callback=self.callback1)
		self.events.trigger('bams',1,2,3)
		self.assertEqual(self.callback0.call_count,0)

class MyTestBaseEvents(Events):
	def __init__(self):
		Events.__init__(self)
		self.mock = Mock()

	events = [
		'boom',
		'boboom'
	]

	def boom(self,*args,**kwargs):
		self.mock('base:boom',self,*args,**kwargs)

	def boboom(self,*args,**kwargs):
		self.mock('base:boboom',self,*args,**kwargs)

	def on_tubudums(self,*args,**kwargs):
		self.mock('base:on_tubudums',self,*args,**kwargs)

class MyTestDerivedEvents(MyTestBaseEvents):
	events = [
		'budums',
		('tubudums','on_tubudums')
	]

	def boom(self,*args,**kwargs):
		self.mock('derived:boom',self,*args,**kwargs)

	@Events.important
	def boboom(self,*args,**kwargs):
		self.mock('derived:boboom',self,*args,**kwargs)

	def budums(self,*args,**kwargs):
		self.mock('derived:budums',self,*args,**kwargs)

class EventsInheritTest(TestCase):
	def setUp(self):
		self.events = MyTestDerivedEvents()

	def test_listening_events(self):
		self.assertTrue(self.events.listening('budums'))
		self.assertTrue(self.events.listening('boom'))
		self.assertTrue(self.events.listening('boboom'))
		self.assertFalse(self.events.listening('bams'))

	def test_base_event_trigger(self):
		self.events.mock.reset_mock()
		self.events.trigger('boom',1,2,3)
		self.events.mock.assert_called_with('derived:boom',self.events,1,2,3)

		self.events.mock.reset_mock()
		self.events.trigger('boboom',1,2,3)
		self.events.mock.assert_called_with('base:boboom',self.events,1,2,3)

	def test_derived_event_trigger(self):
		self.events.mock.reset_mock()
		self.events.trigger('budums',1,2,3)
		self.events.mock.assert_called_with('derived:budums',self.events,1,2,3)

		self.events.mock.reset_mock()
		self.events.trigger('tubudums',1,2,3)
		self.events.mock.assert_called_with('base:on_tubudums',self.events,1,2,3)
