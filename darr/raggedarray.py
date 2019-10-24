# EXPERIMENTAL! This code is still experimental, and is probably going to
# change

from pathlib import Path
from contextlib import contextmanager

import numpy as np
from ._version import get_versions

from .array import Array, MetaData, asarray, \
    check_accessmode, delete_array, create_array, \
    truncate_array
from .basedatadir import BaseDataDir, create_basedatadir
from .metadata import MetaData
from .readcoderaggedarray import readcode
from .utils import wrap

__all__ = ['RaggedArray', 'asraggedarray', 'create_raggedarray',
           'delete_raggedarray', 'truncate_raggedarray']

class RaggedArray(BaseDataDir):
    """
    Disk-based sequence of arrays that may have a variable length in maximally
    one dimension.

    """
    _valuesdirname = 'values'
    _indicesdirname = 'indices'
    _arraydescrfilename = 'arraydescription.json'
    _metadatafilename = 'metadata.json'
    _readmefilename = 'README.txt'
    _filenames = {_valuesdirname, _indicesdirname,
                  _readmefilename, _metadatafilename,
                  _arraydescrfilename} | BaseDataDir._filenames
    _formatversion = get_versions()['version']

    def __init__(self, path, accessmode='r'):
        BaseDataDir.__init__(self, path=path)
        self._accessmode = check_accessmode(accessmode)
        self._valuespath = self.path / self._valuesdirname
        self._indicespath = self.path / self._indicesdirname
        self._arraydescrpath = self._path / self._arraydescrfilename
        self._values = Array(self._valuespath, accessmode=self._accessmode)
        self._indices = Array(self._indicespath, accessmode=self._accessmode)
        self._metadata = MetaData(self._path / self._metadatafilename,
                                  accessmode=accessmode)
        arrayinfo = {}
        arrayinfo['len'] = len(self._indices)
        arrayinfo['size'] = self._values.size
        arrayinfo['atom'] = self._values.shape[1:]
        arrayinfo['numtype'] = self._values._arrayinfo['numtype']
        arrayinfo['darrversion'] = RaggedArray._formatversion
        arrayinfo['darrobject'] = 'RaggedArray'
        self._arrayinfo = arrayinfo

    @property
    def accessmode(self):
        """Data access mode of metadata, {'r', 'r+'}."""
        return self._accessmode

    @accessmode.setter
    def accessmode(self, value):
        self._accessmode = check_accessmode(value)
        self._metadata.accessmode = value
        self._values.accessmode = value
        self._indices.accessmode = value

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
        """Storage size in megabytes of the ragged array.

        """
        return self._values.mb + self._indices.mb

    @property
    def size(self):
        """Total number of values in the data array.

        """
        return int(self._values._size)

    def __getitem__(self, item):
        if not np.issubdtype(type(item), np.integer):
            raise TypeError("Only integers can be used for indexing " \
                            "darraylists, which '{}' is not".format(item))
        index = slice(*self._indices[item])
        return self._values[index]

    def __len__(self):
        return self._indices.shape[0]

    def _update_readmetxt(self):
        txt = readcodetxt(self)
        self._write_txt(self._readmefilename, txt)

    def _update_arraydescr(self, **kwargs):
        self._arrayinfo.update(kwargs)
        self._write_jsondict(filename=self._arraydescrfilename,
                           d=self._arrayinfo, overwrite=True)

    def _append(self, array):
        size = len(array)
        endindex = self._values.shape[0]
        self._values.append(np.asarray(array, dtype=self.dtype))
        self._indices.append([[endindex, endindex + size]])


    def append(self, array):
        self._append(array)
        self._update_readmetxt()
        self._update_arraydescr(len=len(self._indices),
                                size=self._values.size)

    def copy(self, path, accessmode='r', overwrite=False):
        arrayiterable = (self[i] for i in range(len(self)))
        metadata = dict(self.metadata)
        return asraggedarray(path=path, arrayiterable=arrayiterable,
                             dtype=self.dtype, metadata=metadata,
                             accessmode=accessmode, overwrite=overwrite)

    @contextmanager
    def _view(self, accessmode=None):
        with self._indices._open_array(accessmode=accessmode) as (iv, _), \
             self._values._open_array(accessmode=accessmode) as (vv, _):
            yield iv, vv

    def iter_arrays(self, startindex=0, endindex=None, stepsize=1,
                 accessmode=None):
        if endindex is None:
            endindex = self.narrays
        with self._view(accessmode=accessmode):
            for i in range(startindex, endindex, stepsize):
                yield np.array(self[i], copy=True)

    def iterappend(self, arrayiterable):
        """Iteratively append data from a data iterable.

        The iterable has to yield array-like objects compliant with darr.
        The length of first dimension of these objects may be different,
        but the length of other dimensions, if any, has to be the same.

        Parameters
        ----------
        arrayiterable: an iterable that yield array-like objects

        Returns
        -------
            None

        """
        # TODO refactor such that info files are not updated at each append?
        with self._view():
            for a in arrayiterable:
                self._append(a)
        self._update_readmetxt()
        self._update_arraydescr(len=len(self._indices),
                                size=self._values.size)


