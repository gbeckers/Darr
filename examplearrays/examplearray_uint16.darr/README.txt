This directory contains a numeric array that can be accessed in Python using
the Darr library (https://pypi.org/project/darr/), but that can also be
accessed  easily in other environments. In Darr, do:

>>> import darr
>>> a = darr.Array('path_to_array_dir')

where 'path_to_array_dir' is the name of the array directory, which is the one
that also contains this README.

If the Darr library is not available, it should be straightforward to access
the data based on the information below. There is example code for a quite a
number of platforms, in which case it is a matter of copying a few lines.


Description of data format
==========================

The file 'arrayvalues.bin' contains a numeric array in the following format:

  Numeric type: 16‐bit unsigned integer (0 to 65535)
  Byte order: little (most-significant byte last)
  Array dimensions: (8, 2)
  Array order layout:  C (Row-major; last dimension varies most rapidly with memory address)

The file only contains the raw binary values, without header information.

Format details are also stored in json format in the separate UTF-8 text file,
'arraydescription.json' to facilitate automatic reading by a program.

If present, the file 'metadata.json' contains metadata in json UTF-8 text
format.


Example code for reading the numeric data without Darr
=======================================================

Python with Numpy:
------------------
import numpy as np
a = np.fromfile('arrayvalues.bin', dtype='<u2')
a = a.reshape((8, 2), order='C')

Python with Numpy (memmap):
---------------------------
import numpy as np
a = np.memmap('arrayvalues.bin', dtype='<u2', shape=(8, 2), order='C')

R:
--
fileid = file("arrayvalues.bin", "rb")
a = readBin(con=fileid, what=integer(), n=16, size=2, signed=FALSE, endian="little")
a = array(data=a, dim=c(2, 8), dimnames=NULL)
close(fileid)

Matlab/Octave:
--------------
fileid = fopen('arrayvalues.bin');
a = fread(fileid, [2, 8], '*uint16', 'ieee-le');
fclose(fileid);

Julia (version < 1.0):
----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read(fileid, UInt16, (2, 8)));
close(fileid);

Julia (version >= 1.0):
-----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read!(fileid, Array{UInt16}(undef, 2, 8)));
close(fileid);

IDL/GDL:
--------
a = read_binary("arrayvalues.bin", data_type=12, data_dims=[2, 8], endian="little")

Mathematica:
------------
a = BinaryReadList["arrayvalues.bin", "UnsignedInteger16", ByteOrdering -> -1];
a = ArrayReshape[a, {8, 2}];

