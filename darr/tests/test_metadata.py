import tempfile
import shutil
import unittest

from .test_array import DarrTestCase, create_array

class MetaData(DarrTestCase):

    def setUp(self):
        self.temparpath = tempfile.mkdtemp() # even array
        self.metadata = md = {'fs':20000, 'x': 33.3}
        self.tempar = create_array(path=self.temparpath, shape=(12,),
                                    dtype='int64', metadata=md,
                                   accessmode='r+', overwrite=True)
    def tearDown(self):
        shutil.rmtree(str(self.temparpath))


    def test_createwithmetadata(self):
        self.assertDictEqual(dict(self.tempar.metadata), self.metadata)

    def test_getmetadata(self):
        self.assertEqual(self.tempar.metadata.get('fs'), 20000)

    def test_metadatavalues(self):
        self.assertEqual(set(self.tempar.metadata.values()), {20000,33.3})


    def test_changemetadata(self):
        self.tempar.metadata['fs'] = 40000
        self.assertDictEqual(dict(self.tempar.metadata), {'fs': 40000, 'x': 33.3})
        self.tempar.metadata.update({'x': 34.4})
        self.assertDictEqual(dict(self.tempar.metadata), {'fs': 40000, 'x': 34.4})

    def test_popmetadata(self):
        self.tempar.metadata.pop('x')
        self.assertDictEqual(dict(self.tempar.metadata), {'fs': 20000})
        self.tempar.metadata.pop('fs')
        self.assertDictEqual(dict(self.tempar.metadata), {})

    def test_popitmemetadata(self):
        k, _ = self.tempar.metadata.popitem()
        keys = self.tempar.metadata.keys()
        self.assertNotIn(k, keys)
        self.tempar.metadata.popitem()
        self.assertEqual(self.tempar._metadata.path.exists(), False)

    def test_metadataaccessmodereadwrite(self):
        self.assertEqual(self.tempar.metadata.accessmode, 'r+')
        self.tempar.metadata['x'] = 22.2

    def test_metadataaccessmodereadonly(self):
        self.tempar.accessmode = 'r'
        self.assertEqual(self.tempar.metadata.accessmode, 'r')
        self.assertRaises(OSError, self.tempar.metadata.popitem)
        self.assertRaises(OSError, self.tempar.metadata.pop)
        self.assertRaises(OSError, self.tempar.metadata.update, {'a': 3})

    def test_setaccessmode(self):
        self.assertEqual(self.tempar.metadata.accessmode, 'r+')
        self.tempar.metadata.accessmode = 'r'
        self.assertEqual(self.tempar.metadata.accessmode, 'r')
        self.assertRaises(ValueError, setattr, self.tempar.metadata,
                          'accessmode', 'w')
        self.assertRaises(ValueError, setattr, self.tempar.metadata,
                          'accessmode', 'a')

    def test_delitem(self):
        del self.tempar.metadata['x']
        self.assertDictEqual(dict(self.tempar.metadata), {'fs': 20000})

    def test_metadatarepr(self):
        self.assertEqual(repr(self.tempar.metadata),
                         "{'fs': 20000, 'x': 33.3}")

    def test_metadatalen(self):
        l = len(self.tempar.metadata)
        self.assertEqual(l, 2)

    def test_metadataitems(self):
        self.assertTupleEqual((('fs', 20000), ('x', 33.3)),
                              tuple(self.tempar.metadata.items()))

if __name__ == '__main__':
    unittest.main()