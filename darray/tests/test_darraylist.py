import unittest

from darray.vlarraylist import create_vlarraylist
from .utils import tempdir

class CreatedArrayList(unittest.TestCase):

    def test_createone1darray(self):
        with tempdir() as dirname:
            dal = create_vlarraylist(dirname, shape=(0,), dtype='float64',
                                     metadata=None, accessmode='r+',
                                     overwrite=True)
            assert len(dal) == 0
