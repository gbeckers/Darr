from pathlib import Path
from . import readcodearray
from .readcodearray import shapeexplanationtextarray
from .utils import wrap

# Row-major: Mathematica, Numpy
# Column-major: Julia, Matlab/Octave, R, Maple, IDL/GDL

# start counting at 0: Python, IDL
# start counting at 1: Julia, Mathematica, Matlab/Octave, R, Maple,

# inclusive end index: Julia, Mathematica, Matlab/Octave, R, Maple, IDL/GDL
# non-inclusive end index: Python

def readcodedarr(dra, indicespath, valuespath):
    if len(dra) > 2:
       k, position = 2, 'third'
    elif len(dra) == 2:
        k, position = 1, 'second'
    else:
        k, position = 0, 'first'
    ct = f"import darr\n" \
         f"# path_to_data_dir is the directory that contains this README\n" \
         f"a = darr.RaggedArray(path='path_to_data_dir')\n" \
         f"# example to read {position} (k={k}) subarray:\n" \
         f"sa = a[2]\n"

    return ct


def readcodenumpymemmap(dra, indicespath, valuespath):
    rci = readcodearray.readcode(dra._indices, 'numpymemmap',
                                 varname='i',
                                 basepath=indicespath)
    rcv = readcodearray.readcode(dra._values, 'numpymemmap',
                                 varname='v',
                                 basepath=valuespath)
    rcv = ''.join(rcv.splitlines(keepends=True)[1:]) # get rid of import
    rff = 'def getsubarray(k):\n' \
          '    starti, endi = i[k]\n' \
          '    return v[starti:endi]\n'
    if len(dra) > 2:
       k, position = 2, 'third'
    elif len(dra) == 2:
        k, position = 1, 'second'
    else:
        k, position = 0, 'first'
    rca = f'# example to read {position} (k={k}) subarray:\n' \
          f'sa = getsubarray({k})\n' \

    ## the mext is never going to happen as Darr is based on memmap
    ## comment out
    # if (rci is None) or (rcv is None):
    #     return None
    # else:
    return f'{rci}{rcv}{rff}{rca}'

def readcoder(dra, indicespath, valuespath):
    # We allow for int64 index arrays, even though R is not fully compatible.
    # It will only read it correctly for positive values up to 2147483647. So
    # values arrays may not be larger in size than that.
    rci = readcodearray.readcode(dra._indices, 'R',
                                 varname='i',
                                 basepath=indicespath,
                                 ignoreint64=True)
    rcv = readcodearray.readcode(dra._values, 'R',
                                 varname='v',
                                 basepath=valuespath)
    if (rci is None) or (rcv is None):
        return None
    if dra._indices.dtype.name == 'int64':
        if dra._values.size > 2147483647: # larger than can be represented in int32
            return None
    rci = f"# read array of indices to be used on values array\n{rci}"

    rcv = f'# read array of values:\n{rcv}'
    rff = f'# create function to get subarrays:\n' \
          f'getsubarray <- function(k){{\n' \
          f'    starti <- i[1,k] + 1  # R starts counting from 1\n' \
          f'    endi <- i[2,k]        # R has inclusive end index\n'
    if len(dra.atom) == 0:
        rff += f'    if (starti > endi) {{  # subarray is empty\n' \
               f'        return (c())\n' \
               f'    }} else {{\n' \
               f'        return (v[starti:endi])\n' \
               f'    }}\n' \
               f'}}\n'
    else:
        commas = len(dra._arrayinfo['atom'])*','
        emptydim = ",".join([str(d) for d in dra.atom] + ['0'])
        rff += f'    if (starti > endi) {{\n' \
               f'        return (array(numeric(),c({emptydim}))) # empty array\n' \
               f'    }} else {{\n' \
               f'        return (v[{commas}starti:endi])\n' \
               f'    }}\n' \
               f'}}\n'
    if len(dra) > 2:
       k, position = 3, 'third'
    elif len(dra) == 2:
        k, position = 2, 'second'
    else:
        k, position = 1, 'first'
    rca =  f"# example to read {position} (k={k}) subarray:\n" \
           f"sa = getsubarray({k})\n"
    return f'{rci}{rcv}{rff}{rca}'

