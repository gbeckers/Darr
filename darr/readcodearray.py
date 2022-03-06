"""This module contains functions to produce code in various programming
languages to read the numeric information of a Darr array.

"""
# Reading binary files:
# ---------------------
# mathematica: https://reference.wolfram.com/language/ref/BinaryRead.html
# Octave: https://octave.org/doc/v4.2.0/Binary-I_002fO.html
# Matlab: https://mathworks.com/help/matlab/ref/fread.html
# R: https://www.rdocumentation.org/packages/base/versions/3.4.3/topics/readBin
# Julia: https://docs.julialang.org/en/release-0.4/manual/integers-and- floating-point-numbers/
# Maple: https://www.maplesoft.com/support/help/maple/view.aspx?path=FileTools%2FBinary%2FRead

# Row- vs column major:
# ---------------------
# IDL https://www.l3harrisgeospatial.com/docs/columns__rows__and_array.html
# Matlab https://nl.mathworks.com/help/coder/ug/what-are-column-major-and-row-major-representation-1.html


# Row-major: Mathematica, Numpy
# Column-major: Julia, Matlab/Octave, R, Maple, IDL/GDL

# Considerations
# --------------
# Matlab has memmapfile, but it will only read correctly if endianness of
# data is the same as that of the host system, which we can't guarantee.
# Same for Julia. Workaround code possible?

import numpy as np
from pathlib import Path
from .utils import wrap

def readcodedarr(numtype, shape, endianness, filepath='path_to_data_dir',
                  varname='a'):
    ct = f"import darr\n" \
         f"# path_to_data_dir is the directory that contains this README\n" \
         f"{varname} = darr.Array(path='path_to_data_dir')\n"
    return ct


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
                    'float16': 'uint16',
                    'float32': 'float32',
                    'float64': 'float64',
                    'complex64': '_special_case_',
                    'complex128': '_special_case_',
                   }

endianness_matlab = {'little': 'ieee-le',
                     'big': 'ieee-be'}

def readcodematlab(numtype, shape, endianness,filepath='arrayvalues.bin',
                   varname='a'):
    typedescr = typedescr_matlab[numtype]
    if typedescr is None:
        return None
    elif numtype.startswith('complex'): # cannot be read directly by matlab
        return readcodematlab_complex(numtype=numtype, shape=shape,
                                      endianness=endianness, filepath=filepath,
                                      varname=varname)
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
    if numtype == 'float16':  # cannot be read directly by matlab, via uint8
        ct += f"{varname} = half.typecast({varname}); % may not work in " \
              f"Octave yet\n"
    return ct + "fclose(fileid);\n"

def readcodematlab_complex(numtype, shape, endianness,
                           filepath='arrayvalues.bin',
                           varname='a'):
    if numtype=='complex128':
        skip = 8
        typedescr =  typedescr_matlab['float64']
    elif numtype == 'complex64':
        skip = 4
        typedescr = typedescr_matlab['float32']
    else:
        raise ValueError(f"numtype '{numtype}' not a complex64 or complex128")
    endianness = endianness_matlab[endianness]
    shape = list(shape)[::-1]  # darr is always C order, Matlab is F order
    size = np.product(shape)
    ndim = len(shape)
    ct = f"fileid = fopen('{filepath}');\n"
    for subvarname, offset in zip(('re', 'im'),(0, skip)):
        if offset > 0:
            ct += f"fseek(fileid, {offset}, 'bof'); % to read imaginary " \
                  f"numbers\n"
        if ndim == 1:
            ct += f"{subvarname} = fread(fileid, {size}, '*{typedescr}'," \
                  f" {skip}," \
                  f"'{endianness}');\n"
        elif ndim == 2:
            ct += f"{subvarname} = fread(fileid, {shape}, '*{typedescr}', " \
                  f"{skip}, '{endianness}');\n"
        else:  # ndim > 2, we need reshape to get multidimensional array
            ct += f"{subvarname} = reshape(fread(fileid, {size}, " \
                  f"'*{typedescr}', " \
                  f"'{skip}, {endianness}'), {shape});\n"
    ct += "fclose(fileid);\n"
    return ct + f"{varname} = complex(re, im);\n"

def readcodematlab_float16(shape, endianness,
                           filepath='arrayvalues.bin',
                           varname='a'):
    ct = f"fileid = fopen('{filepath}');\n"


# R does not support int64 but will read it OK for values that are valid for
# int32: -2147483647 to 2147483647
typedescr_r = {'int8': ('integer()', 1, 'TRUE'),
               'int16': ('integer()', 2, 'TRUE'),
               'int32': ('integer()', 4, 'TRUE'),
               'int64': ('integer()', 8, 'TRUE'),
               'uint8': ('integer()', 1, 'FALSE'),
               'uint16': ('integer()', 2, 'FALSE'),
               'uint32': None,
               'uint64': None,
               'float16': None,
               'float32': ('numeric()', 4, 'TRUE'),
               'float64': ('numeric()', 8, 'TRUE'),
               'complex64': None,
               'complex128': ('complex()', 16, 'TRUE'),
              }

endianness_r = {'little': 'little',
                'big': 'big'}

