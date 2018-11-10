import sys

# mathematica: https://reference.wolfram.com/language/ref/BinaryRead.html
# Octave: https://octave.org/doc/v4.2.0/Binary-I_002fO.html
# Matlab: https://mathworks.com/help/matlab/ref/fread.html
# R: https://www.rdocumentation.org/packages/base/versions/3.4.3/topics/readBin
# Julia: https://docs.julialang.org/en/release-0.4/manual/integers-and- floating-point-numbers/
# Maple: https://www.maplesoft.com/support/help/maple/view.aspx?path=FileTools%2FBinary%2FRead


numtypes = {
    'int8': {'descr': '8-bit signed integer (-128 to 127)',
             'numpy': 'i1',
             'matlab': 'int8',
             'R': {'what': 'integer()', 'size': 1, 'signed': 'TRUE'},
             'julia': 'Int8',
             'idl': None,
             'mathematica': "Integer8",
             'maple': "integer[1]"},
    'int16': {'descr': '16‐bit signed integer (-32768 to 32767)',
              'numpy': 'i2',
              'matlab': 'int16',
              'R': {'what': 'integer()', 'size': 2, 'signed': 'TRUE'},
              'julia': 'Int16',
              'idl': 2,
              'mathematica': "Integer16",
              'maple': "integer[2]"},
    'int32': {'descr': '32‐bit signed integer (-2147483648 to 2147483647)',
              'numpy': 'i4',
              'matlab': 'int32',
              'R': {'what': 'integer()', 'size': 4, 'signed': 'TRUE'},
              'julia': 'Int32',
              'idl': 3,
              'mathematica': "Integer32",
              'maple': "integer[4]"},
    'int64': {'descr': '64‐bit signed integer (-9223372036854775808 to '
                       '9223372036854775807)',
              'numpy': 'i8',
              'matlab': 'int64',
              'R': {'what': 'integer()', 'size': 8, 'signed': 'TRUE'},
              'julia': 'Int64',
              'idl': 14,
              'mathematica': "Integer64",
              'maple': "integer[8]"},
    'uint8': {'descr': '8‐bit unsigned integer (0 to 255)',
              'numpy': 'u1',
              'matlab': 'uint8',
              'R': {'what': 'integer()', 'size': 1, 'signed': 'FALSE'},
              'julia': 'UInt8',
              'idl': 1,
              'mathematica': "UnsignedInteger8",
              'maple': None},
    'uint16': {'descr': '16‐bit unsigned integer (0 to 65535)',
               'numpy': 'u2',
               'matlab': 'uint16',
               'R': {'what': 'integer()', 'size': 2, 'signed': 'FALSE'},
               'julia': 'UInt16',
               'idl': 12,
               'mathematica': "UnsignedInteger16",
               'maple': None
           },
    'uint32': {'descr': '32‐bit unsigned integer (0 to 4294967295)',
               'numpy': 'u4',
               'matlab': 'uint32',
               'R': {'what': 'integer()', 'size': 4, 'signed': 'FALSE'},
               'julia': 'UInt32',
               'idl': 13,
               'mathematica': "UnsignedInteger32",
               'maple': None},
    'uint64': {'descr': '64‐bit unsigned integer (0 to 18446744073709551615)',
               'numpy': 'u8',
               'matlab': 'uint64',
               'R': {'what': 'integer()', 'size': 8, 'signed': 'FALSE'},
               'julia': 'UInt64',
               'idl': 15,
               'mathematica': "UnsignedInteger64",
                'maple': None},
    'float16': {'descr': '16-bit half precision float (sign bit, 5 bits '
                         'exponent, 10 bits mantissa)',
                'numpy': 'f2',
                'matlab': None,
                'R': {'what': 'numeric()', 'size': 2, 'signed': 'TRUE'},
                'julia': 'Float16',
                'idl': None,
                'mathematica': None,
                'maple': None},
    'float32': {'descr': '32-bit IEEE single precision float (sign bit, '
                         '8 bits exponent, 23 bits mantissa)',
                'numpy': 'f4',
                'matlab': 'float32',
                'R': {'what': 'numeric()', 'size': 4, 'signed': 'TRUE'},
                'julia': 'Float32',
                'idl': 4,
                'mathematica': "Real32",
                'maple': "float[4]"},
    'float64': {'descr': '64-bit IEEE double precision float (sign bit, '
                         '11 bits exponent, 52 bits mantissa)',
                'numpy': 'f8',
                'matlab': 'float64',
                'R': {'what': 'numeric()', 'size': 8, 'signed': 'TRUE'},
                'julia': 'Float64',
                'idl': 5,
                'mathematica': "Real64",
                'maple': "float[8]"},
    'complex64': {'descr': '64-bit IEEE single‐precision complex number, '
                           'represented by two 32 - bit floats (real and '
                           'imaginary components)',
                  'numpy': 'c8',
                  'matlab': None,
                  'R': None,
                  'julia': 'Complex{Float32}',
                  'idl': 6,
                  'mathematica': "Complex64",
                  'maple': None},
    'complex128': {'descr': '128-bit IEEE double‐precision complex number, '
                            'represented by two 64 - bit floats (real and '
                            'imaginary components)',
                   'numpy': 'c16',
                   'matlab': None,
                   'R': {'what': 'complex()', 'size': 16, 'signed': 'TRUE'},
                   'julia': 'Complex{Float64}',
                   'idl': 9,
                   'mathematica': "Complex128",
                   'maple': None}
}

endiannesstypes = {
    'big':    {'descr': 'most-significant byte first',
               'matlab': 'ieee-be',
               'R': 'big',
               'julia': 'ntoh',
               'idl': 'big',
               'mathematica': '+1',
               'numpy': 'big',
               'numpymemmap': 'big',
               'maple': 'big'},
    'little': {'descr': 'least-significant byte first',
               'matlab': 'ieee-le',
               'R': 'little',
               'julia': 'ltoh',
               'idl': 'little',
               'mathematica': '-1',
               'numpy': 'little',
               'numpymemmap': 'little',
               'maple': 'little'}
}


def arrayinfotodtype(arrayinfo):
    """Produces a numpy dtype description string like '<f8' based on a dictionary
    with type description details (as present in json array description file).

    Parameters
    ----------
    arrayinfo: dict
        A dictionary containing info on the numeric type. The following keys
        are required: 'numtype', 'byteorder'.

    Returns
    -------
    dtype description string that can be used to instantiate numpy arrays

    """

    numtype = numtypes.get(arrayinfo['numtype'], None)
    if numtype is None:
        raise ValueError(
            f"'{arrayinfo['numtype']}' is not a valid numeric type")
    numpytype = numtype['numpy']
    if arrayinfo['byteorder'] == 'little':
        dtypedescr = f'<{numpytype}'
    elif arrayinfo['byteorder'] == 'big':
        dtypedescr = f'>{numpytype}'
    else:
        raise ValueError(f"'{arrayinfo['byteorder']}' is not a valid order")
    return dtypedescr


def arraynumtypeinfo(ndarray):
    """Returns a dictionary with numeric type and layout info, to be used
    for saving as json.

    """
    sys_is_le = (sys.byteorder == 'little')
    bo = ndarray.dtype.byteorder
    if (bo == '<') or (sys_is_le and (bo in ('|', '='))):
        bostr = 'little'
    else:
        bostr = 'big'
    return {  # 'dtypedescr': str(ndarray.dtype.descr[0][1]),
        'numtype': ndarray.dtype.name,
        'arrayorder': 'C' if ndarray.flags['C_CONTIGUOUS'] else 'F',
        'shape': ndarray.shape,
        'byteorder': bostr}

