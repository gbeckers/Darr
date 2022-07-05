from pathlib import Path
from contextlib import contextmanager

import numpy as np
from ._version import get_versions

from .array import Array, asarray, check_accessmode, create_array
from .raggedarray import RaggedArray, asraggedarray
from .datadir import DataDir, create_datadir
from .metadata import MetaData
from .readcoderaggedarray import readcode, readcodefunc
from .utils import wrap

__all__ = ['VarDimArray', 'asvardimarray', 'create_vardimarray']


class VarDimArray:
    _valuesdirname = 'values'
    _indicesandshapesdirname = 'indicesandshapes'
    _arraydescrfilename = 'arraydescription.json'
    _metadatafilename = 'metadata.json'
    _readmefilename = 'README.txt'
    _protectedfiles = {_valuesdirname, _indicesandshapesdirname,
                       _readmefilename, _metadatafilename,
                       _arraydescrfilename}
    _formatversion = get_versions()['version']

    def __init__(self, path, accessmode='r'):
        self._datadir = DataDir(path=path,
                                protectedpaths=self._protectedfiles)
        self._path = self._datadir._path
        self._accessmode = check_accessmode(accessmode)
        self._valuespath = self._path / self._valuesdirname
        self._indicesandshapespath = self._path / self._indicesandshapesdirname
        self._arraydescrpath = self._path / self._arraydescrfilename
        self._values = Array(self._valuespath, accessmode=self._accessmode)
        self._indicesandshapes = RaggedArray(self._indicesandshapespath,
                                        accessmode=self._accessmode)
        self._metadata = MetaData(self._path / self._metadatafilename,
                                  accessmode=accessmode)
        arrayinfo = {}
        arrayinfo['len'] = len(self._indicesandshapes)
        arrayinfo['size'] = self._values.size
        arrayinfo['numtype'] = self._values._arrayinfo['numtype']
        arrayinfo['darrversion'] = VarDimArray._formatversion
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
        self._indicesandshapes.accessmode = value

    @property
    def dtype(self):
        """Numpy data type of the array values.

        """
        return self._values._dtype

    @property
    def datadir(self):
        """Data directory object with many useful methods, such as
        writing information to text or json files, archiving all data,
        calculating checksums etc."""
        return self._datadir

    @property
    def narrays(self):
        """number of subarrays in the RaggedArray.

        """
        return len(self._indicesandshapes)

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
        return self._values.mb + self._indicesandshapes.mb

    @property
    def path(self):
        """File system path to array data"""
        return self._path

    @property
    def size(self):
        """Total number of values in the ragged array."""
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
        indicesandshape = self._indicesandshapes[item]
        print(indicesandshape)
        index = slice(*indicesandshape[:2])
        print(index)
        shape = indicesandshape[2:]
        print(shape)
        return self._values[index].reshape(shape)

    def __len__(self):
        return len(self._indicesandshapes)

    def __repr__(self):
        return f'VarDimArray ({self.narrays} variable dimension subarrays ' \
               f'({self.accessmode})'

    __str__ = __repr__

    def _update_readmetxt(self):
        txt = readcodetxt(self)
        self._datadir._write_txt(self._readmefilename, txt, overwrite=True)

    def _update_arraydescr(self, **kwargs):
        self._arrayinfo.update(kwargs)
        self._datadir._write_jsondict(filename=self._arraydescrfilename,
                                      d=self._arrayinfo, overwrite=True)

    def _append(self, array):
        array = np.asarray(array, dtype=self.dtype)
        size = array.size
        endindex = self._values.shape[0]
        self._values.append(array.flatten())
        self._indicesandshapes.append([endindex, endindex + size] \
                                       + list(array.shape))


    def append(self, array):
        """Append array-like objects to the ragged array.

        The shape of the data and the darr must be compliant. The length of
        its first axis may vary, but if the are more axes, these should
        have the same lengths as all other subarrays (which is the `atom` of
        the raged array). When appending data repeatedly it is more efficient
        to use `iterappend`.


        Parameters
        ----------
        array: array-like object
            This can be a numpy array, a sequence that can be converted into a
            numpy array.

        Returns
        -------
            None

        """
        self._append(array)
        self._update_readmetxt()
        self._update_arraydescr(len=len(self._indicesandshapes),
                                size=self._values.size)

    def copy(self, path, dtype=None, accessmode='r', overwrite=False):
        """Copy vardimarray to a different path, potentially changing its
        dtype.

        The copying is performed in chunks to avoid RAM memory overflow for
        very large darr arrays.

        Parameters
        ----------
        path: str or pathlib.Path
        dtype: <dtype, None>
            Numpy data type of the copy. Default is None, which corresponds to
            the dtype of the darr to be copied.
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
        arrayiterable = (self[i] for i in range(len(self)))
        metadata = dict(self.metadata)
        if dtype is None:
            dtype = self.dtype
        return asvardimarray(path=path, arrayiterable=arrayiterable,
                             dtype=dtype, metadata=metadata,
                             accessmode=accessmode, overwrite=overwrite)
    # FIXME
    @contextmanager
    def _view(self, accessmode=None):
        with self._indicesandshapes._view(accessmode=accessmode) as (iv, _), \
                self._values._open_array(accessmode=accessmode) as (vv, _):
            yield iv, vv

    def iter_arrays(self, startindex=0, endindex=None, stepsize=1,
                 accessmode=None):
        """Iterate over vardim array yielding subarrays.

        startindex: <int, None>
            Start index value.
            Default is None, which means to start at the beginning.
        endindex: <int, None>
            End index value.
            Default is None, which means to end at the end.
        stepsize: <int, None>
            Size of the shift per iteration across the first axis.
            Default is None, which means that `stepsize` equals `chunklen`.

        """

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
        # TODO refactor such that info in index and values array files are not
        # updated at each append
        with self._view():
            for a in arrayiterable:
                self._append(a)
        self._update_readmetxt()
        self._update_arraydescr(len=len(self._indicesandshapes),
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
        """Archive ragged array data into a single compressed file.

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

