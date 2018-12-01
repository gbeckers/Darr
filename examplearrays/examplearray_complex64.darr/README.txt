This directory contains a numeric array. The array can be read in Python using the Darr library
(https://pypi.org/project/darr/), but if that is not available it should be straightforward to
read the data in other environments using the information below.

Description of data format
==========================

The file 'arrayvalues.bin' contains a numeric array in the following format:

  Numeric type: 64-bit IEEE single‐precision complex number, represented by two 32 - bit floats (real and imaginary components)
  Byte order: little (most-significant byte last)
  Array dimensions: (8, 2)
  Array order layout:  C (Row-major; last dimension varies most rapidly with memory address)

The file only contains the raw binary values, without header information.

Format details are also stored in json format in the separate UTF-8 text file,
'arraydescription.json' to facilitate automatic reading by a program.

If present, the file 'metadata.json' contains metadata in json UTF-8 text format.

Example code for reading the data
=================================

Python with Numpy:
------------------
import numpy as np
a = np.fromfile('arrayvalues.bin', dtype='<c8')
a = a.reshape((8, 2), order='C')

Python with Numpy (memmap):
---------------------------
import numpy as np
a = np.memmap('arrayvalues.bin', dtype='<c8', shape=(8, 2), order='C')

Julia (version < 1.0):
----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read(fileid, Complex{Float32}, (2, 8)));
close(fileid);

Julia (version >= 1.0):
-----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read!(fileid, Array{Complex{Float32}}(undef, 2, 8)));
close(fileid);

IDL/GDL:
--------
a = read_binary("arrayvalues.bin", data_type=6, data_dims=[2, 8], endian="little")

Mathematica:
------------
a = BinaryReadList["arrayvalues.bin", "Complex64", ByteOrdering -> -1];
a = ArrayReshape[a, {8, 2}];

