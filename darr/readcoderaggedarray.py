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
    rff = 'get_subarray <- function(seqno){\n' \
          '    starti = i[seqno,1] + 1  # R starts counting from 1\n' \
          '    endi = i[seqno,2]  # R has inclusive end index\n' \
          '    return (v[,starti:endi])\n' \
          '}\n'
    if len(dra) > 2:
       j, position = 3, 'third'
    elif len(dra) == 2:
        j, position = 2, 'second'
    else:
        j, position = 1, 'first'
    rca = f'{varname} = get_subarray({j})  # example to read {position} ' \
          f'subarray\n'
    if (rci is None) or (rcv is None):
        return None
    else:
        return f'{rci}{rcv}{rff}{rca}'

def readcodematlab(dra, varname='a'):
    rci = readcodearray.readcode(dra._indices, 'matlab',
                                 filepath='indices/arrayvalues.bin',
                                 varname='i')
    rcv = readcodearray.readcode(dra._values, 'matlab',
                                 filepath='values/arrayvalues.bin',
                                 varname='v')
    if len(dra) > 2:
       j, position = 3, 'third'
    elif len(dra) == 2:
        j, position = 2, 'second'
    else:
        j, position = 1, 'first'
    rca = f'# example to read {position} subarray\n' \
          f'startindex = i(1,{j}) + 1;  # matlab starts counting from 1\n' \
          f'endindex = i(2,{j});  # matlab has inclusive end index\n' \
          f'{varname} = v(:,startindex:endindex);'
    if (rci is None) or (rcv is None):
        return None
    else:
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