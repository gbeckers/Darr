from pathlib import Path
from contextlib import contextmanager

import numpy as np
from ._version import get_versions

from .array import Array, asarray, check_accessmode, delete_array, \
    create_array, truncate_array
from .datadir import DataDir, create_datadir
from .metadata import MetaData
from .readcoderaggedarray import readcode, readcodefunc, \
    shapeindexexplanationtextraggedarray
from .utils import wrap

__all__ = ['RaggedArray', 'asraggedarray', 'create_raggedarray',
           'delete_raggedarray', 'truncate_raggedarray']

# TODO needs doc
# TODO an open_array method
class RaggedArray:
    """
    Disk-based sequence of arrays that may have a variable length in maximally
    one dimension.

    """
    _valuesdirname = 'values'
    _indicesdirname = 'indices'
    _arraydescrfilename = 'arraydescription.json'
    _metadatafilename = 'metadata.json'
    _readmefilename = 'README.txt'
    _protectedfiles = {_valuesdirname, _indicesdirname,
                       _readmefilename, _metadatafilename,
                       _arraydescrfilename}
    _formatversion = get_versions()['version']

    def __init__(self, path, accessmode='r'):

        self._datadir = DataDir(path=path,
                                protectedpaths=self._protectedfiles)
        self._path = self._datadir._path
        self._accessmode = check_accessmode(accessmode)
        self._valuespath = self._path / self._valuesdirname
        self._indicespath = self._path / self._indicesdirname
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
    def datadir(self):
        """Data directory object with many useful methods, such as
        writing information to text or json files, archiving all data,
        calculating checksums etc."""
        return self._datadir

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
    def path(self):
        """File system path to array data"""
        return self._path

    @property
    def size(self):
        """Total number of values in the data array."""
        return int(self._values._size)

    @property
    def readcodelanguages(self):
        """Tuple of the languages that the `readcode` method can produce
                reading code for. Code in these languages is also included in the
                README.txt file that is stored as part of the array ."""
        languages = []
        for lang in readcodefunc.keys():
            if readcode(self, lang) is not None:
                languages.append(lang)
        return tuple(sorted(languages))

    def __getitem__(self, item):
        if not np.issubdtype(type(item), np.integer):
            raise TypeError("Only integers can be used for indexing " \
                            "RaggedArrays, which '{}' is not".format(item))
        index = slice(*self._indices[item])
        return self._values[index]

    def __len__(self):
        return self._indices.shape[0]

    def __repr__(self):
        return f'RaggedArray ({self.narrays} subarrays with atom shape '\
               f'{self.atom}, {self.accessmode})'

    __str__ = __repr__

    def _update_readmetxt(self):
        txt = readcodetxt(self)
        self._datadir._write_txt(self._readmefilename, txt, overwrite=True)

    def _update_arraydescr(self, **kwargs):
        self._arrayinfo.update(kwargs)
        self._datadir._write_jsondict(filename=self._arraydescrfilename,
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

    def readcode(self, language, abspath=False, basepath=None):
        """Generate code to read the array in a different language.

        Note that this does not include reading the metadata, which is just
        based on a text file in JSON format.

        Parameters
        ----------
        language: str
            One of the languages that are supported. Choose from:
            'matlab', 'numpymemmap', 'R'.
        abspath: bool
            Should the paths to the data files be absolute or not? Default:
            True.
        basepath: str or pathlib.Path or None
            Path relative to which the binary array data file should be
            provided. Default: None.

        Example
        -------
        >>> import darr
        >>> a = darr.asraggedarray('test.darr', [[1],[2,3],[4,5,6],[7,8,9,10]], overwrite=True)
        >>> print(a.readcode('matlab'))
        fileid = fopen('indices/arrayvalues.bin');
        i = fread(fileid, [2, 4], '*int64', 'ieee-le');
        fclose(fileid);
        fileid = fopen('values/arrayvalues.bin');
        v = fread(fileid, 10, '*int32', 'ieee-le');
        fclose(fileid);
        % example to read third subarray
        startindex = i(1,3) + 1;  % matlab starts counting from 1
        endindex = i(2,3);  % matlab has inclusive end index
        a = v(startindex:endindex);

        """
        if language not in readcodefunc.keys():
            raise ValueError(f'Language "{language}" not supported, choose '
                             f'from {readcodefunc.keys()}')
        return readcode(self, language, basepath=basepath, abspath=abspath)

    def archive(self, filepath=None, compressiontype='xz', overwrite=False):
        """Archive array data into a single compressed file.

        Parameters
        ----------
        filepath: str
            Name of the archive. In None, it will be derived from the data's
            path name.
        compressiontype: str
            One of 'xz', 'gz', or 'bz2', corresponding to the gzip, bz2 and
            lzma compression algorithms supported by the Python standard
            library.
        overwrite: (True, False), optional
            Overwrites existing archive if it exists. Default is False.

        Returns
        -------
        pathlib.Path
            The path of the created archive

        Notes
        -----
        See the `tarfile library`_ for more info on archiving formats

        .. _tarfile library:
           https://docs.python.org/3/library/tarfile.html

        """
        return self._datadir.archive(filepath=filepath,
                                     compressiontype=compressiontype,
                                     overwrite=overwrite)


# FIXME empty arrayiterable
# TODO describe int32 vs int64 index
def asraggedarray(path, arrayiterable, dtype=None, metadata=None,
                  accessmode='r+', indextype='int64', overwrite=False):
    path = Path(path)
    supportedindextypes = ('int8','uint8', 'int16', 'uint16', 'int32',
                           'uint32', 'int64')
    if not indextype in supportedindextypes:
        raise ValueError(f'`indextype` {indextype} not one of '
                         f'{supportedindextypes}')
    if not hasattr(arrayiterable, 'next'):
        arrayiterable = (a for a in arrayiterable)
    bd = create_datadir(path=path, overwrite=overwrite)
    firstarray = np.asarray(next(arrayiterable), dtype=dtype)
    dtype = firstarray.dtype
    valuespath = bd.path.joinpath(RaggedArray._valuesdirname)
    indicespath = bd.path.joinpath(RaggedArray._indicesdirname)
    valuesda = asarray(path=valuespath, array=firstarray, dtype=dtype,
                       accessmode='r+', overwrite=overwrite)
    firstindices = [[0, len(firstarray)]]
    indicesda = asarray(path=indicespath, array=firstindices,
                        dtype=indextype, accessmode='r+',
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
                       accessmode='r+', indextype='int64', overwrite=False):
    if not hasattr(atom, '__len__'):
        raise TypeError(f'shape "{atom}" is not a sequence of dimensions.\n'
                        f'If you want just a list of 1-dimensional arrays, '
                        f'use "()"')
    shape = [0] + list(atom)
    ar = np.zeros(shape, dtype=dtype)
    ra = asraggedarray(path=path, arrayiterable=[ar], metadata=metadata,
                       accessmode=accessmode, indextype=indextype,
                       overwrite=overwrite)
    # the current ragged array has one element, which is an empty array
    # but we want an empty ragged array => we should get rid of the indices
    create_array(path=ra._indicespath, shape=(0,2), dtype=np.int64,
                 overwrite=True)
    ra._update_arraydescr(len=0, size=0)
    return RaggedArray(ra.path, accessmode=accessmode)

# TODO, simplify explanation if subarrays are 1-dimensional
# TODO add readcode for more languages
def readmetxt(ra):
    n = len(ra)
    ndsa  = len(ra.atom)
    txt = wrap(f'This directory stores a numeric ragged array (also '
               f'called a jagged array), which is a sequence of '
               f'subarrays that may be multidimensional and that '
               f'can vary in the length of their first dimension.') + ' \n\n'
    txt += wrap(f'The ragged array can be read using the NumPy-based Python '
                f'library Darr (https://pypi.org/project/darr/), which was '
                f'used to create the data. If that is not available, you can '
                f'use the code snippets below to read the data in a number of '
                f'other environments. If code for your environment is not '
                f'provided, use the description of how the data can be read '
                f'in the next section.') + '\n\n'
    txt += 'Description of ragged array\n' \
           '===========================\n\n'
    txt += wrap(f'This ragged array is a sequence of {n} '
                f'subarrays, each of which is {ndsa + 1}-dimensional and '
                f'can vary in the length of its first dimension. The array '
                f'consists of {ra.dtype.name} numbers.') \
                + ' \n\n'
    dimtxt = f'The dimensions of the '
    if len(ra) > 5:
        dimtxt += f'first five '
    if len(ra) > 6:
        dimtxt += f'and last '
    dimtxt = wrap(f'{dimtxt}subarrays is (subarray index: dimensions):') + '\n\n'
    txt += dimtxt + dimensionstxt(ra, firstnmax=5) + '\n\n'
    itxt = f'These index numbers are based on Python ' \
           f'indexing, which starts at 0.'
    if len(ra.atom) >0:
        itxt = f'{itxt} Dimensions are based on row-major memory layout. When ' \
               f'using the code provided below to read subarrays, dimensions ' \
               f'will be inversed in column-major languages (see Note below).'
    txt += wrap(itxt) + '\n\n'
    txt += 'Description of storage on disk\n' \
           '==============================\n\n'
    txt += wrap('There are two subdirectories, "values" and "indices", each '
                'containing an array stored in a self-explanatory format. '
                'You first need to read these two arrays using '
                'the information in the README.txt files in their '
                'subdirectories. "values" holds the ragged array, where '
                'subarrays are simply concatenated along their variable '
                'length dimension (first axis). The n-th subarray can be '
                'retrieved from the values array by using the appropriate '
                'start and end index on the first axis of the values '
                'array. These indices are stored in the two-dimensional '
                'array in "indices". The first axis of the index array '
                'corresponds to the sequence numbers of the subarrays, while '
                'the length-2 second axis holds the start and end indices to '
                'be used on the values array to retrieve a subarray. To '
                'read the n-th subarray, read the nt-h start and end indices '
                'from the indices array and use these to read the array data '
                'from the values array. Note that the indices start counting '
                'from zero, and end indices are non-inclusive.') + '\n\n\n'
    return txt


def dimensionstxt(ra, firstnmax=5):
    end = min(len(ra), firstnmax)
    lengths = np.diff(ra._indices[:end], axis=-1).flatten()
    if len(ra.atom) > 0:
        astr = str(ra.atom)[1:-1] + ')'
    else:
        astr = ')'
    lines = []
    for i, l in enumerate(lengths):
        lines.append(f'    {i}: ({l}, {astr}')
    if len(ra) > (firstnmax + 1):
        lines.append('    ...')
    if len(ra) > firstnmax:
        lastdiff = np.diff(ra._indices[-1], axis=-1)[0]
        lines.append(f'    {len(ra)-1}: ({lastdiff}, {astr}')
    return '\n'.join(lines)


def readcodetxt(ra):
    """Returns text on how to read a Darr ragged array numeric binary data in
    various programming languages.

    Parameters
    ----------
    ra: Darr raggedarray

    """

    s = readmetxt(ra)
    s += wrap(f'Example code for reading the data') + '\n' + \
         wrap(f'=================================') + '\n\n'
    languages = (
        ("Python with Darr:", "darr"),
        ("Python with Numpy (memmap):", "numpymemmap"),
        ("R:", "R"),
        ("IDL/GDL", "idl"),
        ("Julia (version >= 1.0):", "julia"),
        ("Maple:", "maple"),
        ("Matlab/Octave:", "matlab"),
        ("Mathematica:", "mathematica")
    )
    for heading, language in languages:
        codetext = readcode(ra, language)
        if codetext is not None:
            s += f"{heading}\n{'-' * len(heading)}\n{codetext}\n"
    return f'{s}\n{shapeindexexplanationtextraggedarray}'


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
    for fn in ra._protectedfiles:
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


