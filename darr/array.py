"""Darr is a Python library for storing numeric data arrays in a format that
is as open and simple as possible. It also provides easy memory-mapped
access to such disk-based data using numpy indexing.

Darr objects can be created from array-like objects, such as numpy arrays
and lists, using the **asarray** function. Alternatively, darr arrays can be
created from scratch by the **create_array** function. Existing Darr data on
disk can be accessed through the **Array** constructor. To remove a Darr
array from disk, use **delete_array**.

"""

import distutils.version
import hashlib
import json
import os
import sys
import warnings
from contextlib import contextmanager
from pathlib import Path

import numpy as np



# Design considerations
# ---------------------
# - All text is written in UTF-8. This is compatible with ASCII, widely used
#   and capable of encoding all 1,112,064 valid code points in Unicode

__all__ = ['Array', 'asarray', 'create_array', 'delete_array',
           'truncate_array']

# mathematica: https://reference.wolfram.com/language/ref/BinaryRead.html
# Octave: https://octave.org/doc/v4.2.0/Binary-I_002fO.html
# Matlab: https://mathworks.com/help/matlab/ref/fread.html
# R: https://www.rdocumentation.org/packages/base/versions/3.4.3/topics/readBin
# Julia: https://docs.julialang.org/en/release-0.4/manual/integers-and-
#        floating-point-numbers/

numtypes = {
    'int8': {'descr': '8-bit signed integer (-128 to 127)',
             'numpy': 'i1',
             'matlab': 'int8',
             'R': {'what': 'integer()', 'size': 1, 'signed': 'TRUE'},
             'julia': 'Int8',
             'idl': None,
             'mathematica': "Integer8"},
    'int16': {'descr': '16‐bit signed integer (-32768 to 32767)',
              'numpy': 'i2',
              'matlab': 'int16',
              'R': {'what': 'integer()', 'size': 2, 'signed': 'TRUE'},
              'julia': 'Int16',
              'idl': 2,
              'mathematica': "Integer16"},
    'int32': {'descr': '32‐bit signed integer (-2147483648 to 2147483647)',
              'numpy': 'i4',
              'matlab': 'int32',
              'R': {'what': 'integer()', 'size': 4, 'signed': 'TRUE'},
              'julia': 'Int32',
              'idl': 3,
              'mathematica': "Integer32"},
    'int64': {'descr': '64‐bit signed integer (-9223372036854775808 to '
                       '9223372036854775807)',
              'numpy': 'i8',
              'matlab': 'int64',
              'R': {'what': 'integer()', 'size': 8, 'signed': 'TRUE'},
              'julia': 'Int64',
              'idl': 14,
              'mathematica': "Integer64"},
    'uint8': {'descr': '8‐bit unsigned integer (0 to 255)',
              'numpy': 'u1',
              'matlab': 'uint8',
              'R': {'what': 'integer()', 'size': 1, 'signed': 'FALSE'},
              'julia': 'UInt8',
              'idl': 1,
              'mathematica': "UnsignedInteger8"},
    'uint16': {'descr': '16‐bit unsigned integer (0 to 65535)',
               'numpy': 'u2',
               'matlab': 'uint16',
               'R': {'what': 'integer()', 'size': 2, 'signed': 'FALSE'},
               'julia': 'UInt16',
               'idl': 12,
               'mathematica': "UnsignedInteger16"},
    'uint32': {'descr': '32‐bit unsigned integer (0 to 4294967295)',
               'numpy': 'u4',
               'matlab': 'uint32',
               'R': {'what': 'integer()', 'size': 4, 'signed': 'FALSE'},
               'julia': 'UInt32',
               'idl': 13,
               'mathematica': "UnsignedInteger32"},
    'uint64': {'descr': '64‐bit unsigned integer (0 to 18446744073709551615)',
               'numpy': 'u8',
               'matlab': 'uint64',
               'R': {'what': 'integer()', 'size': 8, 'signed': 'FALSE'},
               'julia': 'UInt64',
               'idl': 15,
               'mathematica': "UnsignedInteger64"},
    'float16': {'descr': '16-bit half precision float (sign bit, 5 bits '
                         'exponent, 10 bits mantissa)',
                'numpy': 'f2',
                'matlab': None,
                'R': {'what': 'numeric()', 'size': 2, 'signed': 'TRUE'},
                'julia': 'Float16',
                'idl': None,
                'mathematica': None},
    'float32': {'descr': '32-bit IEEE single precision float (sign bit, '
                         '8 bits exponent, 23 bits mantissa)',
                'numpy': 'f4',
                'matlab': 'float32',
                'R': {'what': 'numeric()', 'size': 4, 'signed': 'TRUE'},
                'julia': 'Float32',
                'idl': 4,
                'mathematica': "Real32"},
    'float64': {'descr': '64-bit IEEE double precision float (sign bit, '
                         '11 bits exponent, 52 bits mantissa)',
                'numpy': 'f8',
                'matlab': 'float64',
                'R': {'what': 'numeric()', 'size': 8, 'signed': 'TRUE'},
                'julia': 'Float64',
                'idl': 5,
                'mathematica': "Real64"},
    'complex64': {'descr': '64-bit IEEE single‐precision complex number, '
                           'represented by two 32 - bit floats (real and '
                           'imaginary components)',
                  'numpy': 'c8',
                  'matlab': None,
                  'R': None,
                  'julia': 'Complex{Float32}',
                  'idl': 6,
                  'mathematica': "Complex64"},
    'complex128': {'descr': '128-bit IEEE double‐precision complex number, '
                            'represented by two 64 - bit floats (real and '
                            'imaginary components)',
                   'numpy': 'c16',
                   'matlab': None,
                   'R': {'what': 'complex()', 'size': 16, 'signed': 'TRUE'},
                   'julia': 'Complex{Float64}',
                   'idl': 9,
                   'mathematica': "Complex128"}
}

endiannesstypes = {
    'big':    {'descr': 'most-significant byte first',
               'matlab': 'ieee-be',
               'R': 'big',
               'julia': 'ntoh',
               'idl': 'big',
               'mathematica': '+1',
               'numpy': 'big',
               'numpymemmap': 'big'},
    'little': {'descr': 'least-significant byte first',
               'matlab': 'ieee-le',
               'R': 'little',
               'julia': 'ltoh',
               'idl': 'little',
               'mathematica': '-1',
               'numpy': 'little',
               'numpymemmap': 'little'}
}

class AppendDataError(Exception):
    pass

