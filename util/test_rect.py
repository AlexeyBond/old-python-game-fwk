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

	def test_scale(self):
		self.rect.scale(0.5,origin='center-center')
		self.assertEqual(self.rect.width,50)
		self.assertEqual(self.rect.height,50)
		self.assertEqual(self.rect.left,425)
		self.assertEqual(self.rect.bottom,125)

class RectMoveTest(TestCase):
	def setUp(self):
		self.rect = Rect(top=1,bottom=-1,left=-1,right=1)
	def test_move_center(self):
		self.rect.moveTo(20,10,'center-center')
		self.assertEqual(self.rect.top,11)
		self.assertEqual(self.rect.right,21)
		self.assertEqual(self.rect.width,2)
		self.assertEqual(self.rect.height,2)

	def test_move_bottom_left(self):
		self.rect.moveTo(30,40,'bottom-left')
		self.assertEqual(self.rect.bottom,40)
		self.assertEqual(self.rect.left,30)
		self.assertEqual(self.rect.width,2)
		self.assertEqual(self.rect.height,2)

class RectInsetTest(TestCase):
	def setUp(self):
		self.rect = Rect(bottom=100,top=200,left=10,right=20)
	def test_inset_separate_values(self):
		self.rect.inset(1,10)
		self.assertEqual(self.rect.bottom,110)
		self.assertEqual(self.rect.top,190)
		self.assertEqual(self.rect.left,11)
		self.assertEqual(self.rect.right,19)

	def test_inset_single_value(self):
		self.rect.inset(2)
		self.assertEqual(self.rect.bottom,102)
		self.assertEqual(self.rect.top,198)
		self.assertEqual(self.rect.left,12)
		self.assertEqual(self.rect.right,18)

	def test_inset_with_underflow(self):
		self.rect.inset(51)
		self.assertEqual(self.rect.bottom,150)
		self.assertEqual(self.rect.height,0)
		self.assertEqual(self.rect.left,15)
		self.assertEqual(self.rect.width,0)

class RectCloneAndMagic(TestCase):
	def test_clone_and_compare(self):
		rect1 = Rect(left=10,bottom=30,width=100,height=410)
		rect2 = rect1.clone()
		self.assertEqual(rect1,rect2)
		rect2 = rect1.clone().inset(10)
		self.assertNotEqual(rect1,rect2)

	def test_string_representation(self):
		'''
		Тест, проверяющий наглядность и однозначность строкового представления
			объекта прямоугольника.

		Данный тест создан поздно ночью, поэтому весьма оправданы могут быть
			сомнения как в корректности метода лежащего в его основе так и в
			адекватности автора данного теста в момент его (теста) написания.
		'''
		rect = Rect(left=432548,right=876945,bottom=129543,top=410666)
		srepr = repr(rect)
		self.assertTrue('Rect' in srepr)
		self.assertTrue('432548' in srepr)
		self.assertTrue('876945' in srepr)
		self.assertTrue('129543' in srepr)
		self.assertTrue('410666' in srepr)
