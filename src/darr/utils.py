import hashlib
import textwrap
import json
import numpy as np
import time
import os
from pathlib import Path
from functools import reduce
from operator import mul
import shutil
import tempfile as tf
from contextlib import contextmanager

# believe it or not Python <3.8 does not have such a function
# and numpy.product returns int32 by default (!) causing disaster
# when calculating the size of large files
def product(iterable):
    return reduce(mul, iterable, 1)


def check_accessmode(accessmode, validmodes=('r', 'r+'), makebinary=False):
    if accessmode not in validmodes:
        raise ValueError(f"Mode should be one of {validmodes}, not "
                         f"'{accessmode}'")
    if makebinary:
        accessmode += 'b'
    return accessmode


class DDJSONEncoder(json.JSONEncoder):
    """This JSON encoder fixes the problem that numpy objects aren't
    serialized to JSON with the json library default JSONEncode. Since data
    often involves numpy, and many scientific libraries produce numpy objects,
    we convert these silently to something that is a Python primitive type

    """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.datetime64):
            return str(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif hasattr(obj, 'decode'):
            return obj.decode("utf-8")
        else:
            return super(DDJSONEncoder, self).default(obj)


def write_jsonfile(path, data, sort_keys=True, indent=4, ensure_ascii=True,
                   skipkeys=False, cls=None, overwrite=False):
    path = Path(path)
    if cls is None:
        cls = DDJSONEncoder
    if path.exists() and not overwrite:
        raise OSError(f"'{path}' exists, use 'overwrite' argument")
    try:
        json_string = json.dumps(data, sort_keys=sort_keys, skipkeys=skipkeys,
                                 ensure_ascii=ensure_ascii, indent=indent,
                                 cls=cls)
    except TypeError:
        s = f"Unable to serialize the metadata to JSON: {data}.\n" \
            f"Use character strings as dictionary keys, and only " \
            f"character strings, numbers, booleans, None, lists, " \
            f"and dictionaries as objects."
        raise TypeError(s)
    else:
        # utf-8 is ascii compatible
        if waituntilfileisfree(path):
            with open(path, 'w', encoding='utf-8') as fp:
                fp.write(json_string)
        else:
            raise PermissionError(f"Unable to write to '{path}'")


def fit_frames(totallen, chunklen, steplen=None):
    """
    Calculates how many frames of 'chunklen' fit in 'totallen',
    given a step size of 'steplen'. This is intended for discrete cases (
    i.e. all lengths are integer numbers. Floats that can safely be casted
    to integers are silently allowed as input).

    Parameters
    ----------
    totallen: int
        Size of total. Must be 0 or larger.
    chunklen: int
        Size of frame. Must be 1 or larger.
    steplen: int
        Step size, defaults to chunksize (i.e. no overlap). Must be 1 or larger

    """

    if ((totallen % 1) != 0) or (totallen < 0):
        raise ValueError(f"invalid totalsize ({totallen})")
    if ((chunklen % 1) != 0) or (chunklen <= 0):
        raise ValueError(f"invalid chunklen ({chunklen})")
    if chunklen > totallen:
        return 0, 0, int(totallen)
    if steplen is None:
        steplen = chunklen
    else:
        if ((steplen % 1) != 0) or (steplen <= 0):
            raise ValueError("invalid stepsize")
    totallen = int(totallen)
    chunklen = int(chunklen)
    steplen = int(steplen)
    nchunks = ((totallen - chunklen) // steplen) + 1
    newsize = nchunks * steplen + (chunklen - steplen)
    remainder = totallen - newsize
    return nchunks, newsize, remainder

def filesha256(filepath, blocksize=2 ** 20):
    """Compute the checksum of a file."""
    m = hashlib.sha256()
    if waituntilfileisfree(filepath):
        with open(filepath, 'rb') as f:
            while True:
                buf = f.read(blocksize)
                if not buf:
                    break
                m.update(buf)
    else:
        raise PermissionError(f"Unable to read from '{filepath}'")   
    return m.hexdigest()

def wrap(s):
    return textwrap.fill(s, width=78, replace_whitespace=False)



#TODO avoid double code in next two functions; and do we really need both
# after switching to shutil for removinf dirtree?
@contextmanager
def tempdir(dirname='.', keep=False, report=False):
    """Yields a temporary directory which is removed when context is closed."""
    try:
        tempdirname = tf.mkdtemp(dir=dirname)
        if report:
            print('created tempdir {}'.format(tempdirname))
        yield Path(tempdirname)
    except:
        raise
    finally:
        if not keep:
            shutil.rmtree(tempdirname)
        if report:
            if keep:
                verb = 'kept'
            else:
                verb = 'removed'
            print(f'{verb} temporary directory {tempdirname}')

@contextmanager
def tempdirfile(dirname=None, keep=False, report=False):
    """Yields a filename "tempfile" in a temporary directory which is
    removed when context is closed. Note that the directory is created,
    but the file "tempfile" not."""
    tempdirname = None
    try:
        tempdirname = tf.mkdtemp(dir=dirname)
        if report:
            print(f'created temporary directory {tempdirname}')
        tempfilename = Path(tempdirname) / "tempfile"
        yield tempfilename
    except:
        raise
    finally:
        if not keep:
            shutil.rmtree(tempdirname)
        if report:
            if keep:
                verb = 'kept'
            else:
                verb = 'removed'
            print(f'{verb} temporary directory {tempdirname}')




def waituntilfileisfree(path, timeout=10, interval=0.5):
    """
    Waits until a file is free for access or a specified timeout is reached.

    This function repeatedly attempts to open a file in append mode, checking if it is
    locked or in use by another process. If the file becomes available, the function
    returns `True`. If the specified timeout duration is exceeded without the file
    becoming available, the function returns `False`. The check intervals can be
    configured using the `interval` parameter.

    Parameters
    ----------
    path : str
        The file path to check for availability.
    timeout : float, optional, default=10
        The maximum time (in seconds) to wait for the file to become available.
    interval : float, optional, default=0.5
        The time (in seconds) to wait between successive attempts to access the file.

    Returns
    -------
    bool
        Returns `True` if the file becomes available for access within the specified
        timeout duration, otherwise `False`.
    """
    start_time = time.time()
    while True:
        try:
            with open(path, 'a'):
                return True  # File is available
        except PermissionError:
            if time.time() - start_time > timeout:
                return False  # Timeout exceeded
            time.sleep(interval)


def compare_versionstrings(v1, v2):
    """Compare two version strings."""
    parts1 = [int(p) for p in v1.split('.')]
    parts2 = [int(p) for p in v2.split('.')]

    # Normalize length by padding with zeros
    max_len = max(len(parts1), len(parts2))
    parts1 += [0] * (max_len - len(parts1))
    parts2 += [0] * (max_len - len(parts2))

    # Compare parts
    for p1, p2 in zip(parts1, parts2):
        if p1 < p2:
            return -1  # v1 < v2
        elif p1 > p2:
            return 1  # v1 > v2
    return 0  # equal