class BaseDataDir(object):
    """Use a directory for managing data of a subclass. Has methods for reading
    and writing json data, and text data. Upon initialization it expects and
    reads a json file names "dataclass.json", containing the name and version
    number of the (sub)class that uses the BaseDataDir.

    This class should normally not be used by end users. It is intended to be
    subclassed for disk-based data objects.

    Parameters
    ----------
    path: str or pathlib.Path
    
    """
    _filenames = set()

    def __init__(self, path):
        path = Path(path)
        if not path.exists():
            raise OSError(f"'{path}' does not exist")
        self._path = path

    @property
    def path(self):
        return self._path

    def _read_jsonfile(self, filename):
        path = self._path.joinpath(filename)
        with open(path, 'r') as fp:
            return json.load(fp)

    def _write_jsonfile(self, filename, data, sort_keys=True, indent=4,
                        overwrite=False):
        path = self._path.joinpath(filename)
        write_jsonfile(path, data=data, sort_keys=sort_keys, indent=indent,
                       ensure_ascii=True, overwrite=overwrite)

    def _read_jsondict(self, filename, requiredkeys=None):
        d = self._read_jsonfile(filename=filename)
        if not isinstance(d, dict):
            raise TypeError('json data must be a dictionary')
        if requiredkeys is not None:
            keys = set(d.keys())
            requiredkeys = set(requiredkeys)
            if not requiredkeys.issubset(keys):
                difference = requiredkeys.difference(keys)
                raise ValueError(f"required keys {difference} not present")
        return d

    def _write_jsondict(self, filename, d, overwrite=False):
        if not isinstance(d, dict):
            raise TypeError('json data must be a dictionary')
        return self._write_jsonfile(filename=filename, data=d,
                                    overwrite=overwrite)

    def _update_jsondict(self, filename, *args, **kwargs):
        d2 = self._read_jsondict(filename)
        d2.update(*args, **kwargs)
        self._write_jsondict(filename=filename, d=d2, overwrite=True)
        return d2

    def _write_txt(self, filename, text):
        # utf-8 is ascii-compatible
        with open(self._path.joinpath(filename), 'w', encoding='utf-8') as f:
            f.write(text)
            f.flush()

    def _md5(self, filename, blocksize=2 ** 20):
        """Compute the checksum of a file."""
        m = hashlib.md5()
        with open(self._path.joinpath(filename), 'rb') as f:
            while True:
                buf = f.read(blocksize)
                if not buf:
                    break
                m.update(buf)
        return m.hexdigest()


class MetaData:
    """Dictionary-like access to disk based metadata.

    If there is no metadata, the metadata file does not exist, rather than
    being empty. This saves a block of disk space (potentially 4kb).

    """

    def __init__(self, path, accessmode='r'):

        path = Path(path)
        self._path = path
        self._accessmode = check_accessmode(accessmode)

    @property
    def path(self):
        return self._path

    @property
    def accessmode(self):
        """File access mode of the darr data. `r` means read-only, `r+`
        means read-write. `w` does not exist. To create new darrays,
        potentially overwriting an other one, use the `asdarray` or
        `create_darray` functions.

       """
        return self._accessmode

    def __getitem__(self, item):
        return self._read()[item]

    def __setitem__(self, key, value):
        self.update({key: value})

    def __delitem__(self, key):
        self.pop(key)

    def __len__(self):
        return len(self.keys())

    def __repr__(self):
        return str(self._read())

    __str__ = __repr__

    def _read(self):
        if not self._path.exists():
            return {}
        with open(self._path, 'r') as fp:
            return json.load(fp)

    def get(self, *args):
        """metadata.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None.

        """
        return self._read().get(*args)

    def items(self):
        """a set-like object providing a view on D's items"""
        return self._read().items()

    def keys(self):
        """D.keys() -> a set-like object providing a view on D's keys"""
        return self._read().keys()

    def pop(self, *args):
        """D.pop(k[,d]) -> v, remove specified key and return the corresponding
        value. If key is not found, d is returned if given, otherwise KeyError
        is raised
        """
        metadata = self._read()
        val = metadata.pop(*args)
        if metadata:
            write_jsonfile(self.path, data=metadata, sort_keys=True,
                           ensure_ascii=True, overwrite=True)
        else:
            self._path.unlink()
        return val

    def popitem(self):
        """D.pop() -> k, v, returns and removes an arbitrary element (key,
        value) pair from the dictionary.
        """
        metadata = self._read()
        key, val = metadata.popitem()
        if metadata:
            write_jsonfile(self.path, data=metadata, sort_keys=True,
                           ensure_ascii=True, overwrite=True)
        else:
            self._path.unlink()
        return key, val

    def values(self):
        return self._read().values()

    def update(self, *arg, **kwargs):
        """Updates metadata.

        Metadata are written to disk.

        Parameters
        ----------
        arg: a dictionary with metadata keys and values, optional
        kwargs: keyword arguments, corresponding to keys and values, optional

        Returns
        -------
        None

        Examples
        --------
        >>> import darr as da
        >>> d = da.create_array('test.da', shape=(12,), accesmode= 'r+')
        >>> d.metadata.update({'starttime': '2017-08-31T17:00:00'})
        >>> print(d.metadata)
        {'starttime': '2017-08-31T17:00:00'}
        >>> d.metadata['samplingrate'] = 22050)
        >>> print(d.metadata)
        {'samplingrate': 22050, 'starttime': '2017-08-31T17:00:00'}

        """
        if self._accessmode == 'r':
            raise OSError("metadata not writeable; use 'set_accessmode' "
                          "method to change this")
        metadata = self._read()
        metadata.update(*arg, **kwargs)

        write_jsonfile(self.path, data=metadata, sort_keys=True,
                       ensure_ascii=True, overwrite=True)

    def set_accessmode(self, accessmode):
        """
        Set data access mode of data.

        Parameters
        ----------
        accessmode: {'r', 'r+'}, default 'r'
            File access mode of the data. `r` means read-only, `r+`
            means read-write.

        """
        self._accessmode = check_accessmode(accessmode)


