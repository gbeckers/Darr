This directory contains a numeric array that is stored in an open and simple
format and that is easy to access in most analysis environments. In Python,
you can use the Darr library (https://pypi.org/project/darr/), which was used
to create the data. Alternatively, to access the data directly in Python or
other environments, use the information below, which includes code for a
number of popular platforms.


Data format
===========

The file 'arrayvalues.bin' contains the raw binary values of the numeric
array, without header information, in the following format:

  Numeric type: 64‐bit unsigned integer (0 to 18446744073709551615)
  Byte order: little (most-significant byte last)
  Array dimensions: (24, 2)
  Array order layout:  C (Row-major; last dimension varies most rapidly with memory address)

These details are also stored in JSON format in the separate UTF-8 text file,
'arraydescription.json'.

Example code for reading the numeric data
=========================================

Python with Darr:
-----------------
import darr
# path_to_data_dir is the directory that contains this README
a = darr.Array(path='path_to_data_dir')

Python with Numpy:
------------------
import numpy as np
a = np.fromfile('arrayvalues.bin', dtype='<u8')
a = a.reshape((24, 2), order='C')

Python with Numpy (memmap):
---------------------------
import numpy as np
a = np.memmap('arrayvalues.bin', dtype='<u8', shape=(24, 2), order='C')

R:
--
fileid = file("arrayvalues.bin", "rb")
a = readBin(con=fileid, what=integer(), n=48, size=8, signed=FALSE, endian="little")
a = array(data=a, dim=c(2, 24), dimnames=NULL)
close(fileid)

Matlab/Octave:
--------------
fileid = fopen('arrayvalues.bin');
a = fread(fileid, [2, 24], '*uint64', 'ieee-le');
fclose(fileid);

Julia (version < 1.0):
----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read(fileid, UInt64, (2, 24)));
close(fileid);

Julia (version >= 1.0):
-----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read!(fileid, Array{UInt64}(undef, 2, 24)));
close(fileid);

IDL/GDL:
--------
a = read_binary("arrayvalues.bin", data_type=15, data_dims=[2, 24], endian="little")

Mathematica:
------------
a = BinaryReadList["arrayvalues.bin", "UnsignedInteger64", ByteOrdering -> -1];
a = ArrayReshape[a, {24, 2}];

