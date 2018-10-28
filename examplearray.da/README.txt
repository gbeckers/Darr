Description of data format
==========================

The file 'arrayvalues.bin' contains a numeric array in the following format:

Numeric type: 64-bit IEEE double precision float (sign bit, 11 bits exponent, 52 bits mantissa)
Byte order: little (least-significant byte first)
Array dimensions:  (2, 1024)
Array order layout:  C (Row-major; last dimension varies most rapidly with memory address)

The file only contains the raw binary values, without header information.

Format details are also stored in json format in the separate UTF-8 text file, 'arraydescription.json'.

If present, the file 'metadata.json' contains metadata in json UTF-8 text format.

Example code for reading the data
=================================

Python with Numpy:
------------------
import numpy as np
a = np.fromfile('arrayvalues.bin', dtype='<f8')
a = a.reshape((2, 1024), order='C')

Python with Numpy (memmap):
---------------------------
import numpy as np
a = np.memmap('arrayvalues.bin', dtype='<f8', shape=(2, 1024), order='C')

R:
--
fileid = file("arrayvalues.bin", "rb")
a = readBin(con=fileid, what=numeric(), n=2048, size=8, endian="little")
a = array(data=a, dim=c(1024, 2), dimnames=NULL)
close(fileid)

Matlab/Octave:
--------------
fileid = fopen('arrayvalues.bin');
a = fread(fileid, [1024, 2], '*float64', 'ieee-le');
fclose(fileid);

Julia:
------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read(fileid, Float64, (1024, 2)));
close(fileid);

IDL/GDL:
--------
a = read_binary("arrayvalues.bin", data_type=5, data_dims=[1024, 2], endian="little")

Mathematica:
------------
a = BinaryReadList["arrayvalues.bin", "Real64", ByteOrdering -> -1];
a = ArrayReshape[a, {2, 1024}];

