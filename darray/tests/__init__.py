from unittest import TestLoader, TextTestRunner, TestSuite

from . import test_darray
from . import test_darraylist

modules = [test_darray, test_darraylist]

def test(verbosity=1):
    suite =TestSuite()
    for module in modules:
        suite.addTests(TestLoader().loadTestsFromModule(module))
    return TextTestRunner(verbosity=verbosity).run(suite)