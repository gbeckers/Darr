import hashlib
import textwrap
import json
import numpy as np
from pathlib import Path
from functools import reduce
from operator import mul
import os
import shutil
import tempfile as tf
from contextlib import contextmanager

# believe it or not Python <3.8 does not has such a function
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
        with open(path, 'w', encoding='utf-8') as fp:
            fp.write(json_string)


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
    with open(filepath, 'rb') as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)
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