def asvardimarray(path, arrayiterable, dtype=None, metadata=None,
                  accessmode='r+', indextype='int64', overwrite=False):
    """Creates an empty VarDimArray.

        Parameters
        ----------
        path : str or pathlib.Path
            Path to disk-based array directory.
        arrayiterable: iterator yielding array-like objects
            This can be a numpy array, a sequence that can be converted into a
            numpy array, or an iterator that yields such objects. The latter
            will be concatenated along the first dimension.
        dtype : dtype, optional
            The type of the `darr`. Default is 'float64'
        metadata: {None, dict}
            Dictionary with metadata to be saved in a separate JSON file. Default
            None
        accessmode : {'r', 'r+'}, default 'r'
           File access mode of the darr data. `r` means read-only, `r+` means
           read-write. `w` does not exist. To create new darr arrays, potentially
           overwriting an other one, use the `asarray` or `create_array`
           functions.
        indextype : dtype, optional
            The dtype of the index array underlying the disk-based ragged array
            format. Defaults to 'int64'. But other possibilities are int8','uint8',
            'int16', 'uint16', 'int32', 'uint32', 'int64'. This determines the
            maximum length of the ragged array, but also how compatible the
            array is with other languages.
        overwrite: <True, False>, optional
            Overwrites existing darr data if it exists. Note that a darr
            paths is a directory. If that directory contains additional files,
            these will not be removed and an OSError is raised.
            Default is `False`.

        Returns
        -------
        RaggedArray
            A Darr RaggedArray instance.

        """
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
    valuespath = bd.path.joinpath(VarDimArray._valuesdirname)
    indicesandshapespath = bd.path.joinpath(VarDimArray._indicesandshapesdirname)
    valuesda = asarray(path=valuespath, array=firstarray.flatten(), dtype=dtype,
                       accessmode='r+', overwrite=overwrite)
    firstindicesandshape = [[0, firstarray.size] + list(firstarray.shape)]
    indshapera = asraggedarray(path=indicesandshapespath,
                              arrayiterable=firstindicesandshape,
                              dtype=indextype, accessmode='r+',
                              overwrite=overwrite)
    valueslen = firstarray.size
    with valuesda._open_array(accessmode='r+') as (_, avfd), \
         indshapera._view(accessmode='r+'):
        for array in arrayiterable:
            array = np.asarray(array)
            # append subarray values to value darr array
            lenincreasevalues = valuesda._append(array.flatten(), fd=avfd)
            # append indicesshape
            starti, endi = valueslen, valueslen + lenincreasevalues
            indshape = [starti, endi] + list(array.shape)
            indshapera.append(indshape)
            valueslen += lenincreasevalues

    valuesda._update_len(lenincrease=valueslen-firstarray.size)
    valuesda._update_readmetxt()
    datainfo = {}
    datainfo['len'] = len(indshapera)
    datainfo['size'] = valuesda.size
    datainfo['numtype'] = valuesda._arrayinfo['numtype']
    datainfo['darrversion'] = Array._formatversion
    datainfo['darrobject'] = 'VarDimArray'
    bd._write_jsondict(filename=VarDimArray._arraydescrfilename,
                       d=datainfo, overwrite=overwrite)
    metadatapath = path.joinpath(Array._metadatafilename)
    if metadata is not None:
        bd._write_jsondict(filename=Array._metadatafilename,
                           d=metadata, overwrite=overwrite)
    elif metadatapath.exists():  # no metadata but file exists, remove it
        metadatapath.unlink()
    vda = VarDimArray(path=path, accessmode=accessmode)
    vda._update_readmetxt()
    return VarDimArray(path=path, accessmode=accessmode)


