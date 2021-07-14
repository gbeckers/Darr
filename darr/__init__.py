from .array import *
from .raggedarray import *
from .datadir import DataDir, create_datadir
from .tests import test

from . import _version
__version__ = _version.get_versions()['version']
