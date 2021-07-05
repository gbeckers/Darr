# This is for backward compatibility, module should disappear.

import unittest
from darr.basedatadir import BaseDataDir, create_basedatadir
from darr.utils import tempdir


class TestCreateBaseDataDir(unittest.TestCase):

    def test_futurewarningdeprecation(self):
        with tempdir() as dirname:
            self.assertWarns(FutureWarning, create_basedatadir, dirname, True)


class TestBaseDataDir(unittest.TestCase):
    def test_futurewarningdeprecation(self):
        self.assertWarns(FutureWarning, BaseDataDir, '')

