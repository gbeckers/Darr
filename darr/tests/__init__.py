from unittest import TestLoader, TextTestRunner, TestSuite

from . import test_array
from . import test_raggedarray
from . import test_basedatadir
from . import test_utils
from . import test_numtype
from . import test_basedatadir
from . import test_metadata

modules = [test_array, test_raggedarray, test_basedatadir, test_utils,
           test_numtype, test_basedatadir, test_metadata]

def test(verbosity=1):
    suite = TestSuite()
    for module in modules:
        suite.addTests(TestLoader().loadTestsFromModule(module))
    return TextTestRunner(verbosity=verbosity).run(suite)