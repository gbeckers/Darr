This directory stores a numeric ragged array (also called a jagged array). It
is a sequence of 8 subarrays, each of which are 2-dimensional and can vary in
the length of their first dimension. 

The shape of the first five subarrays is (subarray index: shape):

    0: (6,2)
    1: (6,2)
    2: (3,2)
    3: (4,2)
    4: (1,2)
    ...

The ragged array can be read using the Python library Darr
(https://pypi.org/project/darr/), which was used to create the data. If that
is not available, you can use the code snippets in the last section of this
README to read the data in a number of other environments. If code for your
environment is not provided, use the description of how the data can be read
in the next section.

Description of data format
==========================

There are two subdirectories, "values" and "indices", each containing an array
stored in a self-explanatory format. You first need to read these two arrays
using the information in the README.txt files in their subdirectories.
"values" holds the ragged array, where subarrays are simply concatenated along
their variable length dimension (first axis). The n-th subarray can be
retrieved from the values array by using the appropriate start and end index
on the first axis of the values array. These indices are stored in the two-
dimensional array in "indices". The first axis of the index array corresponds
to the sequence numbers of the subarrays, while the length-2 second axis holds
the start and end indices to be used on the values array to retrieve a
subarray. To read the n-th subarray, read the nt-h start and end indices from
the indices array and use these to read the array data from the values array.
Note that the indices start counting from zero, and end indices are non-
inclusive.


Example code for reading the data
=================================

Python with Numpy (memmap):
---------------------------
import numpy as np
i = np.memmap('indices/arrayvalues.bin', dtype='<i8', shape=(8, 2), order='C')
v = np.memmap('values/arrayvalues.bin', dtype='<c16', shape=(26, 2), order='C')
def get_subarray(seqno):
    starti, endi = i[seqno]
    return v[starti:endi]
a = get_subarray(2)  # example to read third subarray

R:
--
# read array of indices to be used on values array
fileid = file("indices/arrayvalues.bin", "rb")
i = readBin(con=fileid, what=integer(), n=16, size=8, signed=TRUE, endian="little")
i = array(data=i, dim=c(2, 8), dimnames=NULL)
close(fileid)
# read array of values:
fileid = file("values/arrayvalues.bin", "rb")
v = readBin(con=fileid, what=complex(), n=52, size=16, signed=TRUE, endian="little")
v = array(data=v, dim=c(2, 26), dimnames=NULL)
close(fileid)
# create function to get subarrays:
get_subarray <- function(j){
    starti = i[1,j]+1  # R starts counting from 1
    endi = i[2,j]  # R has inclusive end index
    return (v[,starti:endi])}
# example to read third subarray:
# get_subarray(3)

Julia (version >= 1.0):
-----------------------
# read indices array, to be used on values array later:
fileid = open("indices/arrayvalues.bin","r");
i = map(ltoh, read!(fileid, Array{Int64}(undef, 2, 8)));
close(fileid);
# read complex128 values array:
fileid = open("values/arrayvalues.bin","r");
v = map(ltoh, read!(fileid, Array{Complex{Float64}}(undef, 2, 26)));
close(fileid);
# create a function that returns the k-th subarray
# from the values array:
function get_subarray(k)
    starti = i[1,k]+1  # Julia starts counting from 1
    endi = i[2,k]  # Julia has inclusive end index
    v[:,starti:endi]
end
# example to read third subarray:
# get_subarray(3)

Matlab/Octave:
--------------
% read indice array, to be used on values array later:
fileid = fopen('indices/arrayvalues.bin');
i = fread(fileid, [2, 8], '*int64', 'ieee-le');
fclose(fileid);
% read complex128 values array:
fileid = fopen('values/arrayvalues.bin');
re = fread(fileid, [2, 26], '*float64', 8, 'ieee-le');
fseek(fileid, 8, 'bof'); % to read imaginary numbers
im = fread(fileid, [2, 26], '*float64', 8, 'ieee-le');
fclose(fileid);
v = complex(re, im);
% create an anonymous function that returns the k-th subarray
% from the values array:
s = @(k) v(:,i(1,k)+1:i(2,k));
% example to read third subarray:
% s(3)

