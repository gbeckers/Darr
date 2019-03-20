"""This module contains functions to produce code in various programming
languages to read the numeric information of a Darr array.

"""

# mathematica: https://reference.wolfram.com/language/ref/BinaryRead.html
# Octave: https://octave.org/doc/v4.2.0/Binary-I_002fO.html
# Matlab: https://mathworks.com/help/matlab/ref/fread.html
# R: https://www.rdocumentation.org/packages/base/versions/3.4.3/topics/readBin
# Julia: https://docs.julialang.org/en/release-0.4/manual/integers-and- floating-point-numbers/
# Maple: https://www.maplesoft.com/support/help/maple/view.aspx?path=FileTools%2FBinary%2FRead

import numpy as np

typedescr_numpy = {'int8': 'i1',
                   'int16': 'i2',
                   'int32': 'i4',
                   'int64': 'i8',
                   'uint8': 'u1',
                   'uint16': 'u2',
                   'uint32': 'u4',
                   'uint64': 'u8',
                   'float16': 'f2',
                   'float32': 'f4',
                   'float64': 'f8',
                   'complex64': 'c8',
                   'complex128': 'c16',
                  }

endianness_numpy = {'little': '<',
                    'big': '>'}

def readcodenumpy(numtype, shape, endianness, filepath='arrayvalues.bin',
                  varname='a'):
    typedescr = f"{endianness_numpy[endianness]}{typedescr_numpy[numtype]}"
    ct = f"import numpy as np\n" \
         f"{varname} = np.fromfile('{filepath}', dtype='{typedescr}')\n"
    if len(shape) > 1:  # multidimensional, we need reshape
        ct += f"{varname} = {varname}.reshape({shape}, order='C')\n"
    return ct

def readcodenumpymemmap(numtype, shape, endianness, filepath='arrayvalues.bin',
                        varname='a'):
    typedescr = f"{endianness_numpy[endianness]}{typedescr_numpy[numtype]}"
    ct = "import numpy as np\n"
    ct += f"{varname} = np.memmap('{filepath}', dtype='{typedescr}', " \
          f"shape={shape}, order='C')\n"
    return ct

typedescr_matlab = {'int8': 'int8',
                    'int16': 'int16',
                    'int32': 'int32',
                    'int64': 'int64',
                    'uint8': 'uint8',
                    'uint16': 'uint16',
                    'uint32': 'uint32',
                    'uint64': 'uint64',
                    'float16': None,
                    'float32': 'float32',
                    'float64': 'float64',
                    'complex64': None,
                    'complex128': None,
                   }

endianness_matlab = {'little': 'ieee-le',
                     'big': 'ieee-be'}

def readcodematlab(numtype, shape, endianness,filepath='arrayvalues.bin',
                   varname='a'):
    typedescr = typedescr_matlab[numtype]
    if typedescr is None:
        return None
    endianness = endianness_matlab[endianness]
    shape = list(shape)[::-1]  # darr is always C order, Matlab is F order
    size = np.product(shape)
    ndim = len(shape)
    ct = f"fileid = fopen('{filepath}');\n"
    if ndim == 1:
        ct += f"{varname} = fread(fileid, {size}, '*{typedescr}', '{endianness}');\n"
    elif ndim == 2:
        ct += f"{varname} = fread(fileid, {shape}, '*{typedescr}', " \
              f"'{endianness}');\n"
    else:  # ndim > 2, we need reshape to get multidimensional array
        ct += f"{varname} = reshape(fread(fileid, {size}, '*{typedescr}', " \
              f"'{endianness}'), {shape});\n"
    return ct + "fclose(fileid);\n"


typedescr_r = {'int8': ('integer()', 1, 'TRUE'),
               'int16': ('integer()', 2, 'TRUE'),
               'int32': ('integer()', 4, 'TRUE'),
               'int64': ('integer()', 8, 'TRUE'),
               'uint8': ('integer()', 1, 'FALSE'),
               'uint16': ('integer()', 2, 'FALSE'),
               'uint32': ('integer()', 4, 'FALSE'),
               'uint64': ('integer()', 8, 'FALSE'),
               'float16': ('numeric()', 2, 'TRUE'),
               'float32': ('numeric()', 4, 'TRUE'),
               'float64': ('numeric()', 8, 'TRUE'),
               'complex64': None,
               'complex128': ('complex()', 16, 'TRUE'),
              }

endianness_r = {'little': 'little',
                'big': 'big'}

def readcoder(numtype, shape, endianness, filepath='arrayvalues.bin',
              varname='a'):
    typedescr = typedescr_r[numtype]
    if typedescr is None:
        return None
    endianness = endianness_r[endianness]
    what, size, signed = typedescr
    shape = shape[::-1]  # darr is always C order, R is F order
    n = np.product(shape)
    ct = f'fileid = file("{filepath}", "rb")\n' \
         f'{varname} = readBin(con=fileid, what={what}, n={n}, size={size}, ' \
         f'signed={signed}, endian="{endianness}")\n'
    if len(shape) > 1:
        ct += f'{varname} = array(data={varname}, dim=c{shape}, ' \
            f'dimnames=NULL)\n'
    return ct + 'close(fileid)\n'


typedescr_julia = {'int8': 'Int8',
                   'int16': 'Int16',
                   'int32': 'Int32',
                   'int64': 'Int64',
                   'uint8': 'UInt8',
                   'uint16': 'UInt16',
                   'uint32': 'UInt32',
                   'uint64': 'UInt64',
                   'float16': 'Float16',
                   'float32': 'Float32',
                   'float64': 'Float64',
                   'complex64': 'Complex{Float32}',
                   'complex128': 'Complex{Float64}',
                  }

