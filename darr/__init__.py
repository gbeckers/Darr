from .array import *
from .raggedarray import *
from .tests import test

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
