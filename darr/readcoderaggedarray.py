from . import readcodearray


def readcodenumpymemmap(dra, varname='a'):
    rci = readcodearray.readcode(dra._indices, 'numpymemmap',
                                 filepath='indices/arrayvalues.bin',
                                 varname='i')
    rcv = readcodearray.readcode(dra._values, 'numpymemmap',
                                 filepath='values/arrayvalues.bin',
                                 varname='v')
    rcv = ''.join(rcv.splitlines(keepends=True)[1:]) # get rid of import
    rff = 'def get_subarray(seqno):\n' \
          '    starti, endi = i[seqno]\n' \
          '    return v[starti:endi]\n'
    if len(dra) > 2:
       j, position = 2, 'third'
    elif len(dra) == 2:
        j, position = 1, 'second'
    else:
        j, position = 0, 'first'
    rca = f'{varname} = get_subarray({j})  # example to read {position} ' \
          f'subarray\n'
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
    rff = 'get_subarray <- function(j){\n' \
          '    starti = i[1,j]+1  # R starts counting from 1\n' \
          '    endi = i[2,j]  # R has inclusive end index\n'
    commas = len(dra._arrayinfo['atom'])*','
    rff = f'{rff}    return (v[{commas}starti:endi])}}\n'
    rff = f"# create function to get subarrays:\n{rff}"
    if len(dra) > 2:
       j, position = 3, 'third'
    elif len(dra) == 2:
        j, position = 2, 'second'
    else:
        j, position = 1, 'first'
    rca =  f"# example to read {position} subarray:\n"
    rca = f"{rca}# get_subarray({j})\n"
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
    rci = f"% read array of indices to be used on values array:\n{rci}"
    rcv = f"% read array of values:\n{rcv}"
    if len(dra) > 2:
       j, position = 3, 'third'
    elif len(dra) == 2:
        j, position = 2, 'second'
    else:
        j, position = 1, 'first'
    rca = "% create an anonymous function that returns the j-th subarray\n" \
          "% from the values array:\n"
    dims = len(dra._arrayinfo['atom'])*':,'
    rca = f"{rca}s = @(j) v({dims}i(1,j)+1:i(2,j));\n"
    rca =  f'{rca}% example to read {position} subarray:\n' \
           f'% s({j})'
    return f'{rci}{rcv}{rca}'


readcodefunc = {
        'numpymemmap': readcodenumpymemmap,
        'matlab': readcodematlab,
        'R': readcoder
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