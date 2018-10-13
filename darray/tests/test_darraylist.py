import unittest

from darray.arraylist import create_darraylist
from .utils import tempdir

class CreatedArrayList(unittest.TestCase):

    def test_createone1darray(self):
        with tempdir() as dirname:
            dal = create_darraylist(dirname, shape=(0,), dtype='float64',
                                    metadata=None, accessmode='r+',
                                    overwrite=True)
            assert len(dal) == 0
