from unittest import TestLoader, TextTestRunner, TestSuite

from . import test_diskarray

modules = [test_diskarray]

def test(verbosity=1):
    suite =TestSuite()
    for module in modules:
        suite.addTests(TestLoader().loadTestsFromModule(module))
    return TextTestRunner(verbosity=verbosity).run(suite)