import os
import unittest
import numpy as np
from numpy.testing import assert_equal, assert_array_equal

from pathlib import Path
from darr.vlarraylist import create_vlarraylist, asvlarraylist, \
    delete_vlarraylist
from .utils import tempdir


class CreateArrayList(unittest.TestCase):

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


class ClassAsArrayList(unittest.TestCase):

    def test_1darray(self):
        with tempdir() as dirname:
            na = [[1,2,3],[4,5,6]]
            dal = asvlarraylist(dirname, na, overwrite=True)
            assert_array_equal(dal[0], na[0])
            assert_array_equal(dal[1], na[1])


class DeleteArrayList(unittest.TestCase):

    def test_simpledeletevlarray(self):
        with tempdir() as dirname:
            dalpath = Path(dirname).joinpath('temp.dal')
            dal = create_vlarraylist(dalpath, atom=(2,), overwrite=True)
            delete_vlarraylist(dal)
            assert_equal(len(os.listdir(dirname)), 0)