class Array(BaseDataDir):
    """Read and write numeric data from and to a memory-mapped, disk-based
    array using numpy indexing. Memory-mapped arrays are used for accessing
    segments of (very) large files on disk, without reading the entire file
    into memory.

    Darr data is stored in a simple format that maximizes long-term
    readability by other software and programming languages, and has been
    designed with scientific use cases in mind.

    A darr array corresponds to a directory containing 1) a binary file with
    the raw numeric array values, 2) a text file (json format) describing the
    numeric type, array shape, and other format information, 3) a README text
    file documenting the data format, including examples of how to read the
    data in Python or Matlab.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to disk-based array directory.
    accessmode : {'r', 'r+'}, default 'r'
       File access mode of the darr data. `r` means read-only, `r+` means
       read-write. `w` does not exist. To create new darr arrays, potentially
       overwriting an other one, use the `asarray` or `create_array`
       functions.

    """
    _datafilename = 'arrayvalues.bin'
    _arraydescrfilename = 'arraydescription.json'
    _checksumsfilename = 'md5checksums.json'
    _metadatafilename = 'metadata.json'
    _readmefilename = 'README.txt'
    _filenames = {_arraydescrfilename, _datafilename,
                  _readmefilename, _checksumsfilename,
                  _metadatafilename} | BaseDataDir._filenames
    _formatversion = "0.1.0"

    def __init__(self, path, accessmode='r'):
        BaseDataDir.__init__(self, path=path)
        self._datapath = self._path.joinpath(self._datafilename)
        self._accessmode = check_accessmode(accessmode)
        self._arraydescrpath = self._path.joinpath(self._arraydescrfilename)
        self._arraydescr = self._read_arraydescr()
        self._memmap = None
        self._valuesfd = None
        with self._open_array() as (ar, fd):
            self._dtype = ar.dtype
            self._shape = ar.shape
            self._size = ar.size
            self._mb = ar.size * ar.dtype.itemsize / 1e6
        self._check_consistency()
        self._metadata = MetaData(self._path.joinpath(self._metadatafilename),
                                  accessmode=accessmode)

    @property
    def accessmode(self):
        """File access mode of the disk array data. `r` means read-only, `r+`
        means read-write. `w` does not exist. To create new darr arrays,
        potentially overwriting an other one, use the `asarray` or
        `create_array` functions.

       """
        return self._accessmode

    @property
    def dtype(self):
        """Numpy data type of the array values.

        """
        return self._dtype

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
        return self._mb

    @property
    def ndim(self):
        """Number of dimensions.

        """
        return len(self._shape)

    @property
    def shape(self):
        """Tuple with sizes of each axis of the data array.

        """
        return self._shape

    @property
    def size(self):
        """Total number of values in the data array.

        """
        return self._size

    @property
    def currentchecksums(self):
        """Current md5 checksums of data and datadescription files.

        """
        return self._currentchecksums()

    @property
    def storedmd5checksums(self):
        """Previously stored md5 checksums of data and datadescription files.

        """
        return self._storedmd5checksums()

    def __getitem__(self, index):
        with self._open_array() as (ar, fd):
            values = np.array(ar[index], copy=True)
        return values

    def __setitem__(self, index, value):
        with self._open_array() as (ar, fd):
            self.check_arraywriteable()
            ar[index] = value

    def __len__(self):
        return self._shape[0]

    def __repr__(self):
        with self._open_array() as (ar, fd):
            # next needed because class name may be longer than "memmap"
            s = '\n   '.join(repr(ar).lstrip('memmap').splitlines())
        return f"darr array {s} ({self.accessmode})"

    def __str__(self):
        with self._open_array() as (ar, fd):
            s = str(ar)
        return s

    @contextmanager
    def _open_array(self, accessmode=None):

        if accessmode is None:
            accessmode = self._accessmode
        # need different mode strings for file and memmap; memmap does not
        # take 'b', whereas file should have it.
        memmapmode = check_accessmode(accessmode, validmodes=('r', 'r+'),
                                      makebinary=False)
        filemode = check_accessmode(accessmode, validmodes=('r', 'r+'),
                                    makebinary=True)
        if self._memmap is not None:
            yield self._memmap, self._valuesfd
        else:
            try:
                # we must do it like this instead of providing a filename
                # to np.mmemap, otherwise accessing temporary dirs on 
                # windows will fail
                with open(file=self._datapath, mode=filemode) as fd:
                    self._valuesfd = fd
                    ad = self._arraydescr
                    dtypedescr = arraydescrtodtype(ad)
                    if np.product(ad['shape']) == 0: # empty file/array
                        self._memmap = np.zeros(ad['shape'], dtype=dtypedescr,
                                                order=ad['arrayorder'])
                    else:
                        self._memmap = np.memmap(filename=fd,
                                                 mode=memmapmode,
                                                 shape=ad['shape'],
                                                 dtype=dtypedescr,
                                                 order=ad['arrayorder'])
                    yield self._memmap, self._valuesfd
            except Exception:
                raise
            finally:
                #self._memmap._mmap.close() # may need this for Windows
                self._memmap = None
                self._valuesfd = None



    @contextmanager
    def view(self, accessmode=None):
        """Open a memory-mapped view of the array data.

        Although read and write operations can be performed conveniently using
        indexing notation on the Darr object, this can be relatively slow
        when performing multiple access operations in a row. To read data, the
        disk file needs to be opened, data copied into memory, and after which
        the file is closed. I such cases, it is much faster to use a *view* of
        the disk-based data. Whenever possible, indexing operations on this
        view return new views on the data, not copies. These views are lost
        when the context closes.

        Parameters
        ----------
        accessmode: {'r', 'r+'}, default 'r'
            File access mode of the disk array data. `r` means read-only, `r+`
            means read-write.

        Yields
        -------
        ndarray
            view of disk-based array

        Examples
        --------
        >>> import darr as da
        >>> d = da.create_array('test.da', shape=(1000,3), overwrite=True)
        >>> with d.view(accessmode='r+') as v:
                s1 = v[:10,1:].sum()
                s2 = v[20:25,:2].sum()
                v[500:] = 3.33

        """

        with self._open_array(accessmode=accessmode) as (memmap, fp):
            yield memmap

    def _read_arraydescr(self):
        requiredkeys = {'numtype', 'shape', 'arrayorder', 'darrversion'}
        try:
            d = self._read_jsondict(filename=self._arraydescrfilename,
                                    requiredkeys=requiredkeys)
        except Exception:
            raise OSError(f"Could not read array description from "
                          f"'{self._arraydescrfilename}'")
        vfile = distutils.version.StrictVersion(d['darrversion'])
        vlib = distutils.version.StrictVersion(self._formatversion)
        if not vlib >= vfile:
            raise ValueError(f"Format version of file ({d['darrversion']}) "
                             f"is too new. The installed Darr "
                             f"library only handles up to version "
                             f"{self._formatversion}; please update")
        try:
            d['shape'] = tuple(d['shape'])  # json does not have tuples
        except TypeError:
            ValueError(f"'{d['shape']}' is not a valid array shape")
        d['dtypedescr'] = arraydescrtodtype(d)
        if d['arrayorder'] not in {'C', 'F'}:
            raise ValueError(
                f"'{d['arrayorder']}' is not a valid numpy arrayorder")
        return d

    def _check_consistency(self):
        if not (self._read_arraydescr() == self._arraydescr):
            raise ValueError("in-memory and on-disk array descriptions not "
                             "the same")
        filesize = self._datapath.stat().st_size
        expectedfilesize = (self._size * self._dtype.itemsize)
        if filesize != expectedfilesize:
            raise ValueError(
                f"file size ({filesize}) is different from expected file "
                f"size ({expectedfilesize})")
        if self._size != np.product(self._shape):
            raise ValueError('array size and shape not congruent')

    def check_arraywriteable(self):
        with self._open_array() as (ar, fd):
            if not ar.flags.writeable:
                raise OSError(
                    "darr not writeable; use 'set_accessmode' method to "
                    "change this")

    def _update_len(self, lenincrease):
        newshape = list(self.shape)
        newshape[0] += lenincrease
        self._shape = tuple(newshape)
        self._size = np.product(self._shape)
        self._mb = self._size * self._dtype.itemsize / 1e6
        self._arraydescr.update(shape=self._shape)
        self._write_jsondict(filename=self._arraydescrfilename,
                             d=self._arraydescr, overwrite=True)
        self._update_readmetxt()

    def _update_readmetxt(self):
        txt = arrayreadmetxt(self)
        self._write_txt(self._readmefilename, txt)

    def append(self, array):
        """ Add array-like objects to darr to the end of the dataset.

        Data will be appended along the first axis. The shape of the data and
        the darr must be compliant. When appending data repeatedly it is
        more efficient to use `iterappend`.


        Parameters
        ----------
        array: array-like object
            This can be a numpy array, a sequence that can be converted into a
            numpy array.

        Returns
        -------
        None

        Examples
        --------
        >>> import darr as da
        >>> d = da.create_array('test.da', shape=(4,2), overwrite=True)
        >>> d.append([[1,2],[3,4],[5,6]])
        >>> print(d)
        [[ 0.  0.]
         [ 0.  0.]
         [ 0.  0.]
         [ 0.  0.]
         [ 1.  2.]
         [ 3.  4.]
         [ 5.  6.]]

        """
        self.iterappend([array])

    def _checkarrayforappend(self, array):
        """Private function to format input arrays correctly for append.

        """
        if hasattr(array, '__len__'):
            array = np.asarray(array, dtype=self._dtype)
        else:
            array = np.array(array, dtype=self._dtype, ndmin=1)
        if not array.shape[1:] == self.shape[1:]:
            raise TypeError(
                f"array shape {array.shape} not compatible with darr "
                f"shape {self.shape}")
        return array

    def _append(self, array, fd):
        """
        Private method to append data. Does *not* update attributes, json
        array info file, or readme file.

        """
        array = self._checkarrayforappend(array)
        fd.seek(0, 2)  # move to end
        array.tofile(fd)
        fd.flush()
        return array.shape[0]




    def iterappend(self, arrayiterable):
        """Iteratively append data from a data iterable.

        The iterable has to yield chunks of data that are array-like objects
        compliant with the darr.

        Parameters
        ----------
        arrayiterable: an iterable that yield array-like objects

        Returns
        -------
        None

        Examples
        --------
        >>> import darr as da
        >>> d = da.create_array('test.da', shape=(3,2), overwrite=True)
        >>> def ga():
                yield [[1,2],[3,4]]
                yield [[5,6],[7,8],[9,10]]
        >>> d.iterappend(ga())
        >>> print(d)
        [[  0.   0.]
         [  0.   0.]
         [  0.   0.]
         [  1.   2.]
         [  3.   4.]
         [  5.   6.]
         [  7.   8.]
         [  9.  10.]]

        """
        if self._accessmode != 'r+':
            raise OSError(f"Accesmode should be 'r+' "
                          f"(now is '{self._accessmode}')")
        if not hasattr(arrayiterable, '__iter__'):
            raise TypeError("'arrayiterable' is not iterable")
        self.check_arraywriteable()
        arrayiterable = iter(arrayiterable)
        if np.product(self._shape) == 0:
            # numpy cannot write to a fd of an empty file.
            # Hence we overwrite the file. It is not beautiful but it works.
            array = self._checkarrayforappend(next(arrayiterable))
            array.tofile(str(self._datapath))
            self._update_len(lenincrease=array.shape[0])
        with self._open_array() as (v, fd):
            oldshape = v.shape
            lenincrease = 0
            try:
                for i, array in enumerate(arrayiterable):
                    lenincrease += self._append(array=array, fd=fd)
            except Exception as exception:
                if fd.closed:
                    fd = open(file=self._datapath, mode=self._accessmode)
                fd.flush()
                self._update_len(lenincrease=lenincrease)
                fd.truncate(self._size * self._dtype.itemsize)
                fd.close()
                s = f"{exception}\nAppending of data did not (completely) " \
                    f"succeed. Shape of array was {oldshape} and is now " \
                    f"{self._shape} after an increase in length " \
                    f"(along first dimension) of {lenincrease}."
                raise AppendDataError(s)
        self._update_len(lenincrease=lenincrease)

    def iterview(self, chunklen, stepsize=None, startindex=None,
                 endindex=None, include_remainder=True, accessmode=None):
        """View the data array of the darr iteratively in chunks of a
        given length and with a given stepsize.

        This method does not copy the underlying data to a new numpy array,
        and is therefore relatively fast. It can also be used to change the
        darr.

        Parameters
        ----------

        chunklen: int
            Size of chunk for across the first axis. Note that the last chunk
            may be smaller than `chunklen`, depending on the size of the
            first axis.
        stepsize: <int, None>
            Size of the shift per iteration across the first axis.
            Default is None, which means that `stepsize` equals `chunklen`.
        include_remainder: <bool, True>
            Determines whether remainder (< chunklen) should be included.
        startindex: <int, None>
            Start index value.
            Default is None, which means to start at the beginning.
        endindex: <int, None>
            End index value.
            Default is None, which means to end at the end.
        include_remainder: <True, False>
            Determines if the remainder at the end of the array, if it exist,
            should be yielded or not. The remainder is smaller than `chunklen`.
            Default is True.
        accessmode:  {'r', 'r+'}, default 'r'
            File access mode of the darr data. `r` means read-only, `r+`
            means read-write.

        Returns
        -------
        generator
            a generator that produces numpy array chunks.

        Examples
        --------
        >>> import darr as da
        >>> d = da.create_array('test.da', shape=(12,), accesmode= 'r+')
        >>> for i,ar in enumerate(d.iterview(chunklen=2, stepsize=3)):
                ar[:] = i+1
        >>> print(d)
        [ 1.  1.  0.  2.  2.  0.  3.  3.  0.  4.  4.  0.]


        """
        if stepsize is None:
            stepsize = chunklen
        if startindex is None:
            startindex = 0
        if endindex is None:
            endindex = self.shape[0]

        if startindex > endindex:
            raise ValueError("startindex too high")
        if endindex > self.shape[0]:
            raise ValueError("endindex is too high")
        if startindex >= endindex:
            raise ValueError("startindex should be lower than endindex")
        nframes, newsize, remainder = fit_chunks(
            totallen=(endindex - startindex),
            chunklen=chunklen,
            steplen=stepsize)
        framestart = startindex
        frameend = framestart + chunklen
        with self._open_array(accessmode=accessmode) as (ar, fd):
            for i in range(nframes):
                yield ar[framestart:frameend]
                framestart += stepsize
                frameend = framestart + chunklen
            if include_remainder and (remainder > 0) and (
                    framestart < endindex):
                yield ar[framestart:endindex]

    def copy(self, path, dtype=None, chunklen=None, accessmode='r',
             overwrite=False):
        """Copy darr to a different path, potentially changing its dtype.

        The copying is performed in chunks to avoid RAM memory overflow for
        very large darr arrays.

        Parameters
        ----------
        path: str or pathlib.Path
        dtype: <dtype, None>
            Numpy data type of the copy. Default is None, which corresponds to
            the dtype of the darr to be copied.
        chunklen: <int, None>
            The length of chunks (along first axis) that are written during
            creation. If None, it is chosen so that chunks are 10 Mb in total
            size.
        accessmode: {'r', 'r+'}, default 'r'
            File access mode of the darr data of the returned Darr
            object. `r` means read-only, `r+` means read-write.
        overwrite: (True, False), optional
            Overwrites existing darr data if it exists. Note that a
            darr path is a directory. If that directory contains
            additional files, these will not be removed and an OSError is
            raised. Default is `False`.

        Returns
        -------
        Array
           copy of the darr

        """
        metadata = dict(self.metadata)
        return asarray(path=path, array=self, dtype=dtype,
                       accessmode=accessmode, metadata=metadata,
                       chunklen=chunklen, overwrite=overwrite)

    def _currentchecksums(self):
        filenames = self._filenames ^ {self._checksumsfilename}
        if len(self.metadata) == 0:
            filenames = filenames ^ {self._metadatafilename}
        checksums = {}
        for filename in filenames:
            checksums[filename] = self._md5(filename)
        return checksums

    def store_md5checksums(self):
        """Calculates md5 checksums of current data and stores them in a file
        'md5checksums.json'.

        Returns
        -------
        A dictionary with the checksums
        """
        checksums = self._currentchecksums()
        self._write_jsondict(self._checksumsfilename, checksums,
                             overwrite=True)
        return checksums

    def _storedmd5checksums(self):
        if not self._path.joinpath(self._checksumsfilename).exists():
            raise FileNotFoundError('No checksums have been computed before. '
                                    'Use `store_md5checksums` method if you '
                                    'want to save the current ones.')
        return self._read_jsondict(self._checksumsfilename)

    def assert_md5checksums(self):
        lastchecksums = self._storedmd5checksums()
        for fname, md5 in self._currentchecksums().items():
            if fname not in lastchecksums:
                raise ValueError(f"no checksum was stored for '{fname}'")
            elif not md5 == lastchecksums[fname]:
                raise ValueError(f"md5 checksums do not match for '{fname}'\n"
                                 f"previously: {lastchecksums[fname]}\n"
                                 f"now: {md5}\n")

    def set_accessmode(self, accessmode):
        """
        Set data access mode of data.

        Parameters
        ----------
        accessmode: {'r', 'r+'}, default 'r'
            File access mode of the data. `r` means read-only, `r+`
            means read-write.

        """
        self._accessmode = check_accessmode(accessmode)
        self._metadata.set_accessmode(accessmode)