def readcoder(numtype, shape, endianness, filepath='arrayvalues.bin',
              varname='a', ignoreint64=False):
    if numtype == 'int64' and not ignoreint64:
        return None
    typedescr = typedescr_r[numtype]
    if typedescr is None:
        return None
    endianness = endianness_r[endianness]
    what, size, signed = typedescr
    shape = shape[::-1]  # darr is always C order, R is F order
    n = np.product(shape)
    ct = f'fileid <- file("{filepath}", "rb")\n' \
         f'{varname} <- readBin(con=fileid, what={what}, n={n}, size={size}, ' \
         f'signed={signed}, endian="{endianness}")\n'
    if len(shape) > 1:
        ct += f'{varname} <- array(data={varname}, dim=c{shape}, ' \
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
    ct += f'FileTools[Binary][Close]("{filepath}");\n'
    ndim = len(shape)
    if ndim > 1:
        shape = list(shape[::-1])
        ct += f'{varname} := ArrayTools[Reshape]({varname}, {shape});\n'
    return ct

typedescr_python = {'int8': 'b',
                   'int16': 'h',
                   'int32': 'l',
                   'int64': 'q',
                   'uint8': 'B',
                   'uint16': 'H',
                   'uint32': 'L',
                   'uint64': 'Q',
                   'float16': None,
                   'float32': 'f',
                   'float64': 'd',
                   'complex64': 'f', # special case, we create two f arrays
                   'complex128': 'd', # special case, we creats two d arrays
                  }

endianness_python = {'little': '<',
                    'big': '>'}

def readcodepython(numtype, shape, endianness, filepath='arrayvalues.bin',
                  varname='a'):
    """We only support 1D arrays. Complex types are supported but lead to
    separate real and imaginary arrays in Python, as the array type does not
    support complex numbers natively"""

    typeletter = typedescr_python[numtype]
    endianness = endianness_python[endianness]
    if typeletter is None:
        return None
    if len(shape) > 1:
        return None
    size = shape[0]
    if numtype.startswith('complex'):
        size *= 2 # we split real and imaginary numbers
    typedescr = f"{endianness}{size}{typeletter}"
    ct = f"import array\nimport struct\n"
    if numtype.startswith('complex'):
        fptype = {'f': 'float', 'd': 'double' }[typeletter]
        ct += f"# file holds complex values but we need to read them as" \
              f" {fptype} type\n"
    ct += f"with open('arrayvalues.bin', 'rb') as f:\n" \
          f"    {varname} = array.array('{typeletter}', " \
          f"struct.unpack('{typedescr}', f.read()))\n"
    if numtype.startswith('complex'):
        ct += f"# array '{varname}' has real and imaginary values at " \
              f"alternating positions\n" \
              f"# we can split them into separate arrays\n" \
              f"real = array.array('{typeletter}', ({varname}[i] for i in " \
              f"range(0, len({varname}), 2)))\n"\
              f"imag = array.array('{typeletter}', ({varname}[i] for i in " \
              f"range(1, len({varname}), 2)))\n"
    return ct



readcodefunc = {
        'darr': readcodedarr,
        'idl': readcodeidl,
        'julia_ver0': readcodejulia0,
        'julia_ver1': readcodejulia1,
        'mathematica': readcodemathematica,
        'matlab': readcodematlab,
        'maple': readcodemaple,
        'numpy': readcodenumpy,
        'numpymemmap': readcodenumpymemmap,
        'python': readcodepython,
        'R': readcoder,
}


def readcode(da, language, abspath=False, basepath=None, varname='a',**kwargs):
    """Produces the code to read the Darr array `da` in a given programming
    language.

    Parameters
    ----------
    da: Darr array
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
    d = da._arrayinfo
    if language not in readcodefunc:
        raise ValueError(f"'{language}' not supported ({readcodefunc.keys()})")
    numtype = d['numtype']
    shape = d['shape']
    endianness = d['byteorder']
    if abspath:
        filepath = da._datapath.absolute().resolve()
    elif basepath is not None:
        filepath = Path(basepath) / da._datapath.name
    else:
        filepath = Path(da._datapath.name)
    filepath = filepath.as_posix()
    return readcodefunc[language](numtype=numtype, shape=shape,
                                  endianness=endianness, filepath=filepath,
                                  varname=varname, **kwargs)


def promptify_codetxt(codetxt, prompt=">>> "):
    return "\n".join([f"{prompt}{l}" for l in codetxt.splitlines()]) + '\n'


shapeexplanationtextarray = \
     f'Notes on dimensions and indexing of arrays\n' \
     f'==========================================\n\n' + \
wrap(f'The dimensions stated in the format description above are based on a '
     f'row-major memory layout where the *last* dimension is the one that '
     f'varies most rapidly with memory address. However, in some languages '
     f'arrays are based on column-major memory layout. To keep things '
     f'efficient, the code examples above do not change the memory layout '\
     f'when reading the array in a different language. This means that in '
     'column-major languages, the dimension axes will be *inversed*. Row-major '
     f'languages are: Python and Mathematica. Columns-major languages are: '
     f'Julia, Matlab/Octave, R, Maple, and IDL/GDL. \n')

