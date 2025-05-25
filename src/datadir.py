import json
import tarfile
import shutil
import numpy as np
from pathlib import Path
from contextlib import contextmanager

from .utils import filesha256, write_jsonfile

class DataDir(object):
    """A directory for managing data. Has methods for reading
    and writing json data, and text data.

    Parameters
    ----------
    path: str or pathlib.Path
    protectedpaths: sequence | None
      Sequence of paths that should be considered part of the data,
      and that will not be changed using the normal methods of DataDir.
      Default: None.

    """

    def __init__(self, path, protectedpaths=None):
        path = Path(path)
        if not path.exists():
            raise OSError(f"'{path}' does not exist")
        self._path = path
        if protectedpaths is None:
            protectedpaths = set()
        self._protectedpaths = set(protectedpaths)

    @property
    def path(self):
        return self._path

    @property
    def protectedfiles(self):
        """Files that methods will not overwrite"""
        return self._protectedpaths

    @property
    def sha256(self):
        """Checksums (sha256) of files."""
        return self.sha256checksums()

    def __repr__(self):
        return f'DataDir at "{self._path}"'

    __str__ = __repr__

    def read_jsonfile(self, filename):
        path = self._path.joinpath(filename)
        with open(path, 'r') as fp:
            return json.load(fp)

    def _write_jsonfile(self, filename, data, sort_keys=True,
                        skipkeys=False, indent=4, cls=None, overwrite=False):
        path = self._path.joinpath(filename)
        write_jsonfile(path, data=data, sort_keys=sort_keys,
                       skipkeys=skipkeys, indent=indent,
                       ensure_ascii=True, cls=cls, overwrite=overwrite)

    def write_jsonfile(self, filename, data, sort_keys=True,
                       skipkeys=False, indent=4, overwrite=False):
        self._check_writeprotected(filename=filename, accessmode='w')
        self._write_jsonfile(filename=filename, data=data,
                             sort_keys=sort_keys, skipkeys=skipkeys,
                             indent=indent,
                             overwrite=overwrite)

    def read_jsondict(self, filename, requiredkeys=None):
        d = self.read_jsonfile(filename=filename)
        if not isinstance(d, dict):
            raise TypeError('json data must be a dictionary')
        if requiredkeys is not None:
            keys = set(d.keys())
            requiredkeys = set(requiredkeys)
            if not requiredkeys.issubset(keys):
                difference = requiredkeys.difference(keys)
                raise ValueError(f"required keys {difference} not present")
        return d

    def _write_jsondict(self, filename, d, skipkeys=False,
                        cls=None, overwrite=False):
        if not isinstance(d, dict):
            raise TypeError('json data must be a dictionary')
        return self._write_jsonfile(filename=filename, data=d,
                                    skipkeys=skipkeys, cls=cls,
                                    overwrite=overwrite)

    def write_jsondict(self, filename, d, skipkeys=False,
                       cls=None, overwrite=False):
        self._check_writeprotected(filename=filename, accessmode='w')
        return self._write_jsondict(filename=filename, d=d, skipkeys=skipkeys,
                                    cls=cls, overwrite=overwrite)

    def _update_jsondict(self, filename, *args, **kwargs):
        d2 = self.read_jsondict(filename)
        d2.update(*args, **kwargs)
        self._write_jsondict(filename=filename, d=d2, overwrite=True)
        return d2

    def update_jsondict(self, filename, *args, **kwargs):
        self._check_writeprotected(filename=filename, accessmode='w')
        return self._update_jsondict(filename, *args, **kwargs)

    def _write_txt(self, filename, text, overwrite=False):
        path = self._path.joinpath(filename)
        if not path.exists() or overwrite:
            # utf-8 is ascii-compatible
            with open(path, 'w', encoding='utf-8') as f:
                f.write(text)
                f.flush()
        else:
            raise OSError(f'File "{path}" exists, use `overwrite` parameter"')

    def write_txt(self, filename, text, overwrite=False):
        self._check_writeprotected(filename=filename, accessmode='w')
        self._write_txt(filename, text=text, overwrite=overwrite)

    def read_txt(self, filename):
        path = self._path.joinpath(filename)
        with open(path, 'r') as fp:
            return fp.read()

    def sha256checksums(self):
        checksums = {}
        for filepath in self.path.iterdir():
            checksums[str(filepath)] = filesha256(filepath)
        return checksums

    def _delete_files(self, filenames):
        for filename in filenames:
            path = self.path.joinpath(filename)
            if path.exists():
                path.unlink()

    def delete_files(self, filenames):
        for filename in filenames:
            self._check_writeprotected(filename=filename, accessmode='w')
        return self._delete_files(filenames=filenames)

    def _check_writeprotected(self, filename, accessmode):
        if accessmode != 'r' and filename in self._protectedpaths:
            raise OSError(f'Cannot modify protected file "{filename}"')

    # FIXME overwrite parameter?
    @contextmanager
    def open_file(self, filename, accessmode='r', buffering=-1, encoding=None,
                  errors=None, newline=None, closefd=True):
        """Open a file in the darr array directory and yield a file object.
        Protected files, i.e. those that are part of the darr array may only be
        opened for reading (mode='r').

        This method is a thin wrapper of the that of the Python 'open'
        function. The parameters are therefore the same.

        Examples
        --------
        >>> with d.open_file('notes.txt', 'a') as f:
        ...     n = f.write('excellent recording\\n')

        """
        self._check_writeprotected(filename=filename, accessmode=accessmode)
        filepath = self.path / filename
        with open(file=filepath, mode=accessmode, buffering=buffering,
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
            tf.add(self.path, arcname=self.path.name)
        return Path(filepath)

    # TODO tests for this function
    def copy(self, dst):
        if Path(dst).exists():
            raise OSError(f"'{dst}' already exist")
        p = shutil.copytree(self.path, dst, symlinks=False, ignore=None,
                            ignore_dangling_symlinks=False,
                            dirs_exist_ok=False)
        return DataDir(p)


def create_datadir(path, overwrite=False):
    """
    Parameters
    ----------
    path: str or pathlib.Path
    overwrite: True or False, optional
        Default False

    Returns
    -------
    DataDir

    """
    path = Path(path)
    if path.exists() and not overwrite:
        raise OSError(f"'{path}' directory already exists; "
                      f"use `overwrite` parameter to overwrite")
    else:
        if not path.exists():
            Path.mkdir(path)
            path = Path(path)
    return DataDir(path)