def _fillgenerator(shape, dtype='float64', fill=0., fillfunc=None,
                   chunklen=None):
    """Private generator function to yield chunks of numpy arrays with
    requested values. To be used to write new large arrays to disk without
    flooding RAM.

    Parameters
    ----------
    shape : int ot sequence of ints
        Shape of the `darr`.
    dtype: <dtype>
        Numpy data type of the copy. Default is `float64`.
    fill : number, optional
        The value used to fill the array with. Default is `0`
    fillfunc : function, optional
        A function that generates the fill values, potentially on the basis of
        the index numbers of axis 0. This function should only have one
        argument, which will be automatically provided during filling and
        which represents the index numbers along axis 0 for all dimensions (see
        example below). If `fillfunc` is provided, `fill` should be `None`.
        And vice versa. Default is None.
    chunklen: <int, None>
        The length of chunks (along first axis) that are read and written
        during the process. Default is None, which corresponds to a
        reasonable preset value in many cases amounting to 10 Mb.

    Returns
    -------
    A generator yield numpy arrays

    """
    if not hasattr(shape, '__len__'):  # probably integer
        shape = (shape,)
    if shape[0] == 0: # empty array, we yield immediately
        yield np.empty(shape, dtype=dtype)
    dtype = np.dtype(dtype)
    if fill is None and fillfunc is None:
        fill = 0
    elif fill is not None and fillfunc is not None:
        raise ValueError("either 'fill' or 'fillfunc' should be provided, "
                         "not both")
    if chunklen is None:
        chunklen = max(int((80 * 1024 ** 2) // (np.product(shape[1:]) *
                                                dtype.itemsize)), 1)
    nchunks, restlen = divmod(shape[0], chunklen)
    chunkshape = [chunklen] + list(shape[1:])
    chunk = np.empty(chunkshape, dtype=dtype)
    i = np.empty(chunkshape, dtype='int64')
    i.T[:] = np.arange(chunklen, dtype='int64')
    if nchunks > 0:
        for n in range(nchunks):
            chunk[:] = fillfunc(i) if fill is None else fill
            yield chunk
            i += chunklen
    if restlen > 0:
        chunk[:] = fillfunc(i) if fill is None else fill
        yield chunk[:restlen]


