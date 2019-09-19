This directory contains a numeric array that can be accessed most easily in Python using the Darr
library (https://pypi.org/project/darr/), as follows:

>>> import darr as da
>>> a = da.Array('path_to_array_dir')

where 'path_to_array_dir' is the name of the array directory.

If the Darr library is not available, it is straightforward to read the data in other environments
based on the information below.

Description of data format
==========================

The file 'arrayvalues.bin' contains a numeric array in the following format:

  Numeric type: 32-bit IEEE single precision float (sign bit, 8 bits exponent, 23 bits mantissa)
  Byte order: little (most-significant byte last)
  Array dimensions: (24, 2)
  Array order layout:  C (Row-major; last dimension varies most rapidly with memory address)

The file only contains the raw binary values, without header information.

Format details are also stored in json format in the separate UTF-8 text file,
'arraydescription.json' to facilitate automatic reading by a program.

If present, the file 'metadata.json' contains metadata in json UTF-8 text format.

Example code for reading the numeric data without Darr
=======================================================

Python with Numpy:
------------------
import numpy as np
a = np.fromfile('arrayvalues.bin', dtype='<f4')
a = a.reshape((24, 2), order='C')

Python with Numpy (memmap):
---------------------------
import numpy as np
a = np.memmap('arrayvalues.bin', dtype='<f4', shape=(24, 2), order='C')

R:
--
fileid = file("arrayvalues.bin", "rb")
a = readBin(con=fileid, what=numeric(), n=48, size=4, signed=TRUE, endian="little")
a = array(data=a, dim=c(2, 24), dimnames=NULL)
close(fileid)

Matlab/Octave:
--------------
fileid = fopen('arrayvalues.bin');
a = fread(fileid, [2, 24], '*float32', 'ieee-le');
fclose(fileid);

Julia (version < 1.0):
----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read(fileid, Float32, (2, 24)));
close(fileid);

Julia (version >= 1.0):
-----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read!(fileid, Array{Float32}(undef, 2, 24)));
close(fileid);

IDL/GDL:
--------
a = read_binary("arrayvalues.bin", data_type=4, data_dims=[2, 24], endian="little")

Mathematica:
------------
a = BinaryReadList["arrayvalues.bin", "Real32", ByteOrdering -> -1];
a = ArrayReshape[a, {24, 2}];

Maple:
------
a := FileTools[Binary][Read]("arrayvalues.bin", float[4], byteorder=little, output=Array);
a := ArrayTools[Reshape](a, [2, 24]);