endianness_julia = {'little': 'ltoh',
                    'big': 'ntoh'}

def readcodejulia0(numtype, shape, endianness, filepath='arrayvalues.bin',
                   varname='a'):
    # this does not work if numtype is complex and byteorder is different on
    # reading machine, will generate an error, so we accept this.
    typedescr = typedescr_julia[numtype]
    endianness = endianness_julia[endianness]
    shape = shape[::-1]  # darr is always C order, Julia is F order
    return f'fileid = open("{filepath}","r");\n' \
           f'{varname} = map({endianness}, read(fileid, {typedescr}, {shape}));\n' \
           f'close(fileid);\n'

def readcodejulia1(numtype, shape, endianness, filepath='arrayvalues.bin',
                   varname='a'):
    # this does not work if numtype is complex and byteorder is different on
    # reading machine, will generate an error, so we accept this.
    typedescr = typedescr_julia[numtype]
    endianness = endianness_julia[endianness]
    shape = shape[::-1]  # darr is always C order, Julia is F order
    dimstr = str(shape)[1:-1]
    if dimstr.endswith(','):
        dimstr = dimstr[:-1]
    return f'fileid = open("{filepath}","r");\n' \
           f'{varname} = map({endianness}, read!(fileid, Array{{{typedescr}}}(undef, {dimstr})));\n' \
           f'close(fileid);\n'

typedescr_idl = {'int8': None,
                 'int16': 2,
                 'int32': 3,
                 'int64': 14,
                 'uint8': 1,
                 'uint16': 12,
                 'uint32': 13,
                 'uint64': 15,
                 'float16': None,
                 'float32': 4,
                 'float64': 5,
                 'complex64': 6,
                 'complex128': 9,
                }

endianness_idl = {'little': 'little',
                  'big': 'big'}

def readcodeidl(numtype, shape, endianness, filepath='arrayvalues.bin',
                varname='a'):
    typedescr = typedescr_idl[numtype]
    endianness = endianness_idl[endianness]
    if typedescr is None:
        return None
    shape = list(shape[::-1])
    return f'{varname} = read_binary("{filepath}", data_type={typedescr}, ' \
           f'data_dims={shape}, endian="{endianness}")\n'

typedescr_mathematica = {'int8': 'Integer8',
                        'int16': 'Integer16',
                        'int32': 'Integer32',
                        'int64': 'Integer64',
                        'uint8': 'UnsignedInteger8',
                        'uint16': 'UnsignedInteger16',
                        'uint32': 'UnsignedInteger32',
                        'uint64': 'UnsignedInteger64',
                        'float16': None,
                        'float32': 'Real32',
                        'float64': 'Real64',
                        'complex64': 'Complex64',
                        'complex128': 'Complex128',
                       }

endianness_mathematica = {'little': '-1',
                          'big': '+1'}

def readcodemathematica(numtype, shape, endianness,
                        filepath='arrayvalues.bin', varname='a'):
    typedescr = typedescr_mathematica[numtype]
    endianness = endianness_mathematica[endianness]
    if typedescr is None:
        return None
    dimstr = str(shape)[1:-1]
    if dimstr.endswith(','):
        dimstr = dimstr[:-1]
    dimstr = '{' + dimstr + '}'
    return f'{varname} = BinaryReadList["{filepath}", "{typedescr}", ' \
           f'ByteOrdering -> {endianness}];\n' \
           f'{varname} = ArrayReshape[{varname}, {dimstr}];\n'

typedescr_maple = {'int8': 'integer[1]',
                   'int16': 'integer[2]',
                   'int32': 'integer[4]',
                   'int64': 'integer[8]',
                   'uint8': None,
                   'uint16': None,
                   'uint32': None,
                   'uint64': None,
                   'float16': None,
                   'float32': 'float[4]',
                   'float64': 'float[8]',
                   'complex64': None,
                   'complex128': None,
                  }

endianness_maple = {'little': 'little',
                    'big': 'big'}

def readcodemaple(numtype, shape, endianness, filepath='arrayvalues.bin',
                  varname='a'):
    typedescr = typedescr_maple[numtype]
    endianness = endianness_maple[endianness]
    if typedescr is None:
        return None
    ct = f'{varname} := FileTools[Binary][Read]("{filepath}", {typedescr}, ' \
         f'byteorder={endianness}, output=Array);\n'
    ndim = len(shape)
    if ndim > 1:
        shape = list(shape[::-1])
        ct += f'{varname} := ArrayTools[Reshape]({varname}, {shape});\n'
    return ct


readcodefunc = {
        'idl': readcodeidl,
        'julia_ver0': readcodejulia0,
        'julia_ver1': readcodejulia1,
        'mathematica': readcodemathematica,
        'matlab': readcodematlab,
        'maple': readcodemaple,
        'numpy': readcodenumpy,
        'numpymemmap': readcodenumpymemmap,
        'R': readcoder,
}


def readcode(da, language, filepath='arrayvalues.bin', varname='a'):
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
    numtype = d['numtype']
    shape = d['shape']
    endianness = d['byteorder']
    return readcodefunc[language](numtype=numtype, shape=shape,
                                  endianness=endianness, filepath=filepath,
                                  varname=varname)


def promptify_codetxt(codetxt, prompt=">>> "):
    return "\n".join([f"{prompt}{l}" for l in codetxt.splitlines()]) + '\n'
