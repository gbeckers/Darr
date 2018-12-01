This directory contains a numeric array. The array can be read in Python using the Darr library
(https://pypi.org/project/darr/), but if that is not available it should be straightforward to
read the data in other environments using the information below.

Description of data format
==========================

The file 'arrayvalues.bin' contains a numeric array in the following format:

  Numeric type: 128-bit IEEE double‐precision complex number, represented by two 64 - bit floats (real and imaginary components)
  Byte order: little (most-significant byte last)
  Array dimensions: (24, 2)
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
a = np.fromfile('arrayvalues.bin', dtype='<c16')
a = a.reshape((24, 2), order='C')

Python with Numpy (memmap):
---------------------------
import numpy as np
a = np.memmap('arrayvalues.bin', dtype='<c16', shape=(24, 2), order='C')

R:
--
fileid = file("arrayvalues.bin", "rb")
a = readBin(con=fileid, what=complex(), n=48, size=16, signed=TRUE, endian="little")
a = array(data=a, dim=c(2, 24), dimnames=NULL)
close(fileid)

Julia (version < 1.0):
----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read(fileid, Complex{Float64}, (2, 24)));
close(fileid);

Julia (version >= 1.0):
-----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read!(fileid, Array{Complex{Float64}}(undef, 2, 24)));
close(fileid);

IDL/GDL:
--------
a = read_binary("arrayvalues.bin", data_type=9, data_dims=[2, 24], endian="little")

Mathematica:
------------
a = BinaryReadList["arrayvalues.bin", "Complex128", ByteOrdering -> -1];
a = ArrayReshape[a, {24, 2}];