def readcodematlab(dra, indicespath, valuespath, varname='sa'):
    rci = readcodearray.readcode(dra._indices, 'matlab',
                                 varname='i',
                                 basepath=indicespath)
    rcv = readcodearray.readcode(dra._values, 'matlab',
                                 varname='v',
                                 basepath=valuespath)
    if (rci is None) or (rcv is None):
        return None
    numtype = dra.dtype.name
    rci = f"% read indice array, to be used on values array later:\n{rci}"
    rcv = f"% read {numtype} values array:\n{rcv}"
    if len(dra) > 2:
       k, position = 3, 'third'
    elif len(dra) == 2:
        k, position = 2, 'second'
    else:
        k, position = 1, 'first'
    dims = len(dra._arrayinfo['atom']) * ':,'
    rca = f'% create an anonymous function that returns the k-th subarray\n' \
          f'% from the values array:\n' \
          f'getsubarray = @(k) v({dims}i(1,k)+1:i(2,k));\n' \
          f'% example to read {position} (k={k}) subarray:\n' \
          f'sa = getsubarray({k});'
    return f'{rci}{rcv}{rca}\n'

# not supporting versions < 1 anymore
def readcodejulia(dra, indicespath, valuespath):
    rci = readcodearray.readcode(dra._indices, 'julia_ver1',
                                 varname='i',
                                 basepath=indicespath)
    rcv = readcodearray.readcode(dra._values, 'julia_ver1',
                                 varname='v',
                                 basepath=valuespath)
    if (rci is None) or (rcv is None):
        return None
    numtype = dra.dtype.name
    rci = f"# read indices array, to be used on values array later:\n{rci}"
    rcv = f"# read {numtype} values array:\n{rcv}"
    dims = len(dra._arrayinfo['atom']) * ':,'
    rff = f'function getsubarray(k)\n' \
          f'    starti = i[1,k]+1  # Julia starts counting from 1\n' \
          f'    endi = i[2,k]  # Julia has inclusive end index\n' \
          f'    v[{dims}starti:endi]\n' \
          f'end\n'
    rff = f"# create a function that returns the k-th subarray\n" \
          f"# from the values array:\n{rff}"
    if   len(dra) > 2:
       k, position = 3, 'third'
    elif len(dra) == 2:
        k, position = 2, 'second'
    else:
        k, position = 1, 'first'
    rca =  f'# example to read {position} (k={k}) subarray:\n' \
           f'sa = getsubarray({k})'
    return f'{rci}{rcv}{rff}{rca}\n'


def readcodemathematica(dra, indicespath, valuespath):
    numtype = dra.dtype.name
    rci = readcodearray.readcode(dra._indices, 'mathematica',
                                 varname='i',
                                 basepath=indicespath)
    rcv = readcodearray.readcode(dra._values, 'mathematica',
                                 varname='v',
                                 basepath=valuespath)
    if (rci is None) or (rcv is None):
        return None
    rci = f"(* read indices array, to be used on values array later: *)\n{rci}"
    rcv = f"(* read {numtype} values array: *)\n{rcv}"
    if   len(dra) > 2:
       k, position = 3, 'third'
    elif len(dra) == 2:
        k, position = 2, 'second'
    else:
        k, position = 1, 'first'
    rff = f'(* create a function that returns the k-th subarray\n' \
          f'   from the values array *):\n' \
          f'getsubarray[k_?IntegerQ] := \n' \
          f'    Module[{{l}},\n' \
          f'        l = k;\n' \
          f'        starti = i[[l,1]] + 1;\n' \
          f'        endi = i[[l,2]];\n' \
          f'        v[[starti;;endi]]]\n' \
          f'(* example to read {position} (k={k}) subarray: *)\n'\
          f'sa = getsubarray[{k}]\n'
    return f'{rci}{rcv}{rff}'

