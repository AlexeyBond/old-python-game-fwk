#!/usr/bin/python
# coding=UTF-8
import os
import unittest

os.chdir('..')

def load_tests(loader, tests, pattern):
	return unittest.defaultTestLoader.discover('.','test_*.py')

unittest.main(verbosity=100)
