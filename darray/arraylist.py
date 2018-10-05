# EXPERIMENTAL! This code is still experimental, and is probably going to
# change

import numpy as np
from pathlib import Path
from .array import BaseDataDir, dArray, MetaData, asdarray, \
    create_basedir, check_accessmode, delete_darray

__all__ = ['dArrayList', 'asdarraylist', 'create_darraylist',
           'delete_darraylist']


class dArrayList(BaseDataDir):
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
        self._values = dArray(self._valuespath, accessmode=self._accessmode)
        self._indices = dArray(self._indicespath, accessmode=self._accessmode)
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
    def metadata(self):
        """
        Dictionary of meta data.

        """
        return self._metadata

    # FIXME should we just look up what os says?
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
        return asdarraylist(path=path, arrayiterable=arrayiterable,
                            dtype=self.dtype,
                            metadata=self.metadata, mode=mode)


# FIXME empty arrayiterable
def asdarraylist(path, arrayiterable, dtype=None, metadata=None,
                 accessmode='r+', overwrite=False):
    path = Path(path)
    if not hasattr(arrayiterable, 'next'):
        arrayiterable = (a for a in arrayiterable)
    bd = create_basedir(path=path, overwrite=overwrite)
    firstarray = np.asarray(next(arrayiterable), dtype=dtype)
    dtype = firstarray.dtype
    valuespath = bd.path.joinpath(dArrayList._valuesdirname)
    indicespath = bd.path.joinpath(dArrayList._indicesdirname)
    valuesda = asdarray(path=valuespath, array=firstarray, dtype=dtype,
                        accessmode='r+', overwrite=overwrite)
    firstindices = [[0, len(firstarray)]]
    indicesda = asdarray(path=indicespath, array=firstindices,
                         dtype=np.int64, accessmode='r+',
                         overwrite=overwrite)
    valueslen = firstindices[0][1]
    indiceslen = 1
    with valuesda.view(accessmode='r+'), indicesda.view(accessmode='r+'):
        for array in arrayiterable:
            lenincreasevalues = valuesda._append(array)
            lenincreaseindices = indicesda._append([[valueslen, valueslen + lenincreasevalues]])
            valueslen += lenincreasevalues
            indiceslen += lenincreaseindices
    valuesda._update_len(lenincrease=valueslen-firstindices[0][1])
    valuesda._update_readmetxt()
    indicesda._update_len(lenincrease=indiceslen-1)
    indicesda._update_readmetxt()

    metadatapath = path.joinpath(dArray._metadatafilename)
    if metadata is not None:
        bd._write_jsondict(filename=dArray._metadatafilename,
                           d=metadata, overwrite=overwrite)
    elif metadatapath.exists():  # no metadata but file exists, remove it
        metadatapath.unlink()
    bd._write_txt(dArrayList._readmefilename, readmetxt)
    return dArrayList(path=path, accessmode=accessmode)


def create_darraylist(path, shape, dtype, metadata=None,
                      accessmode='r+', overwrite=False):
    if not hasattr(shape, '__len__'):
        raise TypeError(f'shape "{shape}" is not a sequence of dimensions.\n'
                        f'If you want just a 1-dimesional appendable array, '
                        f'use (0,)"')
    ar = np.zeros(shape, dtype=dtype)
    dal = asdarraylist(path=path, arrayiterable=[ar], metadata=metadata,
                       accessmode=accessmode, overwrite=overwrite)
    # the current diskarraylist has one element, which is an empty array
    # but we want an empty diskarraylist => we should get rid of the indices
    indices = asdarray(path=dal._indicespath, array=np.zeros((0, 2)),
                       dtype=np.int64, accessmode='r+', overwrite=True)
    return dArrayList(dal.path)







readmetxt = """Disk array list data storage
============================

This directory and subdirectories contain a list of numeric data arrays, stored
 in a simple format that maximizes portability and archivability.


"""


def delete_darraylist(dal):
    """
    Delete DiskArrayList data from disk.

    Parameters
    ----------
    path: path to data directory

    """
    try:
        if not isinstance(dal, dArrayList):
            dal = dArrayList(dal)
    except:
        raise TypeError(f"'{dal}' not recognized as a DiskArrayList")

    for fn in dal._filenames:
        path = dal.path.joinpath(fn)
        if path.exists():
            path.unlink()
    delete_darray(dal._values)
    delete_darray(dal._indices)
    try:
        dal._path.rmdir()
    except OSError:
        print(f"Error: could not fully delete diskarraylist directory "
              f"'{dal.path}'. It may contain additional files that are not "
              f"part of the diskarraylist. If so, these should be removed "
              f"manually.")
        raise