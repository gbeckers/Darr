import unittest
from contextlib import contextmanager
from pathlib import Path
from darr.array import BaseDataDir
from .utils import tempdir

class TestArchiving(unittest.TestCase):

    @contextmanager
    def create_basedatadir(self):
        with tempdir() as dirname:
            bdddirname = Path(dirname) / 'data.bd'
            bdddirname.mkdir()
            bdd = BaseDataDir(bdddirname)
            bdd._write_jsondict('test.json', {'a': 1})
            yield bdd

    def test_archive(self):
        with self.create_basedatadir() as bdd:
            archivepath = bdd.archive()
            self.assertEqual(archivepath , Path(str(bdd.path) + '.tar.xz'))
            self.assertEqual(archivepath.exists(), True)

    def test_archiveoverwrite(self):
        with self.create_basedatadir() as bdd:
            archivepath = bdd.archive()
            self.assertEqual(archivepath.exists(), True)
            bdd.archive(overwrite=True)
            self.assertEqual(archivepath.exists(), True)
            self.assertRaises(OSError, bdd.archive, overwrite=False)

    def test_archivewrongcompressiontype(self):
        with self.create_basedatadir() as bdd:
            self.assertRaises(ValueError, bdd.archive, compressiontype='z7')
