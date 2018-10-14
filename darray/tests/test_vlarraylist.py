import unittest
import numpy as np
from numpy.testing import assert_equal, assert_array_equal


from darray.vlarraylist import create_vlarraylist
from .utils import tempdir


class CreatedArrayList(unittest.TestCase):

    def test_1darray(self):
        with tempdir() as dirname:
            dal = create_vlarraylist(dirname, atom=(), dtype='float64',
                                     metadata=None, accessmode='r+',
                                     overwrite=True)
            assert len(dal) == 0
            assert dal.atom == ()
            assert dal.dtype == np.float64
            a = np.array([0,1,2,3], dtype='float64')
            dal.append(a)
            assert len(dal) == 1
            assert_equal(dal[0], a)

    def test_2darray(self):
        with tempdir() as dirname:
            dal = create_vlarraylist(dirname, atom=(2,), dtype='float64',
                                     metadata=None, accessmode='r+',
                                     overwrite=True)
            assert len(dal) == 0
            assert dal.atom == (2,)
            assert dal.dtype == np.float64
            a = np.array([[0,1],[2,3],[4,5]], dtype='float64')
            dal.append(a)
            assert len(dal) == 1
            assert_equal(dal[0], a)


