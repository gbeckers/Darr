from . import readcodearray

# Row-major: Mathematica, Numpy
# Column-major: Julia, Matlab, R

def readcodenumpymemmap(dra, varname='a'):
    rci = readcodearray.readcode(dra._indices, 'numpymemmap',
                                 filepath='indices/arrayvalues.bin',
                                 varname='i')
    rcv = readcodearray.readcode(dra._values, 'numpymemmap',
                                 filepath='values/arrayvalues.bin',
                                 varname='v')
    rcv = ''.join(rcv.splitlines(keepends=True)[1:]) # get rid of import
    rff = 'def get_subarray(k):\n' \
          '    starti, endi = i[k]\n' \
          '    return v[starti:endi]\n'
    if len(dra) > 2:
       k, position = 2, 'third'
    elif len(dra) == 2:
        k, position = 1, 'second'
    else:
        k, position = 0, 'first'
    rca = f'# {varname} = get_subarray({k})  # example to read {position} ' \
          f'(k={k}) subarray\n'
    ## the mext is never going to happen as Darr is based on memmap
    ## comment out
    # if (rci is None) or (rcv is None):
    #     return None
    # else:
    return f'{rci}{rcv}{rff}{rca}'


def readcoder(dra, varname='a'):
    rci = readcodearray.readcode(dra._indices, 'R',
                                 filepath='indices/arrayvalues.bin',
                                 varname='i')
    rcv = readcodearray.readcode(dra._values, 'R',
                                 filepath='values/arrayvalues.bin',
                                 varname='v')
    if (rci is None) or (rcv is None):
        return None
    rci = f"# read array of indices to be used on values array\n{rci}"

    rcv = f"# read array of values:\n{rcv}"
    rff = 'get_subarray <- function(k){\n' \
          '    starti = i[1,k]+1  # R starts counting from 1\n' \
          '    endi = i[2,k]  # R has inclusive end index\n'
    commas = len(dra._arrayinfo['atom'])*','
    rff = f'{rff}    return (v[{commas}starti:endi])}}\n'
    rff = f"# create function to get subarrays:\n{rff}"
    if len(dra) > 2:
       k, position = 3, 'third'
    elif len(dra) == 2:
        k, position = 2, 'second'
    else:
        k, position = 1, 'first'
    rca =  f"# example to read {position} (k={k}) subarray:\n"
    rca = f"{rca}# {varname} = get_subarray({k})\n"
    return f'{rci}{rcv}{rff}{rca}'

def readcodematlab(dra, varname='a'):
    rci = readcodearray.readcode(dra._indices, 'matlab',
                                 filepath='indices/arrayvalues.bin',
                                 varname='i')
    rcv = readcodearray.readcode(dra._values, 'matlab',
                                 filepath='values/arrayvalues.bin',
                                 varname='v')
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
    rca = "% create an anonymous function that returns the k-th subarray\n" \
          "% from the values array:\n"
    dims = len(dra._arrayinfo['atom'])*':,'
    rca = f"{rca}get_subarray = @(k) v({dims}i(1,k)+1:i(2,k));\n"
    rca =  f'{rca}% example to read {position} (k={k}) subarray:\n' \
           f'% {varname} = get_subarray({k});'
    return f'{rci}{rcv}{rca}\n'

# not supporting versions < 1 anymore
def readcodejulia(dra, varname='a'):
    rci = readcodearray.readcode(dra._indices, 'julia_ver1',
                                 filepath='indices/arrayvalues.bin',
                                 varname='i')
    rcv = readcodearray.readcode(dra._values, 'julia_ver1',
                                 filepath='values/arrayvalues.bin',
                                 varname='v')
    if (rci is None) or (rcv is None):
        return None
    numtype = dra.dtype.name
    rci = f"# read indices array, to be used on values array later:\n{rci}"
    rcv = f"# read {numtype} values array:\n{rcv}"
    dims = len(dra._arrayinfo['atom']) * ':,'
    rff = f'function get_subarray(k)\n' \
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
           f'# {varname} = get_subarray({k})'
    return f'{rci}{rcv}{rff}{rca}\n'


def readcodemathematica(dra, varname='a'):
    numtype = dra.dtype.name
    rci = readcodearray.readcode(dra._indices, 'mathematica',
                                 filepath='indices/arrayvalues.bin',
                                 varname='i')
    rci = f"(* read indices array, to be used on values array later: *)\n{rci}"
    rcv = readcodearray.readcode(dra._values, 'mathematica',
                                 filepath='values/arrayvalues.bin',
                                 varname='v')
    rcv = f"(* read {numtype} values array: *)\n{rcv}"
    if (rci is None) or (rcv is None):
        return None
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
          f'(* {varname} = getsubarray[{k}] *)\n'
    return f'{rci}{rcv}{rff}\n'


readcodefunc = {
        'julia': readcodejulia,
        'mathematica': readcodemathematica,
        'matlab': readcodematlab,
        'numpymemmap': readcodenumpymemmap,
        'R': readcoder,
}

def readcode(dra, language, varname='a'):
    """Produces the code to read the Darr raggedarray `dra` in a given
    programming language.

    Parameters
    ----------
    dra: Darr raggedarray
    language: str
        A supported language, such as 'julia', 'R', or 'matlab'

    Returns
    -------
    A string with code

    """
    if language not in readcodefunc:
        raise ValueError(f"'{language}' not supported ({readcodefunc.keys()})")
    return readcodefunc[language](dra=dra, varname=varname)