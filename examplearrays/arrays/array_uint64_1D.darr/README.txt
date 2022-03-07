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

  Numeric type: 64‐bit unsigned integer (range: 0 to 18446744073709551615)
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
    a = array.array('Q', struct.unpack('<9Q', f.read()))

Python with Darr:
-----------------
import darr
# path_to_data_dir is the directory that contains this README
a = darr.Array(path='path_to_data_dir')

Python with Numpy:
------------------
import numpy as np
a = np.fromfile('arrayvalues.bin', dtype='<u8')

Python with Numpy (memmap):
---------------------------
import numpy as np
a = np.memmap('arrayvalues.bin', dtype='<u8', shape=(9,), order='C')

Matlab/Octave:
--------------
fileid = fopen('arrayvalues.bin');
a = fread(fileid, 9, '*uint64', 'ieee-le');
fclose(fileid);

Julia (version < 1.0):
----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read(fileid, UInt64, (9,)));
close(fileid);

Julia (version >= 1.0):
-----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read!(fileid, Array{UInt64}(undef, 9)));
close(fileid);

IDL/GDL:
--------
a = read_binary("arrayvalues.bin", data_type=15, data_dims=[9], endian="little")

Mathematica:
------------
a = BinaryReadList["arrayvalues.bin", "UnsignedInteger64", ByteOrdering -> -1];
a = ArrayReshape[a, {9}];


