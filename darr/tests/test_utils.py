import unittest
import json
import numpy as np
from darr.utils import fit_frames, write_jsonfile, product
from darr.utils import tempdir, tempdirfile


class Product(unittest.TestCase):

    def multiply_list(self):
        self.assertEqual(product([1,2,3,4]), 24)

    def multiply_tuple(self):
        self.assertEqual(product([1, 2, 3, 4]), 24)

    def multiply_array(self):
        self.assertEqual(product(np.array([1,2,3,4])), 24)

    def overflow32bitints(self):
        self.assertEqual(product((np.iinfo(np.int32).max, 2)), 4294967294)


class WriteJsonFile(unittest.TestCase):

    def test_pathexistsdonotoverwrite(self):
        with tempdir() as dirname:
            filepath = dirname / "test"
            open(filepath, 'w').close()
            self.assertRaises(OSError, write_jsonfile, path=filepath,
                              data={'a': 1})

    def test_wrongtype(self):
        with tempdirfile() as filename:
            self.assertRaises(TypeError, write_jsonfile, path=filename,
                              data=unittest, overwrite=True)

    def test_acceptnumpyobjects(self):
        with tempdirfile() as filename:
            d1 = {'a': np.int8(1),
                  'b': np.int16(1),
                  'c': np.int32(1),
                  'd': np.int64(1),
                  'e': np.float16(1),
                  'f': np.float32(1),
                  'g': np.float64(1),
                  'h': np.array([1,2], np.int32),
                  'i': np.array([1, 2], np.int64),
                  'j': np.array([1, 2], np.float32),
                  'k': np.array([1, 2], np.float64),
                  }
            write_jsonfile(path=filename, data=d1, overwrite=True)
            with open(filename, 'r') as fp:
                d2 = json.load(fp)
                for k in 'abcd':
                    self.assertEqual(d2[k], 1)
                for k in 'efg':
                    self.assertEqual(d2[k], 1.0)
                for k in 'hi':
                    self.assertEqual(d2[k], [1, 2])
                for k in 'jk':
                    self.assertEqual(d2[k], [1., 2.])




class FitChunks(unittest.TestCase):

    def test_fitremainder_defaultsteplen(self):
        # results = (nchunks, newsize, remainder)
        # even chunklen
        results = fit_frames(totallen=6, chunklen=2, steplen=None)
        self.assertTupleEqual(results, (3, 6, 0))
        results = fit_frames(totallen=7, chunklen=2, steplen=None)
        self.assertTupleEqual(results, (3, 6, 1))
        results = fit_frames(totallen=8, chunklen=2, steplen=None)
        self.assertTupleEqual(results, (4, 8, 0))
        # unevenchunklen
        results = fit_frames(totallen=6, chunklen=3, steplen=None)
        self.assertTupleEqual(results, (2, 6, 0))
        results = fit_frames(totallen=7, chunklen=3, steplen=None)
        self.assertTupleEqual(results, (2, 6, 1))
        results = fit_frames(totallen=8, chunklen=3, steplen=None)
        self.assertTupleEqual(results, (2, 6, 2))
        results = fit_frames(totallen=9, chunklen=3, steplen=None)
        self.assertTupleEqual(results, (3, 9, 0))

    def test_fitremainder_steplen1(self):
        # results = (nchunks, newsize, remainder)
        results = fit_frames(totallen=6, chunklen=3, steplen=1)
        self.assertTupleEqual(results, (4, 6, 0))
        results = fit_frames(totallen=7, chunklen=3, steplen=1)
        self.assertTupleEqual(results, (5, 7, 0))

    def test_strangebutallowedtotallen(self):
        # totallen = 0
        results = fit_frames(totallen=0, chunklen=3, steplen=None)
        self.assertTupleEqual(results, (0, 0, 0))
        # int-castable floats as input
        results = fit_frames(totallen=6., chunklen=2., steplen=None)
        self.assertTupleEqual(results, (3, 6, 0))

    def test_invalidtotallen(self):
        self.assertRaises(ValueError, fit_frames, totallen=-1, chunklen=3)
        self.assertRaises(ValueError, fit_frames, totallen=-1., chunklen=3)
        self.assertRaises(ValueError, fit_frames, totallen=0.5, chunklen=3)

    def test_invalidchunklen(self):
        self.assertRaises(ValueError, fit_frames, totallen=3, chunklen=0)
        self.assertRaises(ValueError, fit_frames, totallen=3, chunklen=0.)
        self.assertRaises(ValueError, fit_frames, totallen=3, chunklen=0.5)
        self.assertRaises(ValueError, fit_frames, totallen=3, chunklen=-1)
        self.assertRaises(ValueError, fit_frames, totallen=3, chunklen=-1.)

    def test_invalidsteplen(self):
        self.assertRaises(ValueError, fit_frames, totallen=3, chunklen=2,
                          steplen=0)
        self.assertRaises(ValueError, fit_frames, totallen=3, chunklen=2,
                          steplen=0.)
        self.assertRaises(ValueError, fit_frames, totallen=3, chunklen=2,
                          steplen=0.5)
        self.assertRaises(ValueError, fit_frames, totallen=3, chunklen=2,
                          steplen=-1)
        self.assertRaises(ValueError, fit_frames, totallen=3, chunklen=2,
                          steplen=-1.)

if __name__ == '__main__':
    unittest.main()