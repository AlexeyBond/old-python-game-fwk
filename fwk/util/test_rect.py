# coding=UTF-8
from unittest import TestCase

from fwk.util.rect import Rect

class RectSizeTest(TestCase):
	def test_sizes_from_coords(self):
		rect = Rect(top=33,bottom=22,left=10,right=20)
		self.assertEqual(rect.width,10)
		self.assertEqual(rect.height,11)

	def test_sizes_from_sizes(self):
		rect = Rect(top=23,height=48,left=64,width=67)
		self.assertEqual(rect.width,67)
		self.assertEqual(rect.height,48)

class RectResizeTest(TestCase):
	def setUp(self):
		self.rect = Rect(top=200,bottom=100,left=400,right=500)
	def test_resize_center(self):
		self.rect.resize(width=200,height=50,origin='center-center')
		self.assertEqual(self.rect.width,200)
		self.assertEqual(self.rect.height,50)
		self.assertEqual(self.rect.top,175)
		self.assertEqual(self.rect.right,550)

	def test_resize_bottom_left(self):
		self.rect.resize(width=253,height=68,origin='bottom-left')
		self.assertEqual(self.rect.width,253)
		self.assertEqual(self.rect.height,68)
		self.assertEqual(self.rect.bottom,100)
		self.assertEqual(self.rect.left,400)

	def test_resize_top_right(self):
		self.rect.resize(width=253,height=68,origin='top-right')
		self.assertEqual(self.rect.width,253)
		self.assertEqual(self.rect.height,68)
		self.assertEqual(self.rect.top,200)
		self.assertEqual(self.rect.right,500)

class RectMoveTest(TestCase):
	def test_move_center(self):
		pass