def _archunkgenerator(array, dtype=None, chunklen=None):
    if (chunklen is None) and isinstance(array, (Array, np.ndarray)):
        chunklen = max(int((80 * 1024 ** 2) // (np.product(array.shape[1:]) *
                                                array.dtype.itemsize)), 1)
    else:
        chunklen = 1
    if hasattr(array, '__next__'):  # is already an iterator
        for chunk in array:
            yield np.asarray(chunk, dtype=dtype)
    elif isinstance(array, Array):
        for chunk in array.iterview(chunklen=chunklen):
            yield chunk.astype(dtype)
    elif hasattr(array, '__len__'):  # is numpy array or sequence
        totallen = len(array)
        if totallen == 0:
            yield array.astype(dtype)
        else:
            nchunks, newsize, remainder = fit_chunks(totallen=totallen,
                                                     chunklen=chunklen)
            for i in range(nchunks):
                yield np.asarray(array[i * chunklen:(i + 1) * chunklen],
                                 dtype=dtype)
            if remainder:
                yield np.asarray(array[-remainder:], dtype=dtype)
    else:
        try:  # could be a number
            yield np.array(array, dtype=dtype, ndmin=1)
        except Exception:
            raise TypeError(
                f"cannot object of type '{type(array)}' to an array")


def asarray(path, array, dtype=None, accessmode='r',
            metadata=None, chunklen=None, overwrite=False):
    """Save an array or array generator as a Darr array to file system path.

    Parameters
    ----------
    path : str or pathlib.Path
        File system path to which the array will be saved. Note that this will 
        be a directory containing multiple files.
    array : array-like object or generator yielding array-like objects
        This can be a numpy array, a sequence that can be converted into a 
        numpy array, or a generator that yields such objects. The latter will 
        be concatenated along the first dimension.
    dtype : `numpy dtype`, optional
        Is inferred from the data if `None`. If `dtype` is provided the data 
        will be cast to `dtype`. Default is `None`.
    accessmode : {`r`, `r+`}, optional
        File access mode of the darr that is returned. `r` means
        read-only, `r+` means read-write. In the latter case, data can be 
        changed. Default `r`.
    metadata: {None, dict}
        Dictionary with metadata to be saved in a separate JSON file. Default
    chunklen: <int, None>
        The length of chunks (along first axis) that are read and written
        during the process. If None and the `array` is a numpy array or
        darr, it is chosen so that chunks are 10 Mb in total size. If
        None and `array` is a generator or sequence, chunklen will be 1.
    overwrite: (True, False), optional
        Overwrites existing darr data if it exists. Note that a darr
        path is a directory. If that directory contains additional files, 
        these will not be removed and an OSError is raised. Default is `False`.

    Returns
    -------
    A Darr `array` instance.

    See Also
    --------
    create_array : create an array from scratch.

    Examples
    --------
    >>> asarray('data.da', [0,1,2,3])
    darr([0, 1, 2, 3])
    >>> asarray('data.da', [0,1,2,3], dtype='float64', overwrite=True)
    darr([ 0.,  1.,  2.,  3.])
    >>> ar = asarray('data_rw.da', [0,1,2,3,4,5], accessmode='r+')
    >>> ar
    darr([0, 1, 2, 3, 4, 5]) (r+)
    >>> ar[-1] = 8
    >>> ar
    darr([0, 1, 2, 3, 4, 8]) (r+)
    >>> ar[::2] = 9
    darr([9, 1, 9, 3, 9, 8]) (r+)


    """
    path = Path(path)
    if isinstance(array, Array) and (path == array.path):
        raise ValueError(f"'{path}' is the same as the path of the "
                         f"source darr.")
    chunkiter = _archunkgenerator(array, dtype=dtype, chunklen=chunklen)
    firstchunk = next(chunkiter)
    if firstchunk.ndim == 0:  # we received a number instead of an array
        firstchunk = np.array(firstchunk, ndmin=1, dtype=dtype)
    if firstchunk.dtype.name not in numtypes:
        raise TypeError(f"darr cannot have type "
                        f"'{firstchunk.dtype.name}'")
    dtype = firstchunk.dtype
    bd = create_basedir(path=path,
                        overwrite=overwrite)
    datapath = path.joinpath(Array._datafilename)
    arraylen = firstchunk.shape[0]
    with open(datapath, 'wb') as df:
        firstchunk.tofile(df)
        for chunk in chunkiter:
            if chunk.ndim == 0:
                chunk = np.array(chunk, ndmin=1, dtype=dtype)
            chunk.astype(dtype).tofile(df)  # is always C order
            arraylen += chunk.shape[0]
    shape = list(firstchunk.shape)
    shape[0] = arraylen
    datainfo = get_arraymetadata(firstchunk)
    if datainfo['arrayorder'] == 'F':
        # numpy's tofile always writes C order, hence we too
        warnings.warn("Warning: array is F_CONTIGUOUS, but data in file will "
                      "be C_CONTIGUOUS")
        datainfo['arrayorder'] = 'C'
    datainfo['shape'] = shape
    datainfo['darrversion'] = Array._formatversion
    bd._write_jsondict(filename=Array._arraydescrfilename,
                       d=datainfo, overwrite=overwrite)
    metadatapath = path.joinpath(Array._metadatafilename)
    if (metadata is not None) and (metadata != {}):
        bd._write_jsondict(filename=Array._metadatafilename,
                           d=metadata, overwrite=overwrite)
    elif metadatapath.exists():  # no metadata but file exists, remove it
        metadatapath.unlink()
    d = Array(path, accessmode=accessmode)
    d._update_readmetxt()
    return d


