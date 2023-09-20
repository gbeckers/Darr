This directory stores a numeric array in an open and simple format that is
universally readable (Darr, see: https://pypi.org/project/darr/). It is
easiest to read the array data using the code provided below for a number of
popular analysis environments. If your language is not included, the data
format description specifies all information needed to read the data.

Data format description
=======================

The file 'arrayvalues.bin' contains the raw binary values of the numeric
array, without header information, in the following format:

  Numeric type: 64-bit IEEE double precision float (sign bit, 11 bits exponent, 52 bits mantissa)
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
with open('arrayvalues.bin', 'rb') as f:
    a = array.array('d', struct.unpack('<7d', f.read()))

Python with Darr:
-----------------
import darr
# path_to_data_dir is the directory that contains this README
a = darr.Array(path='path_to_data_dir')

Python with Numpy:
------------------
import numpy as np
a = np.fromfile('arrayvalues.bin', dtype='<f8')

Python with Numpy (memmap):
---------------------------
import numpy as np
a = np.memmap('arrayvalues.bin', dtype='<f8', shape=(7,), order='C')

R:
--
fileid <- file("arrayvalues.bin", "rb")
a <- readBin(con=fileid, what=numeric(), n=7, size=8, signed=TRUE, endian="little")
close(fileid)

Scilab:
-------
fileid = mopen("arrayvalues.bin", "rb");
a = mget(7, "dl", fileid);
mclose(fileid);

Matlab/Octave:
--------------
fileid = fopen('arrayvalues.bin');
a = fread(fileid, 7, '*float64', 'ieee-le');
fclose(fileid);

Julia (version < 1.0):
----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read(fileid, Float64, (7,)));
close(fileid);

Julia (version >= 1.0):
-----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read!(fileid, Array{Float64}(undef, 7)));
close(fileid);

IDL/GDL:
--------
a = read_binary("arrayvalues.bin", data_type=5, data_dims=[7], endian="little")

Mathematica:
------------
a = BinaryReadList["arrayvalues.bin", "Real64", ByteOrdering -> -1];
a = ArrayReshape[a, {7}];

Maple:
------
a := FileTools[Binary][Read]("arrayvalues.bin", float[8], byteorder=little, output=Array);
FileTools[Binary][Close]("arrayvalues.bin");


