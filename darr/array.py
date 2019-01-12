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
import json
import os
import sys
import tarfile


import warnings
from contextlib import contextmanager
from pathlib import Path

import numpy as np

from .numtype import arrayinfotodtype, arraynumtypeinfo, numtypesdescr
from .readcodearray import readcode
from .utils import fit_chunks, filesha256, wrap
from ._version import get_versions


# Design considerations
# ---------------------
# - All text is written in UTF-8. This is compatible with ASCII, widely used
#   and capable of encoding all 1,112,064 valid code points in Unicode

__all__ = ['Array', 'asarray', 'create_array', 'delete_array',
           'truncate_array']


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

    @property
    def sha256(self):
        """Checksums (sha256) of files."""
        return self._sha256checksums()

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

    def _sha256checksums(self):
        checksums = {}
        for filepath in self.path.iterdir():
            checksums[str(filepath)] = filesha256(filepath)
        return checksums

    @contextmanager
    def open_file(self, filename, mode='r', buffering=-1, encoding=None,
                  errors=None, newline=None, closefd=True):
        """Open a file in the darr array directory and yield a file object.
        Protected files, i.e. those that are part of the darr array may not be
        opened.

        This method is a thin wrapper of the that of the Python 'open'
        function. The parameters are therefore the same.

        Examples
        --------
        >>> import darr as da
        >>> d = da.create_array('recording.darr', shape=(12,))
        >>> with d.open_file('notes.txt', 'a') as f:
        ...     n = f.write('excellent recording\\n')

        """
        filepath = self.path / Path(filename)
        if filepath.name in self._filenames:
            raise OSError(f'Cannot open protected darr file "{filename}"')

        with open(file=filepath, mode=mode, buffering=buffering,
                  encoding=encoding, errors=errors, newline=newline,
                  closefd=closefd) as f:
            yield f

    def archive(self,  filepath=None, compressiontype='xz', overwrite=False):
        """Archive disk-based data into a single compressed file.

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
        if filepath is None:
            filepath = f'{self.path}.tar.{compressiontype}'
        if overwrite:
            filemode = 'w'
        else:
            filemode = 'x'
        supported_compressiontypes = ('xz', 'gz', 'bz2')
        if compressiontype not in supported_compressiontypes:
            raise ValueError(f'"{compressiontype}" is not a valid '
                             f'compressiontype, use one of '
                             f'{supported_compressiontypes}.')
        with tarfile.open(filepath, f"{filemode}:{compressiontype}") as tf:
            tf.add(self.path)
        return Path(filepath)


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
        """
        Set data access mode of metadata.

        Parameters
        ----------
        accessmode: {'r', 'r+'}, default 'r'
            File access mode of the data. `r` means read-only, `r+`
            means read-write.

        """
        return self._accessmode

    @accessmode.setter
    def accessmode(self, value):
        self._accessmode = check_accessmode(value)

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
        if self._accessmode == 'r':
            raise OSError("metadata not writeable; change 'accessmode' to "
                          "'r+'")
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
        if self._accessmode == 'r':
            raise OSError("metadata not writeable; change 'accessmode' to "
                          "'r+'")
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
            raise OSError("metadata not writeable; change 'accessmode' to "
                          "'r+'")
        metadata = self._read()
        metadata.update(*arg, **kwargs)

        write_jsonfile(self.path, data=metadata, sort_keys=True,
                       ensure_ascii=True, overwrite=True)


class Array(BaseDataDir):
    """Instantiate a Darr array from disk.

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
    _metadatafilename = 'metadata.json'
    _readmefilename = 'README.txt'
    _filenames = {_arraydescrfilename, _datafilename,
                  _readmefilename,
                  _metadatafilename} | BaseDataDir._filenames
    _formatversion = get_versions()['version']

    def __init__(self, path, accessmode='r'):
        BaseDataDir.__init__(self, path=path)
        self._datapath = self._path / self._datafilename
        self._accessmode = check_accessmode(accessmode)
        self._arraydescrpath = self._path / self._arraydescrfilename
        self._arrayinfo = self._read_arraydescr()
        self._memmap = None
        self._valuesfd = None
        self._check_arrayinfoconsistency()
        with self._open_array() as (ar, _):
            self._dtype = ar.dtype
            self._shape = ar.shape
            self._size = ar.size
        self._metadata = MetaData(self._path / self._metadatafilename,
                                  accessmode=accessmode)

    @property
    def accessmode(self):
        """Data access mode of metadata, {'r', 'r+'}."""
        return self._accessmode

    @accessmode.setter
    def accessmode(self, value):
        self._accessmode = check_accessmode(value, validmodes=('r', 'r+'),
                                            makebinary=False)
        self._metadata.accessmode = value

    @property
    def dtype(self):
        """Numpy data type of the array values."""
        return self._dtype

    @property
    def metadata(self):
        """Dictionary-like interface to metadata."""
        return self._metadata

    @property
    def itemsize(self):
        """The size in bytes of each item in the array."""
        return self._dtype.itemsize

    @property
    def nbytes(self):
        """Array size in bytes, excluding metadata."""
        return self._size * self._dtype.itemsize

    @property
    def mb(self):
        """Array size in megabytes, excluding metadata."""
        return self.nbytes / 1e6

    @property
    def ndim(self):
        """Number of dimensions """
        return len(self._shape)

    @property
    def shape(self):
        """Tuple with sizes of each axis of the data array."""
        return self._shape

    @property
    def size(self):
        """Total number of values in the data array."""
        return int(self._size)

    def __getitem__(self, index):
        with self._open_array() as (ar, _):
            values = np.array(ar[index], copy=True)
        return values

    def __setitem__(self, index, value):
        with self._open_array() as (ar, _):
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
                    d = self._arrayinfo
                    dtypedescr = arrayinfotodtype(d)
                    if np.product(d['shape']) == 0:  # empty file/array
                        self._memmap = np.zeros(d['shape'], dtype=dtypedescr,
                                                order=d['arrayorder'])
                    else:
                        self._memmap = np.memmap(filename=fd,
                                                 mode=memmapmode,
                                                 shape=d['shape'],
                                                 dtype=dtypedescr,
                                                 order=d['arrayorder'])
                    yield self._memmap, self._valuesfd
            except Exception:
                raise
            finally:
                # self._memmap._mmap.close() # may need this for Windows
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

        with self._open_array(accessmode=accessmode) as (memmap, _):
            yield memmap

    def _read_arraydescr(self):
        """
        Private method to read everything we need to know about the numeric
        data type and layout from the json file that holds this info

        There are 4 essential parameters in this file:

        numtype: the numeric types that Darr supports; these are listed in
                 the 'numtypes' dict in the numtype module, like 'int8' etc.
        shape: a list with dimension lengths
        arrayorder: 'C' or 'F'
        darrversion: a string in loose version format


        """
        requiredkeys = {'numtype', 'shape', 'arrayorder', 'darrversion'}
        try:
            d = self._read_jsondict(filename=self._arraydescrfilename,
                                    requiredkeys=requiredkeys)
        except Exception as e:
            m = f". Could not read array description from "\
                f"'{self._arraydescrpath}. '"
            raise type(e)(str(e) + m).with_traceback(sys.exc_info()[2])
        vfile = distutils.version.LooseVersion(d['darrversion'])
        vlib = distutils.version.LooseVersion(self._formatversion)
        # for now, in alpha stage, we do not recommend the use of newer files
        # with older libraries
        if not vlib >= vfile:
            warnings.warn(f"Format version of file ({d['darrversion']}) "
                          f"is newer than your version of Darr "
                          f"{self._formatversion}. At this stage this is not "
                          f"guaranteed to work", UserWarning)
        try:
            d['shape'] = tuple(d['shape'])  # json does not have tuples
            if not all(isinstance(d, int) for d in d['shape']):  # all ints?
                raise TypeError(f"'{d['shape']}' is not a valid array shape")
        except TypeError:
            raise
        d['dtypedescr'] = arrayinfotodtype(d)
        try:
            if d['arrayorder'] not in {'C', 'F'}:
                raise ValueError(
                    f"'{d['arrayorder']}' is not a valid numpy arrayorder")
        except Exception:
            raise
        return d

    def _check_arrayinfoconsistency(self):
        ai = self._arrayinfo
        dtype = np.dtype(arrayinfotodtype(ai))
        expectedfilesize = np.product(ai['shape']) * dtype.itemsize
        actualfilesize = self._datapath.stat().st_size
        if actualfilesize != expectedfilesize:
            raise ValueError(
                f"binary file size ({actualfilesize}) is different from file "
                f"size as expected from array info file ({expectedfilesize})")

    def _check_consistency(self):
        if not (self._read_arraydescr() == self._arrayinfo):
            raise ValueError("in-memory and on-disk array info not "
                             "the same")
        self._check_arrayinfoconsistency()

    def check_arraywriteable(self):
        with self._open_array() as (ar, fd):
            if not ar.flags.writeable:
                raise OSError("darr not writeable; change 'accessmode' "
                              "attribute to 'r+'")

    def _update_len(self, lenincrease):
        newshape = list(self.shape)
        newshape[0] += lenincrease
        self._shape = tuple(newshape)
        self._size = np.product(self._shape)
        self._arrayinfo.update(shape=self._shape)
        self._write_jsondict(filename=self._arraydescrfilename,
                             d=self._arrayinfo, overwrite=True)
        self._update_readmetxt()

    def _update_readmetxt(self):
        txt = readcodetxt(self)
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
        compliant with Darr arrays.

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
                for array in arrayiterable:
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

        if endindex > self.shape[0]:
            raise ValueError("endindex is too high")
        if startindex >= endindex:
            raise ValueError("startindex should be lower than endindex")
        nframes, _, remainder = fit_chunks(
            totallen=(endindex - startindex),
            chunklen=chunklen,
            steplen=stepsize)
        framestart = startindex
        frameend = framestart + chunklen
        with self._open_array(accessmode=accessmode) as (ar, _):
            for _ in range(nframes):
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
           copy of the darr array

        """
        metadata = dict(self.metadata)
        return asarray(path=path, array=self, dtype=dtype,
                       accessmode=accessmode, metadata=metadata,
                       chunklen=chunklen, overwrite=overwrite)


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
    generator
        A generator that yields numpy arrays

    """
    if not hasattr(shape, '__len__'):  # probably integer
        shape = (shape,)
    if shape[0] == 0:  # empty array, we yield immediately
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
        for _ in range(nchunks):
            chunk[:] = fillfunc(i) if fill is None else fill
            yield chunk
            i += chunklen
    if restlen > 0:
        chunk[:] = fillfunc(i) if fill is None else fill
        yield chunk[:restlen]


