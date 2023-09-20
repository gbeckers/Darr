This directory stores a numeric array in an open and simple format that is
universally readable (Darr, see: https://pypi.org/project/darr/). It is
easiest to read the array data using the code provided below for a number of
popular analysis environments. If your language is not included, the data
format description specifies all information needed to read the data.

Data format description
=======================

The file 'arrayvalues.bin' contains the raw binary values of the numeric
array, without header information, in the following format:

  Numeric type: 8-bit signed integer (range: -128 to 127)
  Byte order: little (most-significant byte last)
  Array dimensions: (26, 2)
  Array order layout:  C (Row-major; last dimension varies most rapidly with memory address)

This information is also stored in JSON format in the separate UTF-8 text
file, 'arraydescription.json'.

Code for reading the numeric data
=================================

Note that the array is 2-dimensional and stored with a row-major memory
layout. In column-major languages (see Note below), the code provided here
will lead to an array that has its dimensions reversed (2, 26) with respect to
the format description above (26, 2).

Python with Darr:
-----------------
import darr
# path_to_data_dir is the directory that contains this README
a = darr.Array(path='path_to_data_dir')

Python with Numpy:
------------------
import numpy as np
a = np.fromfile('arrayvalues.bin', dtype='<i1')
a = a.reshape((26, 2), order='C')

Python with Numpy (memmap):
---------------------------
import numpy as np
a = np.memmap('arrayvalues.bin', dtype='<i1', shape=(26, 2), order='C')

R:
--
fileid <- file("arrayvalues.bin", "rb")
a <- readBin(con=fileid, what=integer(), n=52, size=1, signed=TRUE, endian="little")
a <- array(data=a, dim=c(2, 26), dimnames=NULL)
close(fileid)

Scilab:
-------
fileid = mopen("arrayvalues.bin", "rb");
a = mgeti(52, "cl", fileid);
a = matrix(a, [2, 26]);
mclose(fileid);

Matlab/Octave:
--------------
fileid = fopen('arrayvalues.bin');
a = fread(fileid, [2, 26], '*int8', 'ieee-le');
fclose(fileid);

Julia (version < 1.0):
----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read(fileid, Int8, (2, 26)));
close(fileid);

Julia (version >= 1.0):
-----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read!(fileid, Array{Int8}(undef, 2, 26)));
close(fileid);

Mathematica:
------------
a = BinaryReadList["arrayvalues.bin", "Integer8", ByteOrdering -> -1];
a = ArrayReshape[a, {26, 2}];

Maple:
------
a := FileTools[Binary][Read]("arrayvalues.bin", integer[1], byteorder=little, output=Array);
FileTools[Binary][Close]("arrayvalues.bin");
a := ArrayTools[Reshape](a, [2, 26]);


Notes on dimensions and indexing of arrays
==========================================

The dimensions stated in the format description above are based on a row-major
memory layout where the *last* dimension is the one that varies most rapidly
with memory address. However, in some languages arrays are based on column-
major memory layout. To keep things efficient, the code examples above do not
change the memory layout when reading the array in a different language. This
means that in column-major languages, the dimension axes will be *reversed*.
Row-major languages are: Python and Mathematica. Columns-major languages are:
Julia, Scilab, Matlab/Octave, R, Maple, and IDL/GDL.