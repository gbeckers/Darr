import os
import unittest
import numpy as np
import tempfile
from numpy.testing import assert_equal, assert_array_equal
from pathlib import Path
from darr.raggedarray import create_raggedarray, asraggedarray, \
    delete_raggedarray, truncate_raggedarray, RaggedArray, create_datadir
from darr.readcoderaggedarray import readcode

from darr.utils import tempdirfile
from .test_array import DarrTestCase


class CreateRaggedArray(DarrTestCase):

    def test_1darray(self):
        with tempdirfile() as filename:
            dal = create_raggedarray(filename, atom=(), dtype='float64')
            self.assertEqual(len(dal), 0)
            self.assertEqual(dal.atom, ())
            self.assertEqual(dal.dtype, np.float64)
            a = np.array([0,1,2,3], dtype='float64')
            dal.append(a)
            self.assertEqual(len(dal) ,1)
            assert_equal(dal[0], a)

    def test_2darray(self):
        with tempdirfile() as filename:
            dal = create_raggedarray(filename, atom=(2,), dtype='float64')
            self.assertEqual(len(dal), 0)
            self.assertEqual(dal.atom, (2,))
            self.assertEqual(dal.dtype, np.float64)
            a = np.array([[0,1],[2,3],[4,5]], dtype='float64')
            dal.append(a)
            self.assertEqual(len(dal), 1)
            assert_equal(dal[0], a)

    def test_setaccessmode(self):
        with tempdirfile() as filename:
            dal = create_raggedarray(filename, atom=(), dtype='float64')
            self.assertEqual(dal.accessmode, 'r+')
            self.assertEqual(dal._metadata.accessmode, 'r+')
            self.assertEqual(dal._values.accessmode, 'r+')
            self.assertEqual(dal._indices.accessmode, 'r+')
            dal.accessmode = 'r'
            self.assertEqual(dal.accessmode, 'r')
            self.assertEqual(dal._metadata.accessmode, 'r')
            self.assertEqual(dal._values.accessmode, 'r')
            self.assertEqual(dal._indices.accessmode, 'r')
            self.assertRaises(ValueError, setattr, dal, 'accessmode', 'w')
            self.assertRaises(ValueError, setattr, dal, 'accessmode', 'a')

    def test_overwriteremoveexistingmetadata(self):
        with tempdirfile() as filename:
            metadata = {'a': 1}
            dal1 = create_raggedarray(filename, atom=(), dtype='float64',
                                     metadata=metadata)
            dal2 = create_raggedarray(filename, atom=(), dtype='float64',
                                      overwrite=True)
            self.assertEqual(0, len(dal2.metadata))
            self.assertEqual(False, dal2.metadata.path.exists())

    def test_invalidatom(self):
        with tempdirfile() as filename:
            self.assertRaises(TypeError, create_raggedarray, filename, atom=3)


class RaggedArrayIndexing(DarrTestCase):

    def setUp(self):
        self.temparpath = Path(tempfile.mkdtemp()) / 'testra.ra'
        self.tempar = create_raggedarray(self.temparpath, atom=(),
                                         dtype='float64')
        self.input = np.array([[1,2,3,4],[4,5,6,7]], dtype='float64')
        self.tempar.iterappend(self.input)

    def tearDown(self):
        delete_raggedarray(self.tempar)

    def test_validint(self):
        self.assertArrayIdentical(self.tempar[0], self.input[0])
        self.assertArrayIdentical(self.tempar[1], self.input[1])

    def test_toohighindex(self):
        self.assertRaises(IndexError, self.tempar.__getitem__, 2)

    def test_nonvalidindex(self):
        self.assertRaises(TypeError, self.tempar.__getitem__, 2.0)


    def test_iterarrays(self):
        ars = [a for a in self.tempar.iter_arrays()]
        self.assertArrayIdentical(ars[0], self.input[0])
        self.assertArrayIdentical(ars[1], self.input[1])



# FIXME not complete
class RaggedArrayAttrs(unittest.TestCase):

    def setUp(self):
        self.temparpath = Path(tempfile.mkdtemp()) / 'testra.ra'
        self.tempar = create_raggedarray(self.temparpath, atom=(),
                                         dtype='float64')
        self.tempar.iterappend([[1,2,3],[4,5,6,7]])

    def tearDown(self):
        delete_raggedarray(self.tempar)

    def test_narrays(self):
        self.assertEqual(self.tempar.narrays, 2)

    def test_mb(self):
        self.assertAlmostEqual(self.tempar.mb, 8.8e-05)

    def test_size(self):
        self.assertEqual(self.tempar.size, 7)

    def test_datadirexistence(self):
        self.assertEqual(self.temparpath, self.tempar.datadir.path)


class IterAppendRaggedArray(unittest.TestCase):

    def test_1darray(self):
        with tempdirfile() as filename:
            dal = create_raggedarray(filename, atom=(), dtype='float64',
                                     overwrite=True)
            dal.iterappend([[0., 1., 2.], [3., 4.], [5.]])
            self.assertEqual(len(dal), 3)


class ClassAsRaggedArray(unittest.TestCase):

    def test_1darray(self):
        with tempdirfile() as filename:
            na = [[1,2,3],[4,5,6]]
            md = {'fs': 20000, 'x': 33.3}
            dal = asraggedarray(filename, na, metadata=md)
            assert_array_equal(dal[0], na[0])
            assert_array_equal(dal[1], na[1])
            self.assertDictEqual(dict(dal.metadata), md)