def check_accessmode(accessmode, validmodes=('r', 'r+'), makebinary=False):
    if accessmode not in validmodes:
        raise ValueError(f"Mode should be one of {validmodes}, not "
                         f"'{accessmode}'")
    if makebinary:
        accessmode += 'b'
    return accessmode


def create_basedir(path, overwrite=False):
    """
    Parameters
    ----------
    path: str or pathlib.Path
    overwrite: True or False, optional
        Default False

    Returns
    -------
    BaseDataDir instance
    
    """
    path = Path(path)
    if path.exists() and not overwrite:
        raise OSError(f"'{path}' directory already exists; "
                      f"use `overwrite` parameter to overwrite")
    else:
        if not path.exists():
            Path.mkdir(path)
            path = Path(path)
    return BaseDataDir(path)


#FIXME non-first axis len 0
def create_array(path, shape, dtype='float64', fill=None, fillfunc=None,
                 accessmode='r+', chunklen=None, metadata=None,
                 overwrite=False):
    """Create a new `darr` of given shape and type, filled with
    predetermined values.

    Parameters
    ----------
    path : str or pathlib.Path
        File system path to which the array will be saved. Note that this will
        be a directory containing multiple files.
    shape : int ot sequence of ints
        Shape of the `darr`.
    dtype : dtype, optional
        The type of the `darr`. Default is 'float64'
    fill : number, optional
        The value used to fill the array with. Default is `None`, which will
        lead to the array being filled with zeros.
    fillfunc : function, optional
        A function that generates the fill values, potentially on the basis of
        the index numbers of the first axis of the array. This function should
        only have one argument, which will be automatically provided during
        filling and which represents the index numbers along the first axis for
        all dimensions (see example below). If `fillfunc` is provided, `fill`
        should be `None`.  And vice versa. Default is None.
    accessmode : <`r`, `r+`>, optional
        File access mode of the darr data. `r` means real-only, `r+`
        means read-write, i.e. values can be changed. Default `r`.
    chunklen: <int, None>
        The length of chunks (along first axis) that are written during
        creation. If None, it is chosen so that chunks are 10 Mb in total size.
    metadata: {None, dict}
        Dictionary with metadata to be saved in a separate JSON file. Default
        None
    overwrite: <True, False>, optional
        Overwrites existing darr data if it exists. Note that a darr
        paths is a directory. If that directory contains additional files, 
        these will not be removed and an OSError is raised.
        Default is `False`.

    Returns
    -------
    A Darr `array` instance.

    See Also
    --------
    asarray : create a darr from existing array-like object or
        generator.

    Examples
    --------
    >>> import darr as da
    >>> da.create_array('testarray0', shape=(5,2))
    darr([[ 0.,  0.],
       [ 0.,  0.],
       [ 0.,  0.],
       [ 0.,  0.],
       [ 0.,  0.]]) (r+)
    >>> da.create_array('testarray1', shape=(5,2), dtype='int16')
    darr([[0, 0],
       [0, 0],
       [0, 0],
       [0, 0],
       [0, 0]], dtype=int16) (r+)
    >>> da.create_array('testarray3', shape=(5,2), fill=23.4)
    darr([[ 23.4,  23.4],
       [ 23.4,  23.4],
       [ 23.4,  23.4],
       [ 23.4,  23.4],
       [ 23.4,  23.4]]) (r+)
    >>> fillfunc = lambda i: i * 2 darr
    >>> da.create_array('testarray4', shape=(5,), fillfunc=fillfunc)
    darr([ 0.,  2.,  4.,  6.,  8.]) (r+)
    >>> fillfunc = lambda i: i * [1, 2]
    >>> da.create_array('testarray4', shape=(5,2), fillfunc=fillfunc)
    darr([[ 0.,  0.],
       [ 1.,  2.],
       [ 2.,  4.],
       [ 3.,  6.],
       [ 4.,  8.]]) (r+)

    """
    gen = _fillgenerator(shape=shape, dtype=dtype, fill=fill,
                         fillfunc=fillfunc, chunklen=chunklen)
    return asarray(path=path, array=gen, accessmode=accessmode,
                   metadata=metadata, overwrite=overwrite)


