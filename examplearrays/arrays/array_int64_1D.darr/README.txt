This directory stores a numeric array in an open and simple format that is
universally readable (Darr, see: https://pypi.org/project/darr/). It is
easiest to read the array data using the code provided below for a number of
popular analysis environments. If your language is not included, the data
format description specifies all information needed to read the data.

Data format description
=======================

The file 'arrayvalues.bin' contains the raw binary values of the numeric
array, without header information, in the following format:

  Numeric type: 64‐bit signed integer (range: -9223372036854775808 to 9223372036854775807)
  Byte order: little (most-significant byte last)
  Array length: 9

This information is also stored in JSON format in the separate UTF-8 text
file, 'arraydescription.json'.

The file 'metadata.json' contains metadata in JSON UTF-8 text format.


Code for reading the numeric data
=================================

Python:
-------
import array
import struct
with open('arrayvalues.bin', 'rb') as f:
    a = array.array('q', struct.unpack('<9q', f.read()))

Python with Darr:
-----------------
import darr
# path_to_data_dir is the directory that contains this README
a = darr.Array(path='path_to_data_dir')

Python with Numpy:
------------------
import numpy as np
a = np.fromfile('arrayvalues.bin', dtype='<i8')

Python with Numpy (memmap):
---------------------------
import numpy as np
a = np.memmap('arrayvalues.bin', dtype='<i8', shape=(9,), order='C')

Scilab:
-------
fileid = mopen("arrayvalues.bin", "rb");
a = mgeti(9, "ll", fileid);
mclose(fileid);

Matlab/Octave:
--------------
fileid = fopen('arrayvalues.bin');
a = fread(fileid, 9, '*int64', 'ieee-le');
fclose(fileid);

Julia (version < 1.0):
----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read(fileid, Int64, (9,)));
close(fileid);

Julia (version >= 1.0):
-----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read!(fileid, Array{Int64}(undef, 9)));
close(fileid);

IDL/GDL:
--------
a = read_binary("arrayvalues.bin", data_type=14, data_dims=[9], endian="little")

Mathematica:
------------
a = BinaryReadList["arrayvalues.bin", "Integer64", ByteOrdering -> -1];
a = ArrayReshape[a, {9}];

Maple:
------
a := FileTools[Binary][Read]("arrayvalues.bin", integer[8], byteorder=little, output=Array);
FileTools[Binary][Close]("arrayvalues.bin");