class ClassCopyRaggedArray(unittest.TestCase):

    def test_simplecopy1d(self):
        with tempdirfile() as filename1:
            dal1 = create_raggedarray(filename1, atom=(), dtype='float64')
            a = np.array([0, 1, 2, 3], dtype='float64')
            dal1.append(a)
            with tempdirfile() as filename2:
                dal2 = dal1.copy(path=filename2)
                assert_array_equal(dal1[0], dal2[0])
                self.assertEqual(dal1.dtype, dal2.dtype)


class DeleteRaggedArray(unittest.TestCase):

    def test_simpledelete(self):
        with tempdirfile() as filename:
            dal = create_raggedarray(filename, atom=(2,))
            delete_raggedarray(dal)
            self.assertEqual(len(os.listdir(filename.parent)), 0)

    def test_invalidtarget(self):
         self.assertRaises(TypeError, delete_raggedarray, 1.)

    def test_notwriteable(self):
        with tempdirfile() as filename:
            dal = create_raggedarray(filename, atom=(2,), accessmode='r')
            self.assertRaises(OSError, delete_raggedarray, dal)

    def test_donotremovenondarrfiles(self):
        with tempdirfile() as filename:
            dal = create_raggedarray(filename, atom=(2,), accessmode='r+')
            dal._datadir._write_txt('test.txt', text='abc')
            self.assertRaises(OSError, delete_raggedarray, dal)

class RaggedArrayTruncate(DarrTestCase):

    def test_truncate1d(self):
        with tempdirfile() as filename:
            ra = asraggedarray(path=filename, arrayiterable=[[0,1],[2],[3,4]],
                               dtype='int64')
            self.assertEqual(len(ra), 3)
            truncate_raggedarray(ra, 2)
            self.assertEqual(len(ra),2)
            ra = RaggedArray(filename)
            self.assertEqual(len(ra),2)

    def test_truncatebydirname(self):
        with tempdirfile() as filename:
            ra = asraggedarray(path=filename, arrayiterable=[[0,1],[2],[3,4]],
                               dtype='int64')
            truncate_raggedarray(filename, 2)
            ra = RaggedArray(filename)
            self.assertEqual(len(ra), 2)

    def test_donottruncatenondarrdir(self):
        with tempdirfile() as filename:
            bd = create_datadir(filename)
            bd._write_jsondict('test.json', {'a': 1})
            self.assertRaises(TypeError, truncate_raggedarray, filename, 3)

    def test_truncateinvalidindextype(self):
        with tempdirfile() as filename:
            ra = asraggedarray(path=filename, arrayiterable=[[0,1],[2],[3,4]],
                               dtype='int64')
            self.assertRaises(TypeError, truncate_raggedarray, ra, 'a')

    def test_truncateindextoohigh(self):
        with tempdirfile() as filename:
            ra = asraggedarray(path=filename, arrayiterable=[[0,1],[2],[3,4]],
                               dtype='int64')
            self.assertRaises(IndexError, truncate_raggedarray, ra, 10)

    def test_truncatetolen0(self):
        with tempdirfile() as filename:
            ra = asraggedarray(path=filename, arrayiterable=[[0,1],[2],[3,4]],
                               dtype='int64')
            truncate_raggedarray(ra, 0)
            self.assertEqual(len(ra), 0)
            ra = RaggedArray(filename)
            self.assertEqual(len(ra), 0)


class TestReadCodeArray(DarrTestCase):


    # FIXME test more elaborately
    def test_readcodemethod(self):
        with tempdirfile() as filename:
            ra = asraggedarray(path=filename, arrayiterable=[[0,1],[2],[3,4]],
                               dtype='float64')
            self.assertIsInstance(ra.readcode('matlab'), str)

    def test_rcomplex64none(self):
        with tempdirfile() as filename:
            ra = asraggedarray(path=filename, arrayiterable=[[0,1],[2],[3,4]],
                               dtype='complex64')
            self.assertIsNone(readcode(ra, 'R'))

    def test_readcodeunsupportedlanguage(self):
        with tempdirfile() as filename:
            ra = asraggedarray(path=filename,
                               arrayiterable=[[0, 1], [2], [3, 4]],
                               dtype='float64')
            self.assertRaises(ValueError, readcode, ra, 'perl')

    def test_readcodelanguages(self):
        with tempdirfile() as filename:
            ra = asraggedarray(path=filename,
                               arrayiterable=[[0, 1], [2], [3, 4]],
                               dtype='float64')
            self.assertIsInstance(ra.readcodelanguages, tuple)
            self.assertIn('numpymemmap', ra.readcodelanguages)



# this is already tested with simple Arrays, so a brief check will suffice
class MetaData(unittest.TestCase):

    def test_createwithmetadata(self):
        with tempdirfile() as filename:
            md = {'fs': 20000, 'x': 33.3}
            dal = create_raggedarray(filename, atom=(), dtype='float64',
                                     metadata=md)
            self.assertDictEqual(dict(dal.metadata), md)

    def test_setmetadatawhenempty(self):
        with tempdirfile() as filename:
            md = {'fs': 20000, 'x': 33.3}
            dal = create_raggedarray(filename, atom=(), dtype='float64')
            dal.metadata.update(md)
            self.assertDictEqual(dict(dal.metadata), md)

    def test_setmetadatawhenpresent(self):
        with tempdirfile() as filename:
            md = {'fs': 20000, 'x': 33.3}
            dal = create_raggedarray(filename, atom=(), dtype='float64',
                                     metadata=md)
            md['fs'] = 3000
            dal.metadata.update(md)
            self.assertDictEqual(dict(dal.metadata), md)


if __name__ == '__main__':
    unittest.main()