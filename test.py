# coding=UTF-8
import unittest

# from fwk.test.all import *

def load_tests(loader, tests, pattern):
	return unittest.defaultTestLoader.discover('fwk','test_*.py')

unittest.main(verbosity=100)
