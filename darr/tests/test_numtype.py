import unittest
from darr.numtype import arrayinfotodtype

corrinfo = {'arrayorder': 'C',
            'byteorder': 'little',
            'darrobject': 'Array',
            'darrversion': '0.1.11',
            'numtype': 'float64',
            'shape': (2, 4)}

class ArrayInfoDtype(unittest.TestCase):

    def test_correct(self):
        self.assertEqual(arrayinfotodtype(corrinfo), '<f8')

    def test_validnumptype(self):
        for numtype in ('int8', 'int16', 'int32', 'int64', 'uint8', 'uint16',
                         'uint32', 'uint64', 'float16', 'float32', 'float64',
                         'complex64', 'complex128'):
            info = corrinfo.copy()
            info['numtype'] = numtype
            self.assertIsInstance(arrayinfotodtype(info), str)

    def test_invalidnumtype(self):
        info = corrinfo.copy()
        info['numtype'] = 'int9'
        self.assertRaises(ValueError, arrayinfotodtype, info)


    def test_invalidbyteorder(self):
        info = corrinfo.copy()
        info['byteorder'] = 'middle'
        self.assertRaises(ValueError, arrayinfotodtype, info)

if __name__ == '__main__':
    unittest.main()