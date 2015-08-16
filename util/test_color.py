# coding=UTF-8
from unittest import TestCase

from fwk.util.color import Color

class ColorRGBTest(TestCase):
	def setUp(self):
		self.color = Color()

	def test_rgb_initial(self):
		self.assertEqual(self.color.rgb,(1.,1.,1.))

	def test_rgb_float_assign(self):
		self.color.rgb = 0., 0., 0.
		self.assertEqual(self.color.rgb,(0.,0.,0.))

	def test_rgb_int_assign(self):
		self.color.rgb = 0, 255, 255
		self.assertEqual(self.color.rgb,(0.,1.,1.))

class ColorRGBATest(TestCase):
	def setUp(self):
		self.color = Color()

	def test_rgb_initial(self):
		self.assertEqual(self.color.rgba,(1.,1.,1.,1.))

	def test_rgb_float_assign(self):
		self.color.rgba = 0., 0., 0.,0.5
		self.assertEqual(self.color.rgba,(0.,0.,0.,0.5))
		self.assertEqual(self.color.rgb,(0.,0.,0.))

	def test_rgb_int_assign(self):
		self.color.rgba = 0, 255, 255, 0
		self.assertEqual(self.color.rgba,(0.,1.,1.,0.))
		self.assertEqual(self.color.rgb,(0.,1.,1.))

class ColorConstructorTest(TestCase):
	def test_construct_rgb(self):
		color = Color(.32, .54, .31)
		self.assertEqual(color.rgba,(.32, .54, .31, 1.))

	def test_construct_rgba(self):
		color = Color(.72, .63, .99, .5)
		self.assertEqual(color.rgba,(.72, .63, .99, .5))
