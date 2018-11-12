from unittest import TestLoader, TextTestRunner, TestSuite

from . import test_array
from . import test_raggedarray
from . import test_basedatadir

modules = [test_array, test_raggedarray, test_basedatadir]

def test(verbosity=1):
    suite =TestSuite()
    for module in modules:
        suite.addTests(TestLoader().loadTestsFromModule(module))
    return TextTestRunner(verbosity=verbosity).run(suite)