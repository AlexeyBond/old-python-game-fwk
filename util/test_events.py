# coding=UTF-8
from unittest import TestCase
from mock import Mock

from fwk.util.events import Events
from fwk.util.events import Schedule

class EventsTest(TestCase):
	def setUp(self):
		self.events = Events()
		self.assertTrue(self.events is not None)

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

	def test_multiple_events(self):
		self.events.on('boom',self.callback0)
		self.events.on('bams',self.callback1)

		self.events.listen('boom')
		self.events.listen('bams')

		self.events.trigger('boom',1,2,3)
		self.callback0.assert_called_with(1,2,3)
		self.assertEqual(self.callback1.call_count,0)

		self.callback0.reset_mock()
		self.callback1.reset_mock()

		self.events.trigger('bams',3,2,1)
		self.callback1.assert_called_with(3,2,1)
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

class MyTestMixinEvents:
	events = [
		'mixboom'
	]

	@Events.before
	def mixboom(self,*args,**kwargs):
		self.mock('mixin:mixboom',self,*args,**kwargs)

class MyTestDerivedEvents(MyTestBaseEvents,MyTestMixinEvents):
	events = [
		'budums',
		('tubudums','on_tubudums')
	]

	def boom(self,*args,**kwargs):
		self.mock('derived:boom',self,*args,**kwargs)

	@Events.before
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
		self.assertTrue(self.events.listening('mixboom'))
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

	def test_mixin_event_trigger(self):
		self.events.mock.reset_mock()
		self.events.trigger('mixboom',3,2,1)
		self.events.mock.assert_called_with('mixin:mixboom',self.events,3,2,1)

class EventsSubscribeTest(TestCase):
	def setUp(self):
		self.eventsa = Events()
		self.eventsb = MyTestBaseEvents()

	def test_single_subscription(self):
		self.eventsa.listen('boom')
		self.eventsb.subscribe(self.eventsa,'boom')

		self.assertTrue(self.eventsa.listening('boom'))
		self.assertTrue(self.eventsb.listening('boom'))

		self.eventsa.trigger('boom',1,2,3,4)
		self.eventsb.mock.assert_called_with('base:boom',self.eventsb,1,2,3,4)

	def test_list_subscripption(self):
		self.eventsa.listen('boom')
		self.eventsa.listen('boboom')
		self.eventsb.subscribe(self.eventsa,['boom','boboom'])
		# self.eventsb.subscribe(self.eventsa,'boom')
		# self.eventsb.subscribe(self.eventsa,'boboom')

		self.eventsb.mock.reset_mock()
		self.eventsa.trigger('boom',1,2,3,4)
		self.eventsb.mock.assert_called_with('base:boom',self.eventsb,1,2,3,4)

		self.eventsb.mock.reset_mock()
		self.eventsa.trigger('boboom',4,3,2,1)
		self.eventsb.mock.assert_called_with('base:boboom',self.eventsb,4,3,2,1)

class EventsCallbackTest(TestCase):
	def setUp(self):
		self.mock = Mock()
		self.events = Events()
		self.events.on('boom',self.mock)
		self.events.listen('boom')

	def test_create_callback(self):
		cb = self.events.event('boom',1,2,bar='foo')
		self.assertTrue(callable(cb))

	def test_call_no_args(self):
		cb = self.events.event('boom',1,2,bar='foo')
		cb()
		self.mock.assert_called_with(1,2,bar='foo')

	def test_call_additional_args(self):
		cb = self.events.event('boom',1,2,bar='foo',baz='asd')
		cb(3,4,baz='foo',qwe='rty')
		self.mock.assert_called_with(1,2,3,4,bar='foo',baz='foo',qwe='rty')

class EventsScheduleTest(TestCase):
	def setUp(self):
		self.mock1 = Mock()
		self.mock2 = Mock()
		self.schedule = Schedule()

	def test_schedule_in(self):
		self.schedule.scheduleIn(20,self.mock2,1,2,3,bar='baz')
		self.schedule.scheduleIn(10,self.mock1,'qwe',asd='fgh')

		self.schedule.perform_until_time(5)
		self.assertEqual(self.mock1.call_count,0)
		self.assertEqual(self.mock2.call_count,0)

		self.schedule.perform_until_time(11)
		self.mock1.assert_called_with('qwe',asd='fgh')
		self.mock1.reset_mock()
		self.assertEqual(self.mock2.call_count,0)

		self.schedule.perform_until_time(21)
		self.assertEqual(self.mock1.call_count,0)
		self.mock2.assert_called_with(1,2,3,bar='baz')

	def test_schedule_after(self):
		self.schedule.scheduleAfter(10,self.mock1,1,2,3,asd='bar')

		self.schedule.update(9)
		self.assertEqual(self.mock1.call_count,0)

		self.schedule.update(2)
		self.mock1.assert_called_with(1,2,3,asd='bar')
		self.mock1.reset_mock()

		self.schedule.update(2)
		self.assertEqual(self.mock1.call_count,0)