def create_vardimarray(path, dtype='float64', metadata=None,
                       accessmode='r+', indextype='int64', overwrite=False):
    """Creates an empty VarDimArray.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to disk-based array directory.
    dtype : dtype, optional
        The type of the `darr`. Default is 'float64'
    metadata: {None, dict}
        Dictionary with metadata to be saved in a separate JSON file. Default
        None
    accessmode : {'r', 'r+'}, default 'r'
       File access mode of the darr data. `r` means read-only, `r+` means
       read-write. `w` does not exist. To create new darr arrays, potentially
       overwriting an other one, use the `asarray` or `create_array`
       functions.
    indextype : dtype, optional
        The dtype of the index array underlying the disk-based ragged array
        format. Defaults to 'int64'. But other possibilities are int8','uint8',
        'int16', 'uint16', 'int32', 'uint32', 'int64'. This determines the
        maximum length of the ragged array, but also how compatible the
        array is with other languages.
    overwrite: <True, False>, optional
        Overwrites existing darr data if it exists. Note that a darr
        paths is a directory. If that directory contains additional files,
        these will not be removed and an OSError is raised.
        Default is `False`.

    Returns
    -------
    VarDimArray
        A Darr VarDimArray instance.

    """
    ar = np.zeros([0], dtype=dtype) # 1D array with len0
    vda = asvardimarray(path=path, arrayiterable=[ar], metadata=metadata,
                       accessmode=accessmode, indextype=indextype,
                       overwrite=overwrite)
    # the current ragged array has one element, which is an empty array
    # but we want an empty ragged array => we should get rid of the indices
    create_array(path=vda._indicesandshapes._indicespath,
                 shape=(0,2), dtype=np.int64, overwrite=True)
    vda._update_arraydescr(len=0, size=0)
    return VarDimArray(vda.path, accessmode=accessmode)

def readmetxt(vda):
    txt = wrap("NOT IMPLEMENTED YET\n")
    return txt

def readcodetxt(vda):
    txt = wrap("NOT IMPLEMENTED YET\n")
    return txt