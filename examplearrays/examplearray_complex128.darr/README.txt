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
  Array dimensions: (8, 2)
  Array order layout:  C (Row-major; last dimension varies most rapidly with memory address)

These details are also stored in JSON format in the separate UTF-8 text file,
'arraydescription.json'.

The file 'metadata.json' contains metadata in JSON UTF-8 text format.


Code snippets for reading the numeric data
==========================================

Python with Darr:
-----------------
import darr
# path_to_data_dir is the directory that contains this README
a = darr.Array(path='path_to_data_dir')

Python with Numpy:
------------------
import numpy as np
a = np.fromfile('arrayvalues.bin', dtype='<c16')
a = a.reshape((8, 2), order='C')

Python with Numpy (memmap):
---------------------------
import numpy as np
a = np.memmap('arrayvalues.bin', dtype='<c16', shape=(8, 2), order='C')

R:
--
fileid = file("arrayvalues.bin", "rb")
a = readBin(con=fileid, what=complex(), n=16, size=16, signed=TRUE, endian="little")
a = array(data=a, dim=c(2, 8), dimnames=NULL)
close(fileid)

Matlab/Octave:
--------------
fileid = fopen('arrayvalues.bin');
re = fread(fileid, [2, 8], '*float64', 8, 'ieee-le');
fseek(fileid, 8); % to read imaginary numbers
im = fread(fileid, [2, 8], '*float64', 8, 'ieee-le');
fclose(fileid);
a = complex(re, im);

Julia (version < 1.0):
----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read(fileid, Complex{Float64}, (2, 8)));
close(fileid);

Julia (version >= 1.0):
-----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read!(fileid, Array{Complex{Float64}}(undef, 2, 8)));
close(fileid);

IDL/GDL:
--------
a = read_binary("arrayvalues.bin", data_type=9, data_dims=[2, 8], endian="little")

Mathematica:
------------
a = BinaryReadList["arrayvalues.bin", "Complex128", ByteOrdering -> -1];
a = ArrayReshape[a, {8, 2}];