def delete_array(da):
    """
    Delete darr data from disk.
    
    Parameters
    ----------
    da: Array or str or pathlib.Path
        The darr object to be deleted or file system path to it.

    """
    try:
        if not isinstance(da, Array):
            da = Array(da)
    except Exception:
        raise TypeError(f"'{da}' not recognized as a Darr array")
    da.check_arraywriteable()
    for fn in da._filenames:
        path = da.path.joinpath(fn)
        if path.exists():
            path.unlink()
    try:
        da._path.rmdir()
    except OSError as error:
        message = f"Error: could not fully delete Darr array directory " \
                  f"'{da.path}'. It may contain additional files that are " \
                  f"not part of the darr. If so, these should be removed " \
                  f"manually."
        raise OSError(message) from error


def truncate_array(a, index):
    """Truncate darr data.

    Parameters
    ----------
    a: array or str or pathlib.Path
       The darr object to be truncated or file system path to it.
    index: int
        The index along the first axis at which the darr should be
        truncated. Negative indices can be used but the resulting length of
        the truncated darr should be larger than 0 and smaller than the
        current length.

    Examples
    --------
    >>> import darr as da
    >>> fillfunc = lambda i: i
    >>> a = da.create_array('testarray.da', shape=(5,2), fillfunc=fillfunc)
    >>> a
    darr([[ 0.,  0.],
               [ 1.,  1.],
               [ 2.,  2.],
               [ 3.,  3.],
               [ 4.,  4.]]) (r+)
    >>> da.truncate_array(a, 3)
    >>> a
    darr([[ 0.,  0.],
               [ 1.,  1.],
               [ 2.,  2.]]) (r+)
    >>> da.truncate_array(a, -1)
    >>> a
    darr([[ 0.,  0.],
               [ 1.,  1.]]) (r+)

    """

    try:
        if not isinstance(a, Array):
            a = Array(a)
    except Exception:
        raise TypeError(f"'{a}' not recognized as a darr")
    a.check_arraywriteable()
    if not isinstance(index, int):
        raise TypeError(f"'index' should be an int (is {type(index)})")
    with a.view() as v:
        newlen = len(v[:index])
    lenincrease = newlen - len(a)
    if 0 < newlen < len(a):
        i = newlen * np.product(a.shape[1:]) * a.dtype.itemsize
        os.truncate(a._datapath, i)
        a._update_len(lenincrease)
    else:
        raise ValueError(f"'index' {index} would yield an array of length "
                         f"{newlen}, which is invalid (current length is "
                         f"{len(a)})")


