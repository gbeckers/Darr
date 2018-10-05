import numpy as np
import shutil
import tempfile
import unittest
from contextlib import contextmanager
from numpy.testing import assert_equal, assert_array_equal

from darray.array import asdarray, create_darray, numtypes


@contextmanager
def tempdir(dirname='.', keep=False, report=False):
    try:
        tempdirname = tempfile.mkdtemp(dir=dirname)
        if report:
            print('created tempdir {}'.format(tempdirname))
        yield tempdirname
    except:
        raise
    finally:
        if not keep:
            shutil.rmtree(tempdirname)
            if report:
                print('removed temp dir {}'.format(tempdirname))


def check_arrayequaltoasdiskarray(ndarray):
    with tempdir() as dirname:
        dar = asdarray(path=dirname, array=ndarray, overwrite=True)
        assert_array_equal(dar[:], ndarray)
        assert_equal(dar.dtype, ndarray.dtype)
        assert_equal(dar.shape, ndarray.shape)

def check_arrayequaltocreatediskarray(ndarray, shape, dtype=None,
                                      chunklen=None):
    with tempdir() as dirname:
        dar = create_darray(path=dirname, shape=shape,
                            dtype=dtype, chunklen=chunklen,
                            overwrite=True)
        assert_array_equal(ndarray, dar[:])
        if ndarray.dtype != dar.dtype:
            raise TypeError(f'dtypes are different ({ndarray.dtype} vs '
                            f'{ndarray.dtype})')


class AsDiskArray(unittest.TestCase):

    def test_onedimensional(self):
        ndarray = np.arange(24)
        check_arrayequaltoasdiskarray(ndarray)

    def test_twodimensional(self):
        ndarray = np.arange(24).reshape(12, 2)
        check_arrayequaltoasdiskarray(ndarray)

    def test_threedimensional(self):
        ndarray = np.arange(24).reshape(4, 2, 3)
        check_arrayequaltoasdiskarray(ndarray)

    def test_numericdtypes(self):
        dtypes = numtypes.keys()
        for dtype in dtypes:
            ndarray = np.arange(24, dtype=dtype)
            check_arrayequaltoasdiskarray(ndarray)

    def test_fortranorder(self):
        ndarray = np.asarray(np.arange(24, dtype='float64'), order='F')
        check_arrayequaltoasdiskarray(ndarray)

    def test_littleendian(self):
        ndarray = np.arange(24, dtype='<f4')
        check_arrayequaltoasdiskarray(ndarray)

    def test_bigendian(self):
        ndarray = np.arange(24, dtype='>f4')
        check_arrayequaltoasdiskarray(ndarray)

    def test_emptyarray(self):
        ndarray = np.zeros(0, dtype='float64')
        check_arrayequaltocreatediskarray(ndarray=ndarray, shape=(0,),
                                          dtype='float64')


class CreateDiskArray(unittest.TestCase):

    def test_zerosfloat64default(self):
        ndarray = np.zeros(12, dtype='float64')
        check_arrayequaltocreatediskarray(ndarray=ndarray, shape=(12,))

    def test_twodimensional(self):
        ndarray = np.zeros(24, dtype='float64').reshape(12, 2)
        check_arrayequaltocreatediskarray(ndarray=ndarray, shape=(12,2),
                                          dtype='float64')

    def test_threedimensional(self):
        ndarray = np.zeros(24, dtype='float64').reshape(4, 2, 3)
        check_arrayequaltocreatediskarray(ndarray=ndarray, shape=(4, 2, 3),
                                          dtype='float64')

    def test_numericdtypes(self):
        dtypes = numtypes.keys()
        for dtype in dtypes:
            ndarray = np.zeros(24, dtype=dtype)
            check_arrayequaltocreatediskarray(ndarray=ndarray, shape=(24,),
                                              dtype=dtype)

    def test_chunked(self):
        ndarray = np.zeros(12, dtype='float64')
        for chunklen in (1,5,6,11,12,13):
            check_arrayequaltocreatediskarray(ndarray=ndarray, shape=(12,),
                                              dtype='float64',
                                              chunklen=chunklen)
        ndarray = np.zeros(13, dtype='float64')
        for chunklen in (1, 6, 7, 12, 13, 14):
            check_arrayequaltocreatediskarray(ndarray=ndarray, shape=(13,),
                                              dtype='float64',
                                              chunklen=chunklen)

    def test_chunkedthreedimensional(self):
        ndarray = np.zeros((12,3,7), dtype='float64')
        for chunklen in (1, 5, 6, 11, 12, 13):
            check_arrayequaltocreatediskarray(ndarray=ndarray, shape=(12,3,7),
                                              dtype='float64',
                                              chunklen=chunklen*21)
        ndarray = np.zeros((13,3,7), dtype='float64')
        for chunklen in (1, 6, 7, 12, 13, 14):
            check_arrayequaltocreatediskarray(ndarray=ndarray, shape=(13,3,7),
                                              dtype='float64',
                                              chunklen=chunklen*21)

    def test_toosmallchunklen(self):
        ndarray = np.zeros((12, 3, 7), dtype='float64')
        check_arrayequaltocreatediskarray(ndarray=ndarray, shape=(12, 3, 7),
                                          dtype='float64',
                                          chunklen=1)

    def test_emptyarray(self):
        ndarray = np.zeros((0,3,7), dtype='float64')
        check_arrayequaltocreatediskarray(ndarray=ndarray, shape=(0, 3, 7),
                                          dtype='float64',
                                          chunklen=1)


