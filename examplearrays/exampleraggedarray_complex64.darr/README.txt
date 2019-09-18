Disk-based storage of a ragged array
====================================

This directory is a data store for a numeric ragged array. This is a sequence of arrays in which
one dimension varies in length. On disk, these arrays are concatenated along their variable
dimension. The data can easiest be read in using the Python Darr library
(https://pypi.org/project/darr/):

import darr as da
a = da.RaggedArray(path_to_array_dir)

If Darr is not available, the data can also be read in other environments with more effort using
the descriptions below.

There are two subdirectories, each containing an array stored in a self-explanatory format. See
the READMEs in the corresponding directories to find out in detail out how. However, example code
is provided below for a number of analysis environments, which in many cases is sufficient.

The subdirectory "values" holds the numerical data itself, where subarrays are simply appended
along their variable length dimension (first axis). So the number of dimensions of the values
array is one less than that of the ragged array. A particular subarray can be be retrieved using
the appropriate start and end index along the first axis of the values array. These indices
(counting from 0) are stored in a different 2-dimensional array in the subdirectory "indices". The
first axis of the index array represents the sequence number of the subarray and the second axis
(length 2) represents start and (non-inclusive) end indices to be used on the values array. To
read the n-th subarray, read the nt-h start and end indices from the indices array and use these
to read the array data from the values array.

This ragged array has 3 subarrays.

Example code for reading the data
=================================

Python with Numpy (memmap):
---------------------------
import numpy as np
i = np.memmap('indices/arrayvalues.bin', dtype='<i8', shape=(3, 2), order='C')
v = np.memmap('values/arrayvalues.bin', dtype='<c8', shape=(24, 2), order='C')
def get_subarray(seqno):
    starti, endi = i[seqno]
    return v[starti:endi]
a = get_subarray(2)  # example to read third subarray

