import unittest
from darr.utils import fit_frames, write_jsonfile
from .utils import tempdir, tempdirfile

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