import json
import tarfile
from pathlib import Path
from contextlib import contextmanager

from .utils import filesha256, write_jsonfile

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

    def archive(self, filepath=None, compressiontype='xz', overwrite=False):
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


def create_basedatadir(path, overwrite=False):
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