def fit_chunks(totallen, chunklen, steplen=None):
    """
    Calculates how many frames of 'chunklen' fit in 'totallen',
    given a step size of 'steplen'.

    Parameters
    ----------
    totallen: int
        Size of total
    chunklen: int
        Size of frame
    steplen: int
        Step size, defaults to chunksize (i.e. no overlap)

    """

    if ((totallen % 1) != 0) or (totallen < 1):
        raise ValueError(f"invalid totalsize ({totallen})")
    if ((chunklen % 1) != 0) or (chunklen < 1):
        raise ValueError(f"invalid chunklen ({chunklen})")
    if chunklen > totallen:
        return 0, 0, totallen
    if steplen is None:
        steplen = chunklen
    else:
        if ((steplen % 1) != 0) or (steplen < 1):
            raise ValueError("invalid stepsize")
    totallen = int(totallen)
    chunklen = int(chunklen)
    steplen = int(steplen)
    nchunks = ((totallen - chunklen) // steplen) + 1
    newsize = nchunks * steplen + (chunklen - steplen)
    remainder = totallen - newsize
    return nchunks, newsize, remainder


def arraydescrtodtype(arraydescr):
    numtype = numtypes.get(arraydescr['numtype'], None)
    if numtype is None:
        raise ValueError(
            f"'{arraydescr['numtype']}' is not a valid numeric type")
    numpytype = numtype['numpy']
    if arraydescr['byteorder'] == 'little':
        dtypedescr = f'<{numpytype}'
    elif arraydescr['byteorder'] == 'big':
        dtypedescr = f'>{numpytype}'
    else:
        raise ValueError(f"'{arraydescr['byteorder']}' is not a valid order")
    return dtypedescr


def get_arraymetadata(ndarray):
    sys_is_le = (sys.byteorder == 'little')
    bo = ndarray.dtype.byteorder
    if (bo == '<') or (sys_is_le and (bo in ('|', '='))):
        bostr = 'little'
    else:
        bostr = 'big'
    return {  # 'dtypedescr': str(ndarray.dtype.descr[0][1]),
        'numtype': ndarray.dtype.name,
        'arrayorder': 'C' if ndarray.flags['C_CONTIGUOUS'] else 'F',
        'shape': ndarray.shape,
        'byteorder': bostr}


def get_arrayorderdescr(arrayorder):
    if arrayorder == 'C':
        return 'Row-major; last dimension varies most rapidly with ' \
               'memory address'
    elif arrayorder == 'F':
        return 'Column-major; first dimension varies most rapidly with ' \
               'memory address'
    else:
        raise ValueError(f'arrayorder type "{arrayorder}" unknown')


def formatdescriptiontxt(da):
    md = da._arraydescr
    numdescr = numtypes[md['numtype']]['descr']
    arrayorderdescr = get_arrayorderdescr(md['arrayorder'])
    endianness = md['byteorder']
    d = f"Description of data format\n" \
        f"==========================\n\n" \
        f"The file 'arrayvalues.bin' contains a numeric array in the " \
        f"following format:\n\n" \
        f"Numeric type: {numdescr}\n" \
        f"Byte order: {endianness} ({endiannesstypes[endianness]['descr']})\n"
    if da.ndim == 1:
        d += f"Array length:  {md['shape'][0]}\n"
    else:
        d += f"Array dimensions:  {md['shape']}\n"
    d += f"Array order layout:  {md['arrayorder']} ({arrayorderdescr})\n\n" \
         f"The file only contains the raw binary values, without header " \
         f"information.\n\n" \
         f"Format details are also stored in json format in the separate " \
         f"UTF-8 text file, 'arraydescription.json'.\n\n" \
         f"If present, the file 'metadata.json' contains metadata in json " \
         f"UTF-8 text format.\n\n"
    return d


def readcodenumpy(typedescr, shape, arrayorder, **kwargs):
    ct = f"import numpy as np\n" \
         f"a = np.fromfile('arrayvalues.bin', dtype='{typedescr}')\n"
    if len(shape) > 1:  # multidimensional, we need reshape
        ct += f"a = a.reshape({shape}, order='{arrayorder}')\n"
    return ct


def readcodenumpymemmap(typedescr, shape, arrayorder, **kwargs):
    ct = "import numpy as np\n"
    ct += f"a = np.memmap('arrayvalues.bin', dtype='{typedescr}', " \
          f"shape={shape}, order='{arrayorder}')\n"
    return ct


def readcodematlab(typedescr, shape, endianness, **kwargs):
    shape = list(shape)[::-1]  # darr is always C order, Matlab is F order
    size = np.product(shape)
    ndim = len(shape)
    ct = "fileid = fopen('arrayvalues.bin');\n"
    if ndim == 1:
        ct += f"a = fread(fileid, {size}, '*{typedescr}', '{endianness}');\n"
    elif ndim == 2:
        ct += f"a = fread(fileid, {shape}, '*{typedescr}', " \
              f"'{endianness}');\n"
    else:  # ndim > 2, we need reshape to get multidimensional array
        ct += f"a = reshape(fread(fileid, {size}, '*{typedescr}', " \
              f"'{endianness}'), {shape});\n"
    return ct + "fclose(fileid);\n"


def readcoder(typedescr, shape, endianness, **kwargs):
    # typedecr is a dict, with 'what', 'size' and 'n' keys
    shape = shape[::-1]  # darr is always C order, R is F order
    n = np.product(shape)
    ct = 'fileid = file("arrayvalues.bin", "rb")\n' \
         'a = readBin(con=fileid, what={what}, n={n}, size={size}, ' \
         'endian="{endianness}")\n'.format(endianness=endianness, n=n,
                                           **typedescr)
    if len(shape) > 1:
        ct += f'a = array(data=a, dim=c{shape}, dimnames=NULL)\n'
    return ct + 'close(fileid)\n'


def readcodejulia(typedescr, shape, endianness, **kwargs):
    # this does not work if numtype is complex and byteorder is different on
    # reading machine, will generate an error, so we accept this.
    shape = shape[::-1]  # darr is always C order, Julia is F order
    return f'fileid = open("arrayvalues.bin","r");\n' \
           f'a = map({endianness}, read(fileid, {typedescr}, {shape}));\n' \
           f'close(fileid);\n'


def readcodeidl(typedescr, shape, endianness, **kwargs):
    shape = list(shape[::-1])
    return f'a = read_binary("arrayvalues.bin", data_type={typedescr}, ' \
           f'data_dims={shape}, endian="{endianness}")\n'


def readcodemathematica(typedescr, shape, endianness, **kwargs):
    dimstr = str(shape)[1:-1]
    if dimstr.endswith(','):
        dimstr = dimstr[:-1]
    dimstr = '{' + dimstr + '}'
    return f'a = BinaryReadList["arrayvalues.bin", "{typedescr}", ' \
           f'ByteOrdering -> {endianness}];\n' \
           f'a = ArrayReshape[a, {dimstr}];\n'


readcodefunc = {
        'idl': readcodeidl,
        'julia': readcodejulia,
        'mathematica': readcodemathematica,
        'matlab': readcodematlab,
        'numpy': readcodenumpy,
        'numpymemmap': readcodenumpymemmap,
        'R': readcoder,
}


def readcode(da, language):
    arraydescription = da._arraydescr
    if language not in readcodefunc:
        raise ValueError(f"'{language}' not supported ({readcodefunc.keys()})")
    kwargs = {}
    if 'numpy' in language:
        kwargs['typedescr'] = arraydescription['dtypedescr']
    else:
        kwargs['typedescr'] = numtypes[arraydescription['numtype']][language]
    kwargs['shape'] = arraydescription['shape']
    byteorder = arraydescription['byteorder']
    kwargs['endianness'] = endiannesstypes[byteorder][language]
    kwargs['arrayorder'] = arraydescription['arrayorder']
    if kwargs['typedescr'] is None:
        return None
    else:
        return readcodefunc[language](**kwargs)


def promptify_codetxt(codetxt, prompt=">>> "):
    return "\n".join([f"{prompt}{l}" for l in codetxt.splitlines()]) + '\n'


def arrayreadmetxt(da):
    s = formatdescriptiontxt(da)
    s += "Example code for reading the data\n" \
         "=================================\n\n"
    languages = (
        ("Python with Numpy:", "numpy"),
        ("Python with Numpy (memmap):", "numpymemmap"),
        ("R:", "R"),
        ("Matlab/Octave:", "matlab"),
        ("Julia:", "julia"),
        ("IDL/GDL:", "idl"),
        ("Mathematica:", "mathematica")
    )
    for heading, language in languages:
        codetext = readcode(da, language)
        if codetext is not None:
            s += f"{heading}\n{'-'*len(heading)}\n{codetext}\n"
    return s


def write_jsonfile(path, data, sort_keys=True, indent=4, ensure_ascii=True,
                   overwrite=False):
    path = Path(path)
    if path.exists() and not overwrite:
        raise OSError(f"'{path}' exists, use 'overwrite' argument")
    try:
        json_string = json.dumps(data, sort_keys=sort_keys,
                                 ensure_ascii=ensure_ascii, indent=indent)
    except TypeError:
        print(f"Unable to serialize the metadata to JSON: {data}.\n"
              f"Use character strings as dictionary keys, and only "
              f"character strings, numbers, booleans, None, lists, "
              f"and dictionaries as objects.")
        raise
    else:
        # utf-8 is ascii compatible
        with open(path, 'w', encoding='utf-8') as fp:
            fp.write(json_string)
