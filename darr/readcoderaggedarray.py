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
    return f'{rci}{rcv}{rff}{rca}'


def readcoder(dra, varname='a'):
    rci = readcodearray.readcode(dra._indices, 'R',
                                 filepath='indices/arrayvalues.bin',
                                 varname='i')
    rcv = readcodearray.readcode(dra._values, 'R',
                                 filepath='values/arrayvalues.bin',
                                 varname='v')
    corindex = "i[1,] = i[1,] + 1  # adjust index, R starts counting at 1\n"

    if len(dra) > 2:
       j, position = 3, 'third'
    elif len(dra) == 2:
        j, position = 2, 'second'
    else:
        j, position = 1, 'first'
    rca = f'{varname} = v[i[1,{j}]:i[2,{j}]]  # example to read {position} ' \
        f'subarray\n'
    return f'{rci}{rcv}{corindex}{rca}'



readcodefunc = {
        'numpymemmap': readcodenumpymemmap,
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