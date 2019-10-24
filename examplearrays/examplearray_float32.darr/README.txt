This directory contains a numeric array that can be accessed in Python using
the Darr library (https://pypi.org/project/darr/), but that can also be
accessed  easily in other environments. In Darr, do:

>>> import darr
>>> a = darr.Array('path_to_array_dir')

where 'path_to_array_dir' is the name of the array directory, which is the one
that also contains this README.

If the Darr library is not available, it should be straightforward to access
the data based on the information below. This includes code for a number of
popular platforms, in which case it is a matter of copying a few lines.


Description of data format
==========================

The file 'arrayvalues.bin' contains a numeric array in the following format:

  Numeric type: 32-bit IEEE single precision float (sign bit, 8 bits exponent, 23 bits mantissa)
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
a = np.fromfile('arrayvalues.bin', dtype='<f4')
a = a.reshape((8, 2), order='C')

Python with Numpy (memmap):
---------------------------
import numpy as np
a = np.memmap('arrayvalues.bin', dtype='<f4', shape=(8, 2), order='C')

R:
--
fileid = file("arrayvalues.bin", "rb")
a = readBin(con=fileid, what=numeric(), n=16, size=4, signed=TRUE, endian="little")
a = array(data=a, dim=c(2, 8), dimnames=NULL)
close(fileid)

Matlab/Octave:
--------------
fileid = fopen('arrayvalues.bin');
a = fread(fileid, [2, 8], '*float32', 'ieee-le');
fclose(fileid);

Julia (version < 1.0):
----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read(fileid, Float32, (2, 8)));
close(fileid);

Julia (version >= 1.0):
-----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read!(fileid, Array{Float32}(undef, 2, 8)));
close(fileid);

IDL/GDL:
--------
a = read_binary("arrayvalues.bin", data_type=4, data_dims=[2, 8], endian="little")

Mathematica:
------------
a = BinaryReadList["arrayvalues.bin", "Real32", ByteOrdering -> -1];
a = ArrayReshape[a, {8, 2}];

Maple:
------
a := FileTools[Binary][Read]("arrayvalues.bin", float[4], byteorder=little, output=Array);
a := ArrayTools[Reshape](a, [2, 8]);

