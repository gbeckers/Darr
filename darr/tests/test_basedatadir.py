import unittest
from pathlib import Path
from darr.array import BaseDataDir
from .utils import tempdir

class TestArchiving(unittest.TestCase):

    def test_archive(self):
        with tempdir() as dirname:
            bdddirname = Path(dirname)/'data.bd'
            bdddirname.mkdir()
            bdd = BaseDataDir(bdddirname)
            bdd._write_jsondict('test.json', {'a':1})
            bdd.archive()
            archivepath = Path(str(bdddirname) + '.tar.xz')
            self.assertEqual(archivepath.exists(), True)