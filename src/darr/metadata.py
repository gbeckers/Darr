from pathlib import Path
import json

from .utils import write_jsonfile, check_accessmode


class MetaData:
    """Dictionary-like access to disk based metadata.

    If there is no metadata, the metadata file does not exist, rather than
    being empty. This saves a block of disk space (potentially 4kb).

    """

    def __init__(self, path, accessmode='r', callatfilecreationordeletion=None):

        path = Path(path)
        if callatfilecreationordeletion is None:
            callatfilecreationordeletion = lambda *args: None
        self._path = path
        self._accessmode = check_accessmode(accessmode)
        self._callatfilecreationordeletion = callatfilecreationordeletion

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

    def __contains__(self, item):
        return item in self.keys()

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

    # FIXME remove overlap with popitem
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
            self._callatfilecreationordeletion()
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
            self._callatfilecreationordeletion()
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
        if metadata:
            self._callatfilecreationordeletion()