class IterView(unittest.TestCase):

    def test_defaultparams_fit(self):
        with tempdir() as dirname:
            dar = create_darray(path=dirname, shape=(12,),
                                dtype='int64', overwrite=True)
            l = [c for c in dar.iterview(chunklen=2)]
            assert_equal(len(l), 6)
            assert_array_equal(np.concatenate(l), dar[:])
            del l # otherwise file is still in use and may not be removed
            del dar

    def test_remainderfalse_fit(self):
        with tempdir() as dirname:
            dar = create_darray(path=dirname, shape=(12,),
                                dtype='int64', overwrite=True)
            l = [c for c in dar.iterview(chunklen=2, include_remainder=False)]
            assert_equal(len(l), 6)
            assert_array_equal(np.concatenate(l), dar[:])
            del l # otherwise file is still in use and may not be removed
            del dar

    def test_defaultparams_nofit(self):
        with tempdir() as dirname:
            dar = create_darray(path=dirname, shape=(13,),
                                dtype='int64', overwrite=True)
            l = [c for c in dar.iterview(chunklen=2)]
            assert_equal(len(l), 7)
            assert_array_equal(np.concatenate(l), dar[:])
            del l # otherwise file is still in use and may not be removed
            del dar

    def test_remainderfalse_nofit(self):
        with tempdir() as dirname:
            dar = create_darray(path=dirname, shape=(13,),
                                dtype='int64', overwrite=True)
            l = [c for c in
                 dar.iterview(chunklen=2, include_remainder=False)]
            assert_equal(len(l), 6)
            assert_array_equal(np.concatenate(l), dar[:12])
            del l # otherwise file is still in use and may not be removed
            del dar


class AppendData(unittest.TestCase):

    def test_appendlist1d(self):
        with tempdir() as dirname:
            dar = create_darray(path=dirname, shape=(2,),
                                dtype='int64', overwrite=True)
            dar.append([1,2])
            dar.append([3])
            assert_array_equal(np.array([0,0,1,2,3], dtype='int64'), dar[:])

    def test_appendlist2d(self):
        with tempdir() as dirname:
            dar = create_darray(path=dirname, shape=(2, 3),
                                dtype='int64', overwrite=True)
            dar.append([[1,2,3]])
            dar.append([[1,2,3],[4,5,6]])
            assert_array_equal(np.array([[0,0,0],[0,0,0],[1,2,3],[1,2,3],
                                         [4, 5, 6]], dtype='int64'), dar[:])

    def test_appendtoempty1d(self):
        with tempdir() as dirname:
            dar = create_darray(path=dirname, shape=(0,),
                                dtype='int64', overwrite=True)
            dar.append([1, 2, 3])
            assert_array_equal(np.array([1, 2, 3], dtype='int64'), dar[:])

    def test_appendtoempty2d(self):
        with tempdir() as dirname:
            dar = create_darray(path=dirname, shape=(0, 2),
                                dtype='int64', overwrite=True)
            dar.append([[1,2]])
            dar.append([[1,2],[3,4]])
            assert_array_equal(np.array([[1,2],[1,2],[3,4]], dtype='int64'),
            dar[:])

    def test_appendempty1d(self):
        with tempdir() as dirname:
            dar = create_darray(path=dirname, shape=(1,),
                                dtype='int64', overwrite=True)
            dar.append([])
            assert_array_equal(np.array([0], dtype='int64'), dar[:])

    def test_appendempty2d(self):
        with tempdir() as dirname:
            dar = create_darray(path=dirname, shape=(1, 2),
                                dtype='int64', overwrite=True)
            dar.append(np.zeros((0,2), dtype='int64'))
            assert_array_equal(np.array([[0,0]], dtype='int64'), dar[:])

    def test_appendemptytoempty1d(self):
        with tempdir() as dirname:
            dar = create_darray(path=dirname, shape=(0,),
                                dtype='int64', overwrite=True)
            dar.append([])
            assert_array_equal(np.array([], dtype='int64'), dar[:])

    def test_appendemptytoempty2d(self):
        with tempdir() as dirname:
            dar = create_darray(path=dirname, shape=(0, 2),
                                dtype='int64', overwrite=True)
            dar.append(np.zeros((0, 2), dtype='int64'))
            assert_array_equal(np.zeros((0,2), dtype='int64'), dar[:])

if __name__ == '__main__':
    unittest.main()