# EXPERIMENTAL! This code is still experimental, and is probably going to
# change

from pathlib import Path
from contextlib import contextmanager

import numpy as np
from ._version import get_versions

from .array import BaseDataDir, Array, MetaData, asarray, \
    create_basedir, check_accessmode, delete_array, create_array
from .readcoderaggedarray import readcode
from .utils import wrap

__all__ = ['RaggedArray', 'asraggedarray', 'create_raggedarray',
           'delete_raggedarray']

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
        return self._values._mb + self._indices._mb

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
        with self._indices.view(accessmode=accessmode) as iv,\
             self._values.view(accessmode=accessmode) as vv:
            yield iv, vv

    def iter_arrays(self, startindex=0, endindex=None, stepsize=1,
                 accessmode=None):
        if endindex is None:
            endindex = self.narrays
        with self._view(accessmode=accessmode):
            for i in range(startindex, endindex, stepsize):
                yield self[i]

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
    bd = create_basedir(path=path, overwrite=overwrite)
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
            wrap('This directory is a data store for a numeric ragged array. '
                 'This is a sequence of subarrays that all have the same '
                 'shape except for one dimension. On disk, these subarrays '
                 'are concatenated along their variable dimension. The data '
                 'can be read in Python using the Darr library, but if that '
                 'is not available, they can also be read in other '
                 'environments with a little more effort.') + '\n\n' + \
            wrap('There are two subdirectories, each containing an array '
                 'stored in a self-explanatory format. See the READMEs in '
                 'the corresponding directories to find out in detail out '
                 'how. However, example code is provided below for a number '
                 'of analysis environments, which in many cases is '
                 'suffcient.') + '\n\n' + \
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
                 'the values array.') + '\n\n'


def readcodetxt(dra):
    """Returns text on how to read a Darr ragged array numeric binary data in
    various programming languages.

    Parameters
    ----------
    dra: Darr raggedarray

    """

    s = readmetxt
    s += wrap(f'This ragged array has {len(dra)} subarrays. ') + '\n\n' + \
         wrap(f'Example code for reading the data') + '\n' + \
         wrap(f'=================================') + '\n\n'
    languages = (
        ("Python with Numpy (memmap):", "numpymemmap"),
        ("R:", "R"),
        ("Matlab:", "matlab")
    )
    for heading, language in languages:
        codetext = readcode(dra, language)
        if codetext is not None:
            s += f"{heading}\n{'-' * len(heading)}\n{codetext}\n"
    return s


def delete_raggedarray(rar):
    """
    Delete Darr ragged array data from disk.

    Parameters
    ----------
    path: path to data directory

    """
    try:
        if not isinstance(rar, RaggedArray):
            rar = RaggedArray(rar)
    except:
        raise TypeError(f"'{rar}' not recognized as a Darr array list")

    if not rar.accessmode == 'r+':
        raise OSError('Darr ragged arrays is read-only; set accessmode to '
                      '"r+" to change')
    for fn in rar._filenames:
        path = rar.path.joinpath(fn)
        if path.exists() and not path.is_dir():
            path.unlink()
    delete_array(rar._values)
    delete_array(rar._indices)
    try:
        rar._path.rmdir()
    except OSError as error:
        message = f"Error: could not fully delete Darr array list directory " \
                  f"'{rar.path}'. It may contain additional files that are " \
                  f"not part of the darr. If so, these should be removed " \
                  f"manually."
        raise OSError(message) from error