# FIXME empty arrayiterable
def asraggedarray(path, arrayiterable, dtype=None, metadata=None,
                  accessmode='r+', overwrite=False):
    path = Path(path)
    if not hasattr(arrayiterable, 'next'):
        arrayiterable = (a for a in arrayiterable)
    bd = create_basedatadir(path=path, overwrite=overwrite)
    firstarray = np.asarray(next(arrayiterable), dtype=dtype)
    dtype = firstarray.dtype
    valuespath = bd.path.joinpath(RaggedArray._valuesdirname)
    indicespath = bd.path.joinpath(RaggedArray._indicesdirname)
    valuesda = asarray(path=valuespath, array=firstarray, dtype=dtype,
                       accessmode='r+', overwrite=overwrite)
    firstindices = [[0, len(firstarray)]]
    indicesda = asarray(path=indicespath, array=firstindices,
                        dtype=np.int64, accessmode='r+',
                        overwrite=overwrite)
    valueslen = firstindices[0][1]
    indiceslen = 1
    with valuesda._open_array(accessmode='r+') as (_, vfd), \
         indicesda._open_array(accessmode='r+') as (_, ifd):
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
    datainfo = {}
    datainfo['len'] = len(indicesda)
    datainfo['size'] = valuesda.size
    datainfo['atom'] = valuesda.shape[1:]
    datainfo['numtype'] = valuesda._arrayinfo['numtype']
    datainfo['darrversion'] = Array._formatversion
    datainfo['darrobject'] = 'RaggedArray'
    bd._write_jsondict(filename=RaggedArray._arraydescrfilename,
                       d=datainfo, overwrite=overwrite)
    metadatapath = path.joinpath(Array._metadatafilename)
    if metadata is not None:
        bd._write_jsondict(filename=Array._metadatafilename,
                           d=metadata, overwrite=overwrite)
    elif metadatapath.exists():  # no metadata but file exists, remove it
        metadatapath.unlink()
    ra = RaggedArray(path=path, accessmode=accessmode)
    ra._update_readmetxt()
    return RaggedArray(path=path, accessmode=accessmode)


def create_raggedarray(path, atom=(), dtype='float64', metadata=None,
                       accessmode='r+', overwrite=False):
    if not hasattr(atom, '__len__'):
        raise TypeError(f'shape "{atom}" is not a sequence of dimensions.\n'
                        f'If you want just a list of 1-dimensional arrays, '
                        f'use "()"')
    shape = [0] + list(atom)
    ar = np.zeros(shape, dtype=dtype)
    ra = asraggedarray(path=path, arrayiterable=[ar], metadata=metadata,
                        accessmode=accessmode, overwrite=overwrite)
    # the current ragged array has one element, which is an empty array
    # but we want an empty ragged array => we should get rid of the indices
    create_array(path=ra._indicespath, shape=(0,2), dtype=np.int64,
                 overwrite=True)
    ra._update_arraydescr(len=0, size=0)
    return RaggedArray(ra.path, accessmode=accessmode)


