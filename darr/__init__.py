from .array import *
from .raggedarray import *
from .datadir import DataDir, create_datadir
from .tests import test

from . import _version
__version__ = _version.get_versions()['version']

def open(path, accessmode='r'):
    dd = DataDir(path)
    arraytype = dd.read_jsondict('arraydescription.json')['darrobject']
    if arraytype == 'Array':
        return Array(path=path, accessmode=accessmode)
    elif arraytype == 'RaggedArray':
        return RaggedArray(path=path, accessmode=accessmode)
    else:
        raise ValueError(f"'{arraytype}' not supported in this version of "
                         f"Darr ({__version__}) ")

