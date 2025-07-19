from typing import Union
import warnings
from .array import *
from .raggedarray import *
from .datadir import DataDir, create_datadir


def link(path: str, accessmode: str = 'r') -> Union[Array, RaggedArray]:
    """Instantiate a Darr object linked to disk based array data.

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

# Alias for link() function, deprecated
def open(path: str, accessmode: str = 'r') -> Union[Array, RaggedArray]:
    warnings.warn("The use of `open` is deprecated in "
                  "versions of Darr >= 1.0 Use the `link`function instead.",
                  FutureWarning)
    return link(
        path=path,
        accessmode=accessmode,
    )
