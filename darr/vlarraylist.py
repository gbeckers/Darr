# EXPERIMENTAL! This code is still experimental, and is probably going to
# change

from pathlib import Path

import numpy as np

from .array import BaseDataDir, Array, MetaData, asarray, \
    create_basedir, check_accessmode, delete_array

__all__ = ['VLArrayList', 'asvlarraylist', 'create_vlarraylist',
           'delete_vlarraylist']

class VLArrayList(BaseDataDir):
    """
    Disk-based list of variable-length arrays.

    """
    _valuesdirname = 'values'
    _indicesdirname = 'indices'
    _version = '0.1.0'
    _metadatafilename = 'metadata.json'
    _readmefilename = 'README.txt'
    _filenames = {_valuesdirname, _indicesdirname,
                  _readmefilename, _metadatafilename} | BaseDataDir._filenames
    _formatversion = "0.1.0"
    def __init__(self, path, accessmode='r'):
        BaseDataDir.__init__(self, path=path)
        self._accessmode = check_accessmode(accessmode)
        self._valuespath = self.path.joinpath(self._valuesdirname)
        self._indicespath = self.path.joinpath(self._indicesdirname)
        self._values = Array(self._valuespath, accessmode=self._accessmode)
        self._indices = Array(self._indicespath, accessmode=self._accessmode)
        self._metadata = MetaData(self._path.joinpath(self._metadatafilename),
                                  accessmode=accessmode)

    @property
    def accessmode(self):
        """File access mode of the disk array data. `r` means read-only, `r+`
        means read-write. `w` does not exist. To create new diskarrays,
        potentially overwriting an other one, use the `asdiskarray` or
        `create_diskarray` functions.

       """
        return self._accessmode

    @property
    def dtype(self):
        """Numpy data type of the array values.

        """
        return self._values._dtype

    @property
    def atom(self):
        """Dimensions of the non-variable axes of the arrays.

        """
        return tuple(self._values._shape[1:])

    @property
    def narrays(self):
        """Numpy data type of the array values.

        """
        return self._indices.shape[0]

    @property
    def metadata(self):
        """
        Dictionary of meta data.

        """
        return self._metadata

    @property
    def mb(self):
        """Size in megabytes of the data array.

        """
        return self._values._mb #+ self._indices._mb

    @property
    def size(self):
        """Total number of values in the data array.

        """
        return self._values._size


    def __getitem__(self, item):
        if not np.issubdtype(type(item), np.integer):
            raise TypeError("Only integers can be used for indexing " \
                            "darraylists, which '{}' is not".format(item))
        index = slice(*self._indices[item])
        return self._values[index]

    def __len__(self):
        return self._indices.shape[0]

    def append(self, array):
        size = len(array)
        endindex = self._values.shape[0]
        self._values.append(np.asarray(array, dtype=self.dtype))
        self._indices.append([[endindex, endindex + size]])

    def copy(self, path, mode='r'):
        arrayiterable = (self[i] for i in range(len(self)))
        return asvlarraylist(path=path, arrayiterable=arrayiterable,
                             dtype=self.dtype,
                             metadata=self.metadata, mode=mode)


# FIXME empty arrayiterable
def asvlarraylist(path, arrayiterable, dtype=None, metadata=None,
                  accessmode='r+', overwrite=False):
    path = Path(path)
    if not hasattr(arrayiterable, 'next'):
        arrayiterable = (a for a in arrayiterable)
    bd = create_basedir(path=path, overwrite=overwrite)
    firstarray = np.asarray(next(arrayiterable), dtype=dtype)
    dtype = firstarray.dtype
    valuespath = bd.path.joinpath(VLArrayList._valuesdirname)
    indicespath = bd.path.joinpath(VLArrayList._indicesdirname)
    valuesda = asarray(path=valuespath, array=firstarray, dtype=dtype,
                       accessmode='r+', overwrite=overwrite)
    firstindices = [[0, len(firstarray)]]
    indicesda = asarray(path=indicespath, array=firstindices,
                        dtype=np.int64, accessmode='r+',
                        overwrite=overwrite)
    valueslen = firstindices[0][1]
    indiceslen = 1
    with valuesda._open_array(accessmode='r+') as (vv, vfd), \
         indicesda._open_array(accessmode='r+') as (iv, ifd):
        for array in arrayiterable:
            lenincreasevalues = valuesda._append(array, fd=vfd)
            starti, endi = valueslen, valueslen + lenincreasevalues
            lenincreaseindices = indicesda._append([[starti, endi]], fd=ifd)
            valueslen += lenincreasevalues
            indiceslen += lenincreaseindices
    valuesda._update_len(lenincrease=valueslen-firstindices[0][1])
    valuesda._update_readmetxt()
    indicesda._update_len(lenincrease=indiceslen-1)
    indicesda._update_readmetxt()

    metadatapath = path.joinpath(Array._metadatafilename)
    if metadata is not None:
        bd._write_jsondict(filename=Array._metadatafilename,
                           d=metadata, overwrite=overwrite)
    elif metadatapath.exists():  # no metadata but file exists, remove it
        metadatapath.unlink()
    bd._write_txt(VLArrayList._readmefilename, readmetxt)
    return VLArrayList(path=path, accessmode=accessmode)


def create_vlarraylist(path, atom=(), dtype='float64', metadata=None,
                       accessmode='r+', overwrite=False):
    if not hasattr(atom, '__len__'):
        raise TypeError(f'shape "{atom}" is not a sequence of dimensions.\n'
                        f'If you want just a list of 1-dimensional arrays, '
                        f'use "()"')
    shape = [0] + list(atom)
    ar = np.zeros(shape, dtype=dtype)
    dal = asvlarraylist(path=path, arrayiterable=[ar], metadata=metadata,
                        accessmode=accessmode, overwrite=overwrite)
    # the current diskarraylist has one element, which is an empty array
    # but we want an empty diskarraylist => we should get rid of the indices
    indices = asarray(path=dal._indicespath, array=np.zeros((0, 2)),
                      dtype=np.int64, accessmode='r+', overwrite=True)
    return VLArrayList(dal.path, accessmode=accessmode)






# FIXME this should be a lot clearer
readmetxt = """Disk-based storage of variable-length arrays
               ============================================

This directory is a data store for a list of variable length arrays. There 
are two subdirectories, each containing an array stored in a simple format 
that should be easy to read. To do so, see the READMEs in these directories.

The subdirectory 'values' holds the actual numerical data, where arrays are 
simply appended along their variable length dimension (first axis).

The subdirectory 'indices' holds 2D array data that represent the first 
axis start and end indices (counting from 0) to read corresponding arrays 
in the list.

So to read the n-th array in the list, read the nt-h start and end indices 
from the indices array ('starti, endi = indices[n]') and use these to read the 
array data from the values array (array = values[starti:endi]).


"""


def delete_vlarraylist(dal):
    """
    Delete DiskArrayList data from disk.

    Parameters
    ----------
    path: path to data directory

    """
    try:
        if not isinstance(dal, VLArrayList):
            dal = VLArrayList(dal)
    except:
        raise TypeError(f"'{dal}' not recognized as a DiskArrayList")

    for fn in dal._filenames:
        path = dal.path.joinpath(fn)
        if path.exists() and not path.is_dir():
            path.unlink()
    delete_array(dal._values)
    delete_array(dal._indices)
    try:
        dal._path.rmdir()
    except OSError as error:
        message = f"Error: could not fully delete Darr array list directory " \
                  f"'{da.path}'. It may contain additional files that are " \
                  f"not part of the darr. If so, these should be removed " \
                  f"manually."
        raise OSError(message) from error