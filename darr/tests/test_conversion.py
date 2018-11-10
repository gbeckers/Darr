import unittest

import numpy as np
from numpy.testing import assert_array_equal

from darr.array import asarray, create_array
from darr.conversion import aszarrarray
from .utils import tempdir

class AsZarrArray(unittest.TestCase):

    def test_darrtozarrconversiontofile(self):
        with tempdir() as dirname:
            a = np.arange(10, dtype='float64')
            da = asarray(path=dirname, array=a, overwrite=True)
            za = aszarrarray(da, store=f'{dirname}/array.zarr')
            assert_array_equal(za[:], da[:])

    def test_darrpathtozarrconversiontofile(self):
        with tempdir() as dirname:
            a = np.arange(10, dtype='float64')
            da = asarray(path=dirname, array=a, overwrite=True)
            za = aszarrarray(dirname, store=f'{dirname}/array.zarr')
            assert_array_equal(za[:], da[:])

    def test_darrtozarrconversionmetadata(self):
        with tempdir() as dirname:
            metadata = {'a': 1, 'b': [1, 3, 4.0], 'c': "hi"}
            da = create_array(path=dirname, shape=(2,), fill=0,
                               dtype='int64', overwrite=True,
                               metadata=metadata)
            za = aszarrarray(da, store=f'{dirname}/array.zarr')
            self.assertEqual(dict(za.attrs), metadata)

    def test_darrtozarrwronginput(self):
        self.assertRaises(Exception, aszarrarray, [1,2,3], store='array.zarr')
