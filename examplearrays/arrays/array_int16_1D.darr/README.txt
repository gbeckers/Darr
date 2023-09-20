This directory stores a numeric array in an open and simple format that is
universally readable (Darr, see: https://pypi.org/project/darr/). It is
easiest to read the array data using the code provided below for a number of
popular analysis environments. If your language is not included, the data
format description specifies all information needed to read the data.

Data format description
=======================

The file 'arrayvalues.bin' contains the raw binary values of the numeric
array, without header information, in the following format:

  Numeric type: 16‐bit signed integer (range: -32768 to 32767)
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
    a = array.array('h', struct.unpack('<9h', f.read()))

Python with Darr:
-----------------
import darr
# path_to_data_dir is the directory that contains this README
a = darr.Array(path='path_to_data_dir')

Python with Numpy:
------------------
import numpy as np
a = np.fromfile('arrayvalues.bin', dtype='<i2')

Python with Numpy (memmap):
---------------------------
import numpy as np
a = np.memmap('arrayvalues.bin', dtype='<i2', shape=(9,), order='C')

R:
--
fileid <- file("arrayvalues.bin", "rb")
a <- readBin(con=fileid, what=integer(), n=9, size=2, signed=TRUE, endian="little")
close(fileid)

Scilab:
-------
fileid = mopen("arrayvalues.bin", "rb");
a = mgeti(9, "sl", fileid);
mclose(fileid);

Matlab/Octave:
--------------
fileid = fopen('arrayvalues.bin');
a = fread(fileid, 9, '*int16', 'ieee-le');
fclose(fileid);

Julia (version < 1.0):
----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read(fileid, Int16, (9,)));
close(fileid);

Julia (version >= 1.0):
-----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read!(fileid, Array{Int16}(undef, 9)));
close(fileid);

IDL/GDL:
--------
a = read_binary("arrayvalues.bin", data_type=2, data_dims=[9], endian="little")

Mathematica:
------------
a = BinaryReadList["arrayvalues.bin", "Integer16", ByteOrdering -> -1];
a = ArrayReshape[a, {9}];

Maple:
------
a := FileTools[Binary][Read]("arrayvalues.bin", integer[2], byteorder=little, output=Array);
FileTools[Binary][Close]("arrayvalues.bin");


