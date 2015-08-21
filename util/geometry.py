# coding=UTF-8
import math

'''
Модуль содержит набор функций для геометрических преобразований в соответствии
	с соглашением о системах координат (см. fwk/doc/coordinate-systems.mdown).
'''

def degreeToRad(deg):
	'''
	Перевод градусов в радианы
	'''
	return (deg/180.0) * math.pi

def radToDegree(rad):
	'''
	Перевод радиан в градусы
	'''
	return (rad/math.pi) * 180.0

def directionFromAngle(angle):
	'''
	Вычисление вектора направления по углу поворота.
	'''
	angleRad = degreeToRad(angle)
	return math.sin(angleRad), math.cos(angleRad)

def perpendicularDirection(direction):
	'''
	Вычисление вектора направления, перпендикулярного заданному.
	'''
	return direction[1], -direction[0]

def rotateVector(vector,angle):
	'''
	Поворачивает вектор на заданный угол.
	'''
	r1 = directionFromAngle(angle)
	r0 = perpendicularDirection(r1)
	return vector[0] * r0[0] + vector[1] * r1[0],vector[0] * r0[1] + vector[1] * r1[1]

def distance2(pt1,pt2):
	'''
	Вычисляет квадрат расстояния между точками.
	'''
	return (pt1[0] - pt2[0])*(pt1[0] - pt2[0]) + (pt1[1] - pt2[1])*(pt1[1] - pt2[1])

def distance(pt1,pt2):
	'''
	Вычисляет расстояние между точками.
	'''
	return math.sqrt(distance2(pt1,pt2))
