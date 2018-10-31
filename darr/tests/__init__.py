from unittest import TestLoader, TextTestRunner, TestSuite

from . import test_array
from . import test_vlarraylist
from . import test_conversion

modules = [test_array, test_vlarraylist, test_conversion]

def test(verbosity=1):
    suite =TestSuite()
    for module in modules:
        suite.addTests(TestLoader().loadTestsFromModule(module))
    return TextTestRunner(verbosity=verbosity).run(suite)