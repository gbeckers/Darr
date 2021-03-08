This directory contains a numeric array that is stored in an open and simple
format and that is easy to access in most analysis environments. In Python,
you can use the Darr library (https://pypi.org/project/darr/), which was used
to create the data. If Darr is not available, it is straightforward to access
the data using the information below, which includes code for a number of
popular platforms.


Data format
===========

The file 'arrayvalues.bin' contains a numeric array in the following format:

  Numeric type: 32‐bit signed integer (-2147483648 to 2147483647)
  Byte order: little (most-significant byte last)
  Array dimensions: (24, 2)
  Array order layout:  C (Row-major; last dimension varies most rapidly with memory address)

The file only contains the raw binary values, without header information.

Format details are also stored in json format in the separate UTF-8 text file,
'arraydescription.json' to facilitate automatic reading by a program.

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
a = np.fromfile('arrayvalues.bin', dtype='<i4')
a = a.reshape((24, 2), order='C')

Python with Numpy (memmap):
---------------------------
import numpy as np
a = np.memmap('arrayvalues.bin', dtype='<i4', shape=(24, 2), order='C')

R:
--
fileid = file("arrayvalues.bin", "rb")
a = readBin(con=fileid, what=integer(), n=48, size=4, signed=TRUE, endian="little")
a = array(data=a, dim=c(2, 24), dimnames=NULL)
close(fileid)

Matlab/Octave:
--------------
fileid = fopen('arrayvalues.bin');
a = fread(fileid, [2, 24], '*int32', 'ieee-le');
fclose(fileid);

Julia (version < 1.0):
----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read(fileid, Int32, (2, 24)));
close(fileid);

Julia (version >= 1.0):
-----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read!(fileid, Array{Int32}(undef, 2, 24)));
close(fileid);

IDL/GDL:
--------
a = read_binary("arrayvalues.bin", data_type=3, data_dims=[2, 24], endian="little")

Mathematica:
------------
a = BinaryReadList["arrayvalues.bin", "Integer32", ByteOrdering -> -1];
a = ArrayReshape[a, {24, 2}];

Maple:
------
a := FileTools[Binary][Read]("arrayvalues.bin", integer[4], byteorder=little, output=Array);
a := ArrayTools[Reshape](a, [2, 24]);

