Disk-based storage of a ragged array
====================================

This directory is a data store for a numeric ragged array. A ragged array
(also called a jagged array) is a sequence of arrays that may vary in length
in their first dimension only. On disk, these arrays are concatenated along
their variable dimension. The easiest way to access the data is to use the
Darr library (https://pypi.org/project/darr/) in Python, as follows:

>>> import darr
>>> a = darr.RaggedArray('path_to_array_dir')

where 'path_to_array_dir' is the name of the array directory, which is the one
that also contains this README.

If Darr is not available, the data can also be read in other environments,
with a little more effort, using the description or example code below.


Description of data storage
---------------------------
There are two subdirectories, each containing an array stored in a self-
explanatory format. See the READMEs in the corresponding directories to find
out in detail out how to read them. Example code is provided below for a
number of analysis environments, which in many cases is sufficient.

The subdirectory "values" holds the numerical data itself, where subarrays are
simply appended along their variable length dimension (first axis). So the
number of dimensions of the values array is one less than that of the ragged
array. A particular subarray can be be retrieved using the appropriate start
and end index along the first axis of the values array. These indices
(counting from 0) are stored in a different 2-dimensional array in the
subdirectory "indices". The first axis of the index array represents the
sequence number of the subarray and the second axis (length 2) represents
start and (non-inclusive) end indices to be used on the values array. To read
the n-th subarray, read the nt-h start and end indices from the indices array
and use these to read the array data from the values array.


This ragged array has 3 subarrays.

Example code for reading the data
=================================

Python with Numpy (memmap):
---------------------------
import numpy as np
i = np.memmap('indices/arrayvalues.bin', dtype='<i8', shape=(3, 2), order='C')
v = np.memmap('values/arrayvalues.bin', dtype='<f2', shape=(24, 2), order='C')
def get_subarray(seqno):
    starti, endi = i[seqno]
    return v[starti:endi]
a = get_subarray(2)  # example to read third subarray

R:
--
# read array of indices to be used on values array
fileid = file("indices/arrayvalues.bin", "rb")
i = readBin(con=fileid, what=integer(), n=6, size=8, signed=TRUE, endian="little")
i = array(data=i, dim=c(2, 3), dimnames=NULL)
close(fileid)
# read array of values:
fileid = file("values/arrayvalues.bin", "rb")
v = readBin(con=fileid, what=numeric(), n=48, size=2, signed=TRUE, endian="little")
v = array(data=v, dim=c(2, 24), dimnames=NULL)
close(fileid)
get_subarray <- function(j){
    starti = i[1,j]+1  # R starts counting from 1
    endi = i[2,j]  # R has inclusive end index
    return (v[,starti:endi])}
# create function to get subarrays:
# example to read third subarray:
# get_subarray(3)

