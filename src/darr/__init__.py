from typing import Union
import warnings
from .array import *
from .raggedarray import *
from .datadir import DataDir, create_datadir


def open(path: str, accessmode: str = 'r') -> Union[Array, RaggedArray]:
    """Open disk-based Darr array data for access.

    Instantiates the appropriate Darr object (Array or RaggedArray, detected
    automatically from the stored array description) through which the
    disk-based data can be read and, depending on `accessmode`, written using
    numpy indexing. No data is loaded into memory.

    Parameters
    ----------
    path: Path to the array directory
    accessmode: File access mode ('r' for read-only, 'r+' for read/write)

    Returns
    -------
    Array or RaggedArray object, based on the array type

    Raises
    ------
    ValueError: If array type is not supported

    """
    dd = DataDir(path)
    arraytype = dd.read_jsondict('arraydescription.json')['darrobject']
    if arraytype == 'Array':
        return Array(path=path, accessmode=accessmode)
    elif arraytype == 'RaggedArray':
        return RaggedArray(path=path, accessmode=accessmode)
    else:
        raise ValueError(f"'{arraytype}' not supported in this version of "
                         f"Darr")

# Alias for open() function, deprecated
def link(path: str, accessmode: str = 'r') -> Union[Array, RaggedArray]:
    warnings.warn("The use of `link` is deprecated in "
                  "versions of Darr >= 0.6. Use the `open` function instead.",
                  FutureWarning)
    return open(
        path=path,
        accessmode=accessmode,
    )
