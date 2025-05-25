import unittest
from contextlib import contextmanager
from pathlib import Path
from darr.datadir import DataDir, create_datadir
from darr.utils import filesha256, tempdir

@contextmanager
def create_testbasedatadir(filename='test.json', datadict=None):
    if datadict is None:
        datadict = {'a': 1}
    with tempdir() as dirname:
        bdddirname = Path(dirname) / 'data.bd'
        bdddirname.mkdir()
        bdd = DataDir(bdddirname)
        bdd._write_jsondict(filename, datadict)
        yield bdd


class TestCreateBaseDir(unittest.TestCase):

    def test_pathexistsnotoverwrite(self):
        with tempdir() as dirname:
            self.assertRaises(OSError, create_datadir, dirname)

    def test_pathexistsoverwrite(self):
        with tempdir() as dirname:
            create_datadir(dirname, overwrite=True)


class TestDataDir(unittest.TestCase):

    def test_nonexistingpath(self):
        with self.assertRaises(OSError):
            DataDir("lkjhlkihlkblhhhgdhg") # assume that doesn't exist

    def test_writejsondictcorrectinput(self):
        with tempdir() as dirname:
            bd = DataDir(dirname)
            bd.write_jsondict('test1.json', {'a': 1})

    def test_writejsondictincorrectinput(self):
        with tempdir() as dirname:
            bd = DataDir(dirname)
            with self.assertRaises(TypeError):
                bd.write_jsondict('test1.json', 3)
            with self.assertRaises(TypeError):
                bd.write_jsondict('test1.json', 'a')

    def test_updatejsondictcorrect(self):
        with tempdir() as dirname:
            bd = DataDir(dirname)
            bd.write_jsondict('test1.json', {'a': 1})
            bd.update_jsondict('test1.json', {'a': 2, 'b':3})

    def test_readjsondict(self):
        with tempdir() as dirname:
            bd = DataDir(dirname)
            wd = {'a': 1, 'b': [1,2,3], 'c': 'k'}
            bd.write_jsondict('test1.json', wd)
            rd = bd.read_jsondict('test1.json')
            self.assertDictEqual(wd, rd)

    def test_readjsondictrequiredkeypresent(self):
        with tempdir() as dirname:
            bd = DataDir(dirname)
            wd = {'a': 1, 'b': [1,2,3], 'c': 'k'}
            bd.write_jsondict('test1.json', wd)
            rd = bd.read_jsondict('test1.json', requiredkeys=('a', 'c'))
            self.assertDictEqual(wd, rd)

    def test_readjsondictrequiredkeynotpresent(self):
        with tempdir() as dirname:
            bd = DataDir(dirname)
            wd = {'a': 1, 'b': [1,2,3], 'c': 'k'}
            bd.write_jsondict('test1.json', wd)
            self.assertRaises(ValueError, bd.read_jsondict, 'test1.json',
                              requiredkeys=('a', 'd'))

    def test_readjsondictnotdict(self):
        with tempdir() as dirname:
            bd = DataDir(dirname)
            bd.write_jsonfile('test1.json', [1,2,3])
            self.assertRaises(TypeError, bd.read_jsondict, 'test1.json')

    def test_writetxt(self):
        with tempdir() as dirname:
            bd = DataDir(dirname)
            bd.write_txt('test1.txt', 'hello')
            self.assertEqual(bd.read_txt('test1.txt'), 'hello')

    def test_writetxtdonotoverwrite(self):
        with tempdir() as dirname:
            bd = DataDir(dirname)
            bd.write_txt('test1.txt', 'hello')
            self.assertRaises(OSError, bd._write_txt, 'test1.txt', 'hello')

    def test_writetxtoverwrite(self):
        with tempdir() as dirname:
            bd = DataDir(dirname)
            bd.write_txt('test1.txt', 'hello')
            bd.write_txt('test1.txt', 'hello', overwrite=True)

    def test_deletefiles(self):
        with tempdir() as dirname:
            bd = DataDir(dirname)
            bd.write_txt('test1.txt', 'hello')
            bd.write_txt('test2.txt', 'hello')
            bd.delete_files(('test1.txt', 'test2.txt', 'test3.txt'))

    def test_protectedfiles(self):
        with tempdir() as dirname:
            bd = DataDir(dirname, protectedpaths=('test.dat',))
            self.assertEqual(bd.protectedfiles, set(('test.dat',)))

    def test_deleteprotectedfile(self):
        with tempdir() as dirname:
            bd = DataDir(dirname, protectedpaths=('test.dat',))
            self.assertRaises(OSError, bd.delete_files, (('test.dat',)))


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
        with create_testbasedatadir(filename='test.json', datadict=datadict) \
                as bdd:
            checksums = bdd.sha256[str(bdd.path / filename)]
            self.assertEqual(checksums, filesha256(bdd.path / filename))

if __name__ == '__main__':
    unittest.main()