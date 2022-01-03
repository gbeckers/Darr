This directory contains a numeric array that is stored in an open and simple
format. It should be easy to access the data in most analysis environments. In
Python, you can use the Darr library (https://pypi.org/project/darr/), which
was used to create the data. Alternatively, you can access the data directly
using the code snippets below. If your language is not included, the full data
format description should help.


Data format
===========

The file 'arrayvalues.bin' contains the raw binary values of the numeric
array, without header information, in the following format:

  Numeric type: 16-bit half precision float (sign bit, 5 bits exponent, 10 bits mantissa)
  Byte order: little (most-significant byte last)
  Array length: 7

These details are also stored in JSON format in the separate UTF-8 text file,
'arraydescription.json'.

The file 'metadata.json' contains metadata in JSON UTF-8 text format.


Code snippets for reading the numeric data
==========================================

Python with Darr:
-----------------
import darr
# path_to_data_dir is the directory that contains this README
a = darr.Array(path='path_to_data_dir')

Python with Numpy:
------------------
import numpy as np
a = np.fromfile('arrayvalues.bin', dtype='<f2')

Python with Numpy (memmap):
---------------------------
import numpy as np
a = np.memmap('arrayvalues.bin', dtype='<f2', shape=(7,), order='C')

R:
--
fileid = file("arrayvalues.bin", "rb")
a = readBin(con=fileid, what=numeric(), n=7, size=2, signed=TRUE, endian="little")
close(fileid)

Julia (version < 1.0):
----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read(fileid, Float16, (7,)));
close(fileid);

Julia (version >= 1.0):
-----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read!(fileid, Array{Float16}(undef, 7)));
close(fileid);

