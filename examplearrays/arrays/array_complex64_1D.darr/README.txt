This directory stores a numeric array in an open and simple format that is
universally readable (Darr, see: https://pypi.org/project/darr/). It is
easiest to read the array data using the code provided below for a number of
popular analysis environments. If your language is not included, the data
format description specifies all information needed to read the data.

Data format description
=======================

The file 'arrayvalues.bin' contains the raw binary values of the numeric
array, without header information, in the following format:

  Numeric type: 64-bit IEEE single‐precision complex number, represented by two 32 - bit floats (real and imaginary components)
  Byte order: little (most-significant byte last)
  Array length: 7

This information is also stored in JSON format in the separate UTF-8 text
file, 'arraydescription.json'.

The file 'metadata.json' contains metadata in JSON UTF-8 text format.


Code for reading the numeric data
=================================

Python:
-------
import array
import struct
# file holds complex values but we need to read them as float type
with open('arrayvalues.bin', 'rb') as f:
    a = array.array('f', struct.unpack('<14f', f.read()))
# array 'a' has real and imaginary values at alternating positions
# we can split them into separate arrays
real = array.array('f', (a[i] for i in range(0, len(a), 2)))
imag = array.array('f', (a[i] for i in range(1, len(a), 2)))

Python with Darr:
-----------------
import darr
# path_to_data_dir is the directory that contains this README
a = darr.Array(path='path_to_data_dir')

Python with Numpy:
------------------
import numpy as np
a = np.fromfile('arrayvalues.bin', dtype='<c8')

Python with Numpy (memmap):
---------------------------
import numpy as np
a = np.memmap('arrayvalues.bin', dtype='<c8', shape=(7,), order='C')

Scilab:
-------
fileid = mopen("arrayvalues.bin", "rb");
a = mget(14, "fl", fileid);
a = matrix(a, [2, 7]);
mclose(fileid);
a = complex(squeeze(a(1,:)),squeeze(a(2,:)));

Matlab/Octave:
--------------
fileid = fopen('arrayvalues.bin');
re = fread(fileid, 7, '*float32', 4,'ieee-le');
fseek(fileid, 4, 'bof'); % to read imaginary numbers
im = fread(fileid, 7, '*float32', 4,'ieee-le');
fclose(fileid);
a = complex(re, im);

Julia (version < 1.0):
----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read(fileid, Complex{Float32}, (7,)));
close(fileid);

Julia (version >= 1.0):
-----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read!(fileid, Array{Complex{Float32}}(undef, 7)));
close(fileid);

IDL/GDL:
--------
a = read_binary("arrayvalues.bin", data_type=6, data_dims=[7], endian="little")

Mathematica:
------------
a = BinaryReadList["arrayvalues.bin", "Complex64", ByteOrdering -> -1];
a = ArrayReshape[a, {7}];