readmetxt = wrap('Disk-based storage of a ragged array') + '\n' + \
            wrap('====================================') + '\n\n' + \
            wrap('This directory is a data store for a numeric ragged array, '
                 'which is a sequence of arrays in which one dimension varies '
                 'in length. On disk, these arrays are concatenated along '
                 'their variable dimension. The easiest way to access the '
                 'data is to use the Darr library '
                 '(https://pypi.org/project/darr/) in Python, as follows:') \
            + '\n\n' \
            + '>>> import darr\n' \
            + ">>> a = darr.RaggedArray('path_to_array_dir')\n\n" + \
            wrap("where 'path_to_array_dir' is the name of the array "
              "directory, which is the one that also contains this README.")\
               + "\n\n" + \
            wrap('If Darr is not available, the data can also be read in '\
                 'other environments, with more effort, using the '\
                 'description and example code below.') + '\n\n\n' \
            + 'Description of data storage\n' \
            + '---------------------------\n' + \
            wrap('There are two subdirectories, each containing an array '
                 'stored in a self-explanatory format. See the READMEs in '
                 'the corresponding directories to find out in detail out '
                 'how to read them. Example code is provided below '
                 'for a number of analysis environments, which in many cases '
                 'is sufficient.') + '\n\n' + \
            wrap('The subdirectory "values" holds the numerical data itself, '
                 'where subarrays are simply appended along their variable '
                 'length dimension (first axis). So the number of dimensions '
                 'of the values array is one less than that of the ragged '
                 'array. A particular subarray can be be retrieved using the '
                 'appropriate start and end index along the first axis of the '
                 'values array. These indices (counting from 0) are stored in '
                 'a different 2-dimensional array in the subdirectory '
                 '"indices". The first axis of the index array represents the '
                 'sequence number of the subarray and the second axis '
                 '(length 2) represents start and (non-inclusive) end '
                 'indices to be used on the values array. To read the n-th '
                 'subarray, read the nt-h start and end indices from the '
                 'indices array and use these to read the array data from '
                 'the values array.') + '\n\n\n'


def readcodetxt(ra):
    """Returns text on how to read a Darr ragged array numeric binary data in
    various programming languages.

    Parameters
    ----------
    ra: Darr raggedarray

    """

    s = readmetxt
    s += wrap(f'This ragged array has {len(ra)} subarrays. ') + '\n\n' + \
         wrap(f'Example code for reading the data') + '\n' + \
         wrap(f'=================================') + '\n\n'
    languages = (
        ("Python with Numpy (memmap):", "numpymemmap"),
        ("R:", "R"),
        ("Matlab:", "matlab")
    )
    for heading, language in languages:
        codetext = readcode(ra, language)
        if codetext is not None:
            s += f"{heading}\n{'-' * len(heading)}\n{codetext}\n"
    return s


def delete_raggedarray(ra):
    """
    Delete Darr ragged array data from disk.

    Parameters
    ----------
    path: path to data directory

    """
    try:
        if not isinstance(ra, RaggedArray):
            ra = RaggedArray(ra, accessmode='r+')
    except:
        raise TypeError(f"'{ra}' not recognized as a Darr ragged array")

    if not ra.accessmode == 'r+':
        raise OSError('Darr ragged array is read-only; set accessmode to '
                      '"r+" to change')
    for fn in ra._filenames:
        path = ra.path.joinpath(fn)
        if path.exists() and not path.is_dir():
            path.unlink()
    delete_array(ra._values)
    delete_array(ra._indices)
    try:
        ra._path.rmdir()
    except OSError as error:
        message = f"Error: could not fully delete Darr ragged array " \
                  f"directory " \
                  f"'{ra.path}'. It may contain additional files that are " \
                  f"not part of the darr. If so, these should be removed " \
                  f"manually."
        raise OSError(message) from error


def truncate_raggedarray(ra, index):
    """Truncate darr ragged array.

    Parameters
    ----------
    ra: array or str or pathlib.Path
       The darr object to be truncated or file system path to it.
    index: int
        The index along the first axis at which the darr ragged array should
        be truncated. Negative indices can be used but the resulting length of
        the truncated darr should be 0 or larger and smaller than the
        current length.

    """
    try:
        if not isinstance(ra, RaggedArray):
            ra = RaggedArray(ra, accessmode='r+')
    except Exception:
        raise TypeError(f"'{ra}' not recognized as a darr Ragged Array")
    # FIXME allow for numpy ints
    if not isinstance(index, int):
        raise TypeError(f"'index' should be an int (is {type(index)})")
    with ra._indices._open_array() as (mmap, _):
        newlen = len(mmap[:index])
    del mmap
    ra._values.check_arraywriteable()
    ra._indices.check_arraywriteable()
    if 0 <= newlen < len(ra):
        truncate_array(ra._indices, index=newlen)
        if newlen == 0:
            vi = 0
        else:
            vi = int(ra._indices[-1][-1])
        truncate_array(ra._values, index=vi)
        ra._update_readmetxt()
        ra._update_arraydescr(len=len(ra._indices), size=ra._values.size)
    else:
        raise IndexError(f"'index' {index} would yield a ragged array of "
                         f"length {newlen}, which is invalid (current length "
                         f"is {len(ra)})")


