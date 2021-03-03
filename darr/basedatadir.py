# REMOVE this module in 1.0 version of Darr

import warnings
from .datadir import DataDir, create_datadir

class BaseDataDir(DataDir):

    def __init__(self, path, filenames=None):
        warnings.warn("The use of `BaseDataDir` is deprecated in "
                      "versions of Darr > 2.2. Use `DataDir`, and its "
                      "associated function `create_datadir` instead.",
                      FutureWarning)
        DataDir.__init__(self, path=path, protectedfiles=filenames)


create_basedatadir = create_datadir