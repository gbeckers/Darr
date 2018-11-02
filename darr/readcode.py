"""This module contains functions to produce code in various programming
languages to read the numeric information of a Darr array.

"""

import numpy as np
from .numtype import numtypes, endiannesstypes

def readcodenumpy(typedescr, shape, arrayorder, **kwargs):
    ct = f"import numpy as np\n" \
         f"a = np.fromfile('arrayvalues.bin', dtype='{typedescr}')\n"
    if len(shape) > 1:  # multidimensional, we need reshape
        ct += f"a = a.reshape({shape}, order='{arrayorder}')\n"
    return ct


def readcodenumpymemmap(typedescr, shape, arrayorder, **kwargs):
    ct = "import numpy as np\n"
    ct += f"a = np.memmap('arrayvalues.bin', dtype='{typedescr}', " \
          f"shape={shape}, order='{arrayorder}')\n"
    return ct


def readcodematlab(typedescr, shape, endianness, **kwargs):
    shape = list(shape)[::-1]  # darr is always C order, Matlab is F order
    size = np.product(shape)
    ndim = len(shape)
    ct = "fileid = fopen('arrayvalues.bin');\n"
    if ndim == 1:
        ct += f"a = fread(fileid, {size}, '*{typedescr}', '{endianness}');\n"
    elif ndim == 2:
        ct += f"a = fread(fileid, {shape}, '*{typedescr}', " \
              f"'{endianness}');\n"
    else:  # ndim > 2, we need reshape to get multidimensional array
        ct += f"a = reshape(fread(fileid, {size}, '*{typedescr}', " \
              f"'{endianness}'), {shape});\n"
    return ct + "fclose(fileid);\n"


def readcoder(typedescr, shape, endianness, **kwargs):
    # typedecr is a dict, with 'what', 'size' and 'n' keys
    shape = shape[::-1]  # darr is always C order, R is F order
    n = np.product(shape)
    ct = 'fileid = file("arrayvalues.bin", "rb")\n' \
         'a = readBin(con=fileid, what={what}, n={n}, size={size}, ' \
         'endian="{endianness}")\n'.format(endianness=endianness, n=n,
                                           **typedescr)
    if len(shape) > 1:
        ct += f'a = array(data=a, dim=c{shape}, dimnames=NULL)\n'
    return ct + 'close(fileid)\n'


def readcodejulia(typedescr, shape, endianness, **kwargs):
    # this does not work if numtype is complex and byteorder is different on
    # reading machine, will generate an error, so we accept this.
    shape = shape[::-1]  # darr is always C order, Julia is F order
    return f'fileid = open("arrayvalues.bin","r");\n' \
           f'a = map({endianness}, read(fileid, {typedescr}, {shape}));\n' \
           f'close(fileid);\n'


def readcodeidl(typedescr, shape, endianness, **kwargs):
    shape = list(shape[::-1])
    return f'a = read_binary("arrayvalues.bin", data_type={typedescr}, ' \
           f'data_dims={shape}, endian="{endianness}")\n'


def readcodemathematica(typedescr, shape, endianness, **kwargs):
    dimstr = str(shape)[1:-1]
    if dimstr.endswith(','):
        dimstr = dimstr[:-1]
    dimstr = '{' + dimstr + '}'
    return f'a = BinaryReadList["arrayvalues.bin", "{typedescr}", ' \
           f'ByteOrdering -> {endianness}];\n' \
           f'a = ArrayReshape[a, {dimstr}];\n'

def readcodemaple(typedescr, shape, endianness, **kwargs):
    ct = f'a := FileTools[Binary][Read]("arrayvalues.bin", {typedescr}, ' \
         f'byteorder={endianness}, output=Array);\n'
    ndim = len(shape)
    if ndim > 1:
        shape = list(shape[::-1])
        ct += f'a := ArrayTools[Reshape](a, {shape});\n'
    return ct


readcodefunc = {
        'idl': readcodeidl,
        'julia': readcodejulia,
        'mathematica': readcodemathematica,
        'matlab': readcodematlab,
        'maple': readcodemaple,
        'numpy': readcodenumpy,
        'numpymemmap': readcodenumpymemmap,
        'R': readcoder,
}


def readcode(da, language):
    """Produces the code to read the Darr array `da` in a given programming
    language.

    Parameters
    ----------
    da: Darr array
    language: str
        A supported language, such as 'julia', 'R', or 'matlab'

    Returns
    -------
    A string with code

    """
    d = da._arrayinfo
    if language not in readcodefunc:
        raise ValueError(f"'{language}' not supported ({readcodefunc.keys()})")
    kwargs = {}
    if 'numpy' in language:
        kwargs['typedescr'] = d['dtypedescr']
    else:
        kwargs['typedescr'] = numtypes[d['numtype']][language]
    kwargs['shape'] = d['shape']
    byteorder = d['byteorder']
    kwargs['endianness'] = endiannesstypes[byteorder][language]
    kwargs['arrayorder'] = d['arrayorder']
    if kwargs['typedescr'] is None:
        return None
    else:
        return readcodefunc[language](**kwargs)


def promptify_codetxt(codetxt, prompt=">>> "):
    return "\n".join([f"{prompt}{l}" for l in codetxt.splitlines()]) + '\n'
