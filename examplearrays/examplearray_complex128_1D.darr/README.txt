This directory contains a numeric array that is stored in an open and simple
format. It should be easy to access the data in most analysis environments. In
Python, you can use the Darr library (https://pypi.org/project/darr/), which
was used to create the data. Alternatively, you can access the data directly
using the code snippets below. If your language is not included, the full data
format description should help.


Data format
===========

The file 'arrayvalues.bin' contains the raw binary values of the numeric
array, without header information, in the following format:

  Numeric type: 128-bit IEEE double‐precision complex number, represented by two 64 - bit floats (real and imaginary components)
  Byte order: little (most-significant byte last)
  Array length: 7

These details are also stored in JSON format in the separate UTF-8 text file,
'arraydescription.json'.

The file 'metadata.json' contains metadata in JSON UTF-8 text format.


Code snippets for reading the numeric data
==========================================

Python:
-------
import array
import struct
# file holds complex values but we need to read them as double type
with open('arrayvalues.bin', 'rb') as f:
    a = array.array('d', struct.unpack('<14d', f.read()))
# array 'a' has real and imaginary values at alternating positions
# we can split them into separate arrays
real = array.array('d', (a[i] for i in range(0, len(a), 2)))
imag = array.array('d', (a[i] for i in range(1, len(a), 2)))

Python with Darr:
-----------------
import darr
# path_to_data_dir is the directory that contains this README
a = darr.Array(path='path_to_data_dir')

Python with Numpy:
------------------
import numpy as np
a = np.fromfile('arrayvalues.bin', dtype='<c16')

Python with Numpy (memmap):
---------------------------
import numpy as np
a = np.memmap('arrayvalues.bin', dtype='<c16', shape=(7,), order='C')

R:
--
fileid = file("arrayvalues.bin", "rb")
a = readBin(con=fileid, what=complex(), n=7, size=16, signed=TRUE, endian="little")
close(fileid)

Matlab/Octave:
--------------
fileid = fopen('arrayvalues.bin');
re = fread(fileid, 7, '*float64', 8,'ieee-le');
fseek(fileid, 8, 'bof'); % to read imaginary numbers
im = fread(fileid, 7, '*float64', 8,'ieee-le');
fclose(fileid);
a = complex(re, im);

Julia (version < 1.0):
----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read(fileid, Complex{Float64}, (7,)));
close(fileid);

Julia (version >= 1.0):
-----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read!(fileid, Array{Complex{Float64}}(undef, 7)));
close(fileid);

IDL/GDL:
--------
a = read_binary("arrayvalues.bin", data_type=9, data_dims=[7], endian="little")

Mathematica:
------------
a = BinaryReadList["arrayvalues.bin", "Complex128", ByteOrdering -> -1];
a = ArrayReshape[a, {7}];

