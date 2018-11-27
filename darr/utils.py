import hashlib
import textwrap

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
