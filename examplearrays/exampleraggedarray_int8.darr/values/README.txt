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

  Numeric type: 8-bit signed integer (range: -128 to 127)
  Byte order: little (most-significant byte last)
  Array dimensions: (24, 2)
  Array order layout:  C (Row-major; last dimension varies most rapidly with memory address)

These details are also stored in JSON format in the separate UTF-8 text file,
'arraydescription.json'.

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
a = np.fromfile('arrayvalues.bin', dtype='<i1')
a = a.reshape((24, 2), order='C')

Python with Numpy (memmap):
---------------------------
import numpy as np
a = np.memmap('arrayvalues.bin', dtype='<i1', shape=(24, 2), order='C')

R:
--
fileid = file("arrayvalues.bin", "rb")
a = readBin(con=fileid, what=integer(), n=48, size=1, signed=TRUE, endian="little")
a = array(data=a, dim=c(2, 24), dimnames=NULL)
close(fileid)

Matlab/Octave:
--------------
fileid = fopen('arrayvalues.bin');
a = fread(fileid, [2, 24], '*int8', 'ieee-le');
fclose(fileid);

Julia (version < 1.0):
----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read(fileid, Int8, (2, 24)));
close(fileid);

Julia (version >= 1.0):
-----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read!(fileid, Array{Int8}(undef, 2, 24)));
close(fileid);

Mathematica:
------------
a = BinaryReadList["arrayvalues.bin", "Integer8", ByteOrdering -> -1];
a = ArrayReshape[a, {24, 2}];

Maple:
------
a := FileTools[Binary][Read]("arrayvalues.bin", integer[1], byteorder=little, output=Array);
a := ArrayTools[Reshape](a, [2, 24]);