def _archunkgenerator(array, dtype=None, chunklen=None):
    if chunklen is None:  # we try to make a reasonable guess
        if hasattr(array, 'shape') and hasattr(array, 'dtype'):
            chunklen = int((80 * 1024 ** 2) // (np.product(array.shape[1:]) *
                                                array.dtype.itemsize))
        else:
            chunklen = (1024 ** 2)
    chunklen = max(chunklen, 1)
    if hasattr(array, '__next__'):  # is already an iterator, ignore chunklen
        for chunk in array:
            yield np.asarray(chunk, dtype=dtype)
    elif isinstance(array, Array):
        for chunk in array.iterview(chunklen=chunklen):
            yield chunk
    elif hasattr(array, '__len__'):  # is numpy array or sequence
        totallen = len(array)
        if totallen == 0:
            yield array.astype(dtype)
        else:
            nchunks, _, remainder = fit_chunks(totallen=totallen,
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
        Dictionary with metadata to be saved in a separate JSON file.
        Default is None. If so, and the array has a 'metadata' attribute,
        Darr will try to use it as metadata of the output array.
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
    Array
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
    if metadata is None and hasattr(array, 'attrs'):  # e.g. zarr array
        try:  # see if we can use it as json dict
            metadata = dict(array.attrs)
            json.dumps(metadata, ensure_ascii=True)
        except Exception:
            warnings.warn("Found metadata but could not read it as a " 
                          "dictionary. Not saving it as part of darr array")
    if isinstance(array, Array) and (path == array.path):
        raise ValueError(f"'{path}' is the same as the path of the "
                         f"source darr.")
    chunkiter = _archunkgenerator(array, dtype=dtype, chunklen=chunklen)
    firstchunk = next(chunkiter)
    if firstchunk.ndim == 0:  # we received a number instead of an array
        firstchunk = np.array(firstchunk, ndmin=1, dtype=dtype)
    if firstchunk.dtype.name not in numtypesdescr.keys():
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
    datainfo = arraynumtypeinfo(firstchunk)
    if datainfo['arrayorder'] == 'F':
        # numpy's tofile always writes C order, hence we too
        warnings.warn("Warning: array is F_CONTIGUOUS, but data in file will "
                      "be C_CONTIGUOUS")
        datainfo['arrayorder'] = 'C'
    datainfo['shape'] = shape
    datainfo['darrversion'] = Array._formatversion
    datainfo['darrobject'] = 'Array'
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
    BaseDataDir
    
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


# FIXME non-first axis len 0
def create_array(path, shape, dtype='float64', fill=None, fillfunc=None,
                 accessmode='r+', chunklen=None, metadata=None,
                 overwrite=False):
    """Create a new `darr array` of given shape and type, filled with
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
    Array
        A Darr `array` instance.

    See Also
    --------
    asarray : create a darr array from existing array-like object or
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
    Delete Darr array data from disk.
    
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


def readcodetxt(da):
    """Returns text on how to read a Darr array numeric binary data in various
    programming languages.

    Parameters
    ----------
    da: Darr array

    """

    s = numtypedescriptiontxt(da)
    s += "Example code for reading the data\n" \
         "=================================\n\n"
    languages = (
        ("Python with Numpy:", "numpy"),
        ("Python with Numpy (memmap):", "numpymemmap"),
        ("R:", "R"),
        ("Matlab/Octave:", "matlab"),
        ("Julia (version < 1.0):", "julia0"),
        ("Julia (version >= 1.0):", "julia1"),
        ("IDL/GDL:", "idl"),
        ("Mathematica:", "mathematica"),
        ("Maple:", "maple")
    )
    for heading, language in languages:
        codetext = readcode(da, language)
        if codetext is not None:
            s += f"{heading}\n{'-'*len(heading)}\n{codetext}\n"
    return s


def numtypedescriptiontxt(da):
    """Returns a paragraph of text that describes Darr array type and layout
    information, as well as some additional info on how metadata is stored etc.

    Parameters
    ----------
    da: Darr array


    """
    d = da._arrayinfo
    shape = d['shape']
    typedescr = numtypesdescr[d['numtype']]
    arrayorder = d['arrayorder']
    endianness = d['byteorder']
    if endianness == 'little':
        endiannessdescr = 'most-significant byte last'
    elif endianness == 'big':
        endiannessdescr = 'most-significant byte first'
    if arrayorder == 'C':
        arrayorderdescr = 'Row-major; last dimension varies most rapidly ' \
                          'with memory address'
    elif arrayorder == 'F':
        arrayorderdescr = 'Column-major; first dimension varies most rapidly ' \
                          'with memory address'
    else:
        raise ValueError(f'arrayorder type "{arrayorder}" unknown')
    s = wrap("This directory contains a numeric array. The array can be "
             "read in Python using the Darr library "
             "(https://pypi.org/project/darr/), but if that is not available "
             "it should be straightforward to read the data in other "
             "environments using the information below.") + "\n\n"
    s+= f"Description of data format\n==========================\n\n"
    s += wrap("The file 'arrayvalues.bin' contains a numeric array in the "
              "following format:") + "\n\n"
    s +=f"  Numeric type: {typedescr}\n" \
        f"  Byte order: {endianness} ({endiannessdescr})\n"
    if da.ndim == 1:
        s += f"  Array length: {shape[0]}\n"
    else:
        s += f"  Array dimensions: {shape}\n"
    s += f"  Array order layout:  {arrayorder} ({arrayorderdescr})\n\n"
    s += wrap("The file only contains the raw binary values, without header "
              "information.") + "\n\n"
    s += wrap("Format details are also stored in json format in the separate "
              "UTF-8 text file, 'arraydescription.json' to facilitate "
              "automatic reading by a program.") + "\n\n"
    s += wrap("If present, the file 'metadata.json' contains metadata in json "
              "UTF-8 text format.") + "\n\n"
    return s
