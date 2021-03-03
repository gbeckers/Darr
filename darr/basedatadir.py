# REMOVE this module in 1.0 version of Darr

import warnings
from .datadir import DataDir, create_datadir

def warn():
    warnings.warn("The use of `BaseDataDir` is deprecated in "
                  "versions of Darr > 2.2. Use `DataDir`, and its "
                  "associated function `create_datadir` instead.",
                  FutureWarning)

class BaseDataDir(DataDir):

    def __init__(self, path, filenames=None):
        warn()
        DataDir.__init__(self, path=path, protectedpaths=filenames)


def create_basedatadir(path, overwrite=False):
    warn()
    return create_datadir(path=path, overwrite=overwrite)