def readcodemaple(dra, indicespath, valuespath):
    numtype = dra.dtype.name
    rci = readcodearray.readcode(dra._indices, 'maple',
                                 varname='i',
                                 basepath=indicespath)
    rcv = readcodearray.readcode(dra._values, 'maple',
                                 varname='v',
                                 basepath=valuespath)
    if (rci is None) or (rcv is None):
        return None
    rci = f"# read indices array, to be used on values array later:\n{rci}"
    rcv = f"# read {numtype} values array:\n{rcv}"
    if   len(dra) > 2:
       k, position = 3, 'third'
    elif len(dra) == 2:
        k, position = 2, 'second'
    else:
        k, position = 1, 'first'
    dims = len(dra._arrayinfo['atom']) * '..,'
    rff = f'# create a function that returns the k-th subarray\n' \
          f'# from the values array:\n' \
          f'getsubarray := proc (k::integer);\n' \
          f'    v({dims} i(1,k) + 1 .. i(2,k));\n' \
          f'end proc;\n' \
          f'# example to read {position} (k={k}) subarray:\n'\
          f'sa = getsubarray({k});\n'
    return f'{rci}{rcv}{rff}'

# empty subarrays don't work with this method
def readcodeidl(dra, indicespath, valuespath):
    rci = readcodearray.readcode(dra._indices, 'idl',
                                 varname='i',
                                 basepath=indicespath)
    rcv = readcodearray.readcode(dra._values, 'idl',
                                 varname='v',
                                 basepath=valuespath)
    if (rci is None) or (rcv is None):
        return None
    if   len(dra) > 2:
       k, position = 2, 'third'
    elif len(dra) == 2:
        k, position = 1, 'second'
    else:
        k, position = 0, 'first'
    numtype = dra.dtype.name
    rci = f"; read indices array, to be used on values array later:\n{rci}"
    rcv = f"; read {numtype} values array:\n{rcv}"
    dims = len(dra._arrayinfo['atom']) * '*,'
    rff = f"; example to get the {position} (k={k}) subarray from the values " \
          f"array,\n"
    rca =  f'; but set k to get the subarray number you want:\n' \
           f'k = {k} \n' \
           f'; expression below sets sa variable to subarray\n' \
           f'IF i[0,k] EQ i[1,k] THEN sa=[] ELSE sa=v[{dims}i[0,k]:i[1,k]-1]\n'
    return f'{rci}{rcv}{rff}{rca}'


readcodefunc = {
        'darr' : readcodedarr,
        'idl': readcodeidl,
        'julia': readcodejulia,
        'maple': readcodemaple,
        'mathematica': readcodemathematica,
        'matlab': readcodematlab,
        'numpymemmap': readcodenumpymemmap,
        'R': readcoder,
}

def readcode(dra, language, basepath='', abspath=False):
    """Produces the code to read the Darr raggedarray `dra` in a given
    programming language.

    Parameters
    ----------
    dra: Darr raggedarray
    language: str
        A supported language, such as 'julia', 'R', or 'matlab'
    abspath: bool
        Should the paths to the data files be absolute or not? Default:
        True.
    basepath: str or pathlib.Path or None
        Path relative to which the binary array data file should be
        provided. Default: None.

    Returns
    -------
    A string with code

    """
    if language not in readcodefunc:
        raise ValueError(f"'{language}' not supported ({readcodefunc.keys()})")
    if abspath:
        ip = dra._indices.path.absolute().resolve()
        vp = dra._values.path.absolute().resolve()
    elif basepath is not None:
        ip = Path(basepath) / dra._indicesdirname
        vp = Path(basepath) / dra._valuesdirname
    else:
        ip = Path(dra._indicesdirname)
        vp = Path(dra._valuesdirname)
    return readcodefunc[language](dra=dra, indicespath=ip, valuespath=vp)


shapeindexexplanationtextraggedarray = shapeexplanationtextarray + '\n\n' +  \
wrap(f'Further, Python starts counting at 0. So the first subarray in a '
     f'ragged array has index number 0. This is also true for IDL/GDL. '
     f'However, Julia, Mathematica, Matlab/Octave, R, and Maple start '
     f'counting at 1, so the first subarray has index number 1 in these '
     f'languages. Finally, in Python indexing the end index is '
     f'non-inclusive. E.g., a[0:2] returns a[0] and a[1], but not a[2]. '
     f'However, all other languages for which reading code is provided, Julia, '
     f'Mathematica, Matlab/Octave, R, Maple, and IDL/GDL have an inclusive '
     f'end index. The reading code provided takes these differences into '
     f'account.\n')