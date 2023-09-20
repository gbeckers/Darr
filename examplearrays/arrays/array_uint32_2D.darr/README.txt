This directory stores a numeric array in an open and simple format that is
universally readable (Darr, see: https://pypi.org/project/darr/). It is
easiest to read the array data using the code provided below for a number of
popular analysis environments. If your language is not included, the data
format description specifies all information needed to read the data.

Data format description
=======================

The file 'arrayvalues.bin' contains the raw binary values of the numeric
array, without header information, in the following format:

  Numeric type: 32‐bit unsigned integer (range: 0 to 4294967295)
  Byte order: little (most-significant byte last)
  Array dimensions: (8, 2)
  Array order layout:  C (Row-major; last dimension varies most rapidly with memory address)

This information is also stored in JSON format in the separate UTF-8 text
file, 'arraydescription.json'.

The file 'metadata.json' contains metadata in JSON UTF-8 text format.


Code for reading the numeric data
=================================

Note that the array is 2-dimensional and stored with a row-major memory
layout. In column-major languages (see Note below), the code provided here
will lead to an array that has its dimensions reversed (2, 8) with respect to
the format description above (8, 2).

Python with Darr:
-----------------
import darr
# path_to_data_dir is the directory that contains this README
a = darr.Array(path='path_to_data_dir')

Python with Numpy:
------------------
import numpy as np
a = np.fromfile('arrayvalues.bin', dtype='<u4')
a = a.reshape((8, 2), order='C')

Python with Numpy (memmap):
---------------------------
import numpy as np
a = np.memmap('arrayvalues.bin', dtype='<u4', shape=(8, 2), order='C')

Scilab:
-------
fileid = mopen("arrayvalues.bin", "rb");
a = mgeti(16, "uil", fileid);
a = matrix(a, [2, 8]);
mclose(fileid);

Matlab/Octave:
--------------
fileid = fopen('arrayvalues.bin');
a = fread(fileid, [2, 8], '*uint32', 'ieee-le');
fclose(fileid);

Julia (version < 1.0):
----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read(fileid, UInt32, (2, 8)));
close(fileid);

Julia (version >= 1.0):
-----------------------
fileid = open("arrayvalues.bin","r");
a = map(ltoh, read!(fileid, Array{UInt32}(undef, 2, 8)));
close(fileid);

IDL/GDL:
--------
a = read_binary("arrayvalues.bin", data_type=13, data_dims=[2, 8], endian="little")

Mathematica:
------------
a = BinaryReadList["arrayvalues.bin", "UnsignedInteger32", ByteOrdering -> -1];
a = ArrayReshape[a, {8, 2}];


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