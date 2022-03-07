This directory contains a numeric array that is stored in an open and simple
format. It should be easy to access the data in most analysis environments.
The array can be read using the NumPy-based Python library Darr
(https://pypi.org/project/darr/), which was used to create the data.
Alternatively, you can access the data directly using the code snippets below.
If your language is not included, the full data format description should
help.

Data format
===========

The file 'arrayvalues.bin' contains the raw binary values of the numeric
array, without header information, in the following format:

  Numeric type: 8-bit signed integer (range: -128 to 127)
  Byte order: little (most-significant byte last)
  Array length: 9

These details are also stored in JSON format in the separate UTF-8 text file,
'arraydescription.json'.

The file 'metadata.json' contains metadata in JSON UTF-8 text format.


Code snippets for reading the numeric data
==========================================

Python:
-------
import array
import struct
with open('arrayvalues.bin', 'rb') as f:
    a = array.array('b', struct.unpack('<9b', f.read()))

Python with Darr:
-----------------
import darr
# path_to_data_dir is the directory that contains this README
a = darr.Array(path='path_to_data_dir')

Python with Numpy:
------------------
import numpy as np
a = np.fromfile('arrayvalues.bin', dtype='<i1')

Python with Numpy (memmap):
---------------------------
import numpy as np
a = np.memmap('arrayvalues.bin', dtype='<i1', shape=(9,), order='C')

R:
--
fileid <- file("arrayvalues.bin", "rb")
a <- readBin(con=fileid, what=integer(), n=9, size=1, signed=TRUE, endian="little")
close(fileid)

Matlab/Octave:
--------------
fileid = fopen('arrayvalues.bin');
a = fread(fileid, 9, '*int8', 'ieee-le');
fclose(fileid);

Julia (version < 1.0):
----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read(fileid, Int8, (9,)));
close(fileid);

Julia (version >= 1.0):
-----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read!(fileid, Array{Int8}(undef, 9)));
close(fileid);

Mathematica:
------------
a = BinaryReadList["arrayvalues.bin", "Integer8", ByteOrdering -> -1];
a = ArrayReshape[a, {9}];

Maple:
------
a := FileTools[Binary][Read]("arrayvalues.bin", integer[1], byteorder=little, output=Array);
FileTools[Binary][Close]("arrayvalues.bin");


