from unittest import TestLoader, TextTestRunner, TestSuite

from . import test_array
from . import test_vlarraylist

modules = [test_array, test_vlarraylist]

def test(verbosity=1):
    suite =TestSuite()
    for module in modules:
        suite.addTests(TestLoader().loadTestsFromModule(module))
    return TextTestRunner(verbosity=verbosity).run(suite)