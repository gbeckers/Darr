import hashlib
import textwrap

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
    return textwrap.fill(s, width=98, replace_whitespace=False)
