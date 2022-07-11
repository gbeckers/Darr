from pathlib import Path
from contextlib import contextmanager

import numpy as np
from ._version import get_versions

from .array import Array, asarray, check_accessmode, create_array, delete_array
from .raggedarray import RaggedArray, asraggedarray, delete_raggedarray, create_raggedarray
from .datadir import DataDir, create_datadir
from .metadata import MetaData
from .readcodevardimarray import readcode, readcodefunc
from .utils import wrap

__all__ = ['VarDimArray', 'asvardimarray', 'create_vardimarray',
           'delete_vardimarray']


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
        arrayinfo['darrobject'] = 'VarDimArray'
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
                            "VarDimArrays, which '{}' is not".format(item))
        indicesandshape = self._indicesandshapes[item]
        index = slice(*indicesandshape[:2])
        shape = indicesandshape[2:]
        return self._values[index].reshape(shape)

    def __len__(self):
        return len(self._indicesandshapes)

    def __repr__(self):
        return f'VarDimArray ({self.narrays} variable dimension subarrays ' \
               f'({self.accessmode})'

    __str__ = __repr__

    def _update_readmetxt(self):
        txt = readmetxt(self)
        self._datadir._write_txt(self._readmefilename, txt, overwrite=True)

    def _update_arraydescr(self, **kwargs):
        self._arrayinfo.update(kwargs)
        self._datadir._write_jsondict(filename=self._arraydescrfilename,
                                      d=self._arrayinfo, overwrite=True)

    def _append(self, array, valfd, isaindfdv, isavalfd, vallen,
                isavallen):
        """Private method that appends data but does not update attributes
        and info/readme files.

        Parameters
        ----------
        array
        valfd: file descriptor
            File with array values.
        isaindfdv: file descriptor
            File with indicesandshapes array indices.
        isavalfd: file descriptor
            File with indicesandshapes array values.
        vallen: int
            The current length of the values array.
        isavallen: int
            The current length of the indicesandshapes values arrays

        Returns
        -------

        """
        array = np.asarray(array, dtype=self.dtype)
        shape = array.shape
        # append values to values array
        vlenincr = self._values._append(array.flatten(),
                                        valfd)
        # append index and shape info to indicesandshapes raggedarray
        indshape = [vallen, vallen+array.size] + list(shape)
        isavallenincr, isaindlenincr = \
            self._indicesandshapes._append(array=indshape, fdv=isavalfd,
                                           fdi=isaindfdv,
                                           vlen=isavallen)
        return (vlenincr, isavallenincr, isaindlenincr)

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
        with self.open_arrays() as ((isaindmm, isavalmm),
                                    (isaindfdv, isavalfd),
                                    (valmm, valfd)):
            vallen = self._values.shape[0]
            isavallen = self._indicesandshapes._values.shape[0]
            (vlenincr, isavallenincr, isaindlenincr) = \
                self._append(array=array, valfd=valfd, isaindfdv=isaindfdv,
                             isavalfd=isavalfd, vallen=vallen,
                             isavallen=isavallen)
        self._values._update_len(lenincrease=vlenincr)
        self._values._update_arrayinfo()
        self._values._update_readmetxt()
        self._indicesandshapes._values._update_len(lenincrease=isavallenincr)
        self._indicesandshapes._values._update_arrayinfo()
        self._indicesandshapes._values._update_readmetxt()
        self._indicesandshapes._indices._update_len(lenincrease=isaindlenincr)
        self._indicesandshapes._indices._update_arrayinfo()
        self._indicesandshapes._indices._update_readmetxt()
        self._update_arraydescr(len=len(self._indicesandshapes),
                                size=self._values.size)
        self._update_readmetxt()


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

    @contextmanager
    def open_arrays(self, accessmode=None):
        with self._indicesandshapes.open_arrays(accessmode=accessmode) as \
                ((isaindmm, isavalmm), (isavalfd, isaindfdv)), \
                self._values._open_array(accessmode=accessmode) as (valmm, valfd):
            yield (isaindmm, isavalmm), (isaindfdv, isavalfd), (valmm, valfd)

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
        with self.open_arrays() as ((isaindmm, isavalmm),
                                    (isaindfdv, isavalfd),
                                    (valmm, valfd)):
            totvlenincr = 0
            totisavallenincr = 0
            totisaindlenincr = 0
            vallen = self._values.shape[0]
            isavallen = self._indicesandshapes._values.shape[0]
            for a in arrayiterable:
                (vlenincr, isavallenincr, isaindlenincr) = \
                    self._append(array=a, valfd=valfd,
                                 isaindfdv=isaindfdv,
                                 isavalfd=isavalfd, vallen=vallen+totvlenincr,
                                 isavallen=isavallen+totisavallenincr)
                totvlenincr += vlenincr
                totisavallenincr += isavallenincr
                totisaindlenincr += isaindlenincr
        self._values._update_len(lenincrease=totvlenincr)
        self._values._update_arrayinfo()
        self._values._update_readmetxt()
        self._indicesandshapes._values._update_len(lenincrease=totisavallenincr)
        self._indicesandshapes._values._update_arrayinfo()
        self._indicesandshapes._values._update_readmetxt()
        self._indicesandshapes._indices._update_len(lenincrease=totisaindlenincr)
        self._indicesandshapes._indices._update_arrayinfo()
        self._indicesandshapes._indices._update_readmetxt()
        self._update_arraydescr(len=len(self._indicesandshapes),
                                size=self._values.size)
        self._update_readmetxt()


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
    vda.iterappend(arrayiterable)
    return vda


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
    create_raggedarray(path=vda._indicesandshapespath,
                 atom=(), dtype=np.int64, overwrite=True)
    vda._update_arraydescr(len=0, size=0)
    return VarDimArray(vda.path, accessmode=accessmode)

def readmetxt(vda):
    txt = wrap("This directory hold data for a VarDimArray, which is an "
               "experimental type of Darr array.") + ' \n\n'
    txt += wrap("A VarDimArray can be seen as a sequence of subarrays, "
                "each of which may have a variable number of dimensions that "
                "can be variable in length. In essence it is a sequence of "
                "ND-arrays that can have arbitrary shapes.") + ' \n\n'
    txt += wrap("VarDimArrays are still experimental, so an elaborate "
                "description is not yet provided. On disk, the array is saved "
                "as a combination of a Darr Array that holds the values and "
                "a Darr RaggedArray that holds information on the location "
                "and shape of each subarray in the values array.")
    return txt

def readcodetxt(vda):
    txt = wrap("NOT IMPLEMENTED YET\n")
    return txt

def delete_vardimarray(vda):
    """
    Delete Darr vardim array data from disk.

    Parameters
    ----------
    vda: RaggedArray or path to VarDimArray to be deleted.

    """
    try:
        if not isinstance(vda, VarDimArray):
            vda = VarDimArray(vda, accessmode='r+')
    except:
        raise TypeError(f"'{vda}' not recognized as a Darr vardim array")
    if not vda.accessmode == 'r+':
        raise OSError('Darr ragged array is read-only; set accessmode to '
                      '"r+" to change')
    for fn in vda._protectedfiles:
        path = vda.path.joinpath(fn)
        if path.exists() and not path.is_dir():
            path.unlink()
    delete_array(vda._values)
    delete_raggedarray(vda._indicesandshapes)
    try:
        vda._path.rmdir()
    except OSError as error:
        message = f"Error: could not fully delete Darr vardim array " \
                  f"directory " \
                  f"'{vda.path}'. It may contain additional files that are " \
                  f"not part of the darr. If so, these should be removed " \
                  f"manually."
        raise OSError(message) from error
