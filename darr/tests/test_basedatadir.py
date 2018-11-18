import unittest
from contextlib import contextmanager
from pathlib import Path
from darr.array import BaseDataDir
from .utils import tempdir

@contextmanager
def create_testbasedatadir(filename='test.json', datadict=None):
    if datadict is None:
        datadict = {'a': 1}
    with tempdir() as dirname:
        bdddirname = Path(dirname) / 'data.bd'
        bdddirname.mkdir()
        bdd = BaseDataDir(bdddirname)
        bdd._write_jsondict(filename, datadict)
        yield bdd

class TestArchiving(unittest.TestCase):

    def test_archive(self):
        with create_testbasedatadir() as bdd:
            archivepath = bdd.archive()
            self.assertEqual(archivepath , Path(str(bdd.path) + '.tar.xz'))
            self.assertEqual(archivepath.exists(), True)

    def test_archiveoverwrite(self):
        with create_testbasedatadir() as bdd:
            archivepath = bdd.archive()
            self.assertEqual(archivepath.exists(), True)
            bdd.archive(overwrite=True)
            self.assertEqual(archivepath.exists(), True)
            self.assertRaises(OSError, bdd.archive, overwrite=False)

    def test_archivewrongcompressiontype(self):
        with create_testbasedatadir() as bdd:
            self.assertRaises(ValueError, bdd.archive, compressiontype='z7')

    def test_sha256checksums(self):
        datadict = {'a': 1, 'b': "abcd"}
        filename = 'test.json'
        with create_testbasedatadir(datadict=datadict) as bdd:
            checksums = bdd.sha256
            self.assertEqual(checksums[str(bdd.path.joinpath(filename))],
                             '0f955a82d1055c6c71a21bd1953a0323aa5ce0b57067bae01c93a773fe913369')



