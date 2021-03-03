from .array import *
from .raggedarray import *
from .datadir import DataDir, create_datadir
from .tests import test

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
