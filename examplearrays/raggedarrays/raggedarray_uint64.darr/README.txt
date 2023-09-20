This directory stores a numeric ragged array (also called a jagged array),
which is a sequence of subarrays that may be multidimensional and that can
vary in the length of their first dimension. 

The ragged array can be read using the NumPy-based Python library Darr
(https://pypi.org/project/darr/), which was used to create the data. If that
is not available, you can use the code snippets below to read the data in a
number of other environments. If code for your environment is not provided,
use the description of how the data can be read in the next section.

Description of ragged array
===========================

This ragged array is a sequence of 9 subarrays, each of which is 2-dimensional
and can vary in the length of its first dimension. The array consists of
uint64 numbers. 

The dimensions of the first five and last subarrays is (subarray index:
dimensions):

    0: (6, 2,)
    1: (6, 2,)
    2: (3, 2,)
    3: (0, 2,)
    4: (4, 2,)
    ...
    8: (2, 2,)

These index numbers are based on Python indexing, which starts at 0.
Dimensions are based on row-major memory layout. When using the code provided
below to read subarrays, dimensions will be inversed in column-major languages
(see Note below).

Description of storage on disk
==============================

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

Python with Darr:
-----------------
import darr
# path_to_data_dir is the directory that contains this README
a = darr.RaggedArray(path='path_to_data_dir')
# example to read third (k=2) subarray:
sa = a[2]

Python with Numpy (memmap):
---------------------------
import numpy as np
i = np.memmap('indices/arrayvalues.bin', dtype='<i8', shape=(9, 2), order='C')
v = np.memmap('values/arrayvalues.bin', dtype='<u8', shape=(26, 2), order='C')
def getsubarray(k):
    starti, endi = i[k]
    return v[starti:endi]
# example to read third (k=2) subarray:
sa = getsubarray(2)

IDL/GDL
-------
; read indices array, to be used on values array later:
i = read_binary("indices/arrayvalues.bin", data_type=14, data_dims=[2, 9], endian="little")
; read uint64 values array:
v = read_binary("values/arrayvalues.bin", data_type=15, data_dims=[2, 26], endian="little")
; example to get the third (k=2) subarray from the values array,
; but set k to get the subarray number you want:
k = 2 
; expression below sets sa variable to subarray
IF i[0,k] EQ i[1,k] THEN sa=[] ELSE sa=v[*,i[0,k]:i[1,k]-1]

Julia (version >= 1.0):
-----------------------
# read indices array, to be used on values array later:
fileid = open("indices/arrayvalues.bin","r");
i = map(ltoh, read!(fileid, Array{Int64}(undef, 2, 9)));
close(fileid);
# read uint64 values array:
fileid = open("values/arrayvalues.bin","r");
v = map(ltoh, read!(fileid, Array{UInt64}(undef, 2, 26)));
close(fileid);
# create a function that returns the k-th subarray
# from the values array:
function getsubarray(k)
    starti = i[1,k]+1  # Julia starts counting from 1
    endi = i[2,k]  # Julia has inclusive end index
    v[:,starti:endi]
end
# example to read third (k=3) subarray:
sa = getsubarray(3)

Matlab/Octave:
--------------
% read indice array, to be used on values array later:
fileid = fopen('indices/arrayvalues.bin');
i = fread(fileid, [2, 9], '*int64', 'ieee-le');
fclose(fileid);
% read uint64 values array:
fileid = fopen('values/arrayvalues.bin');
v = fread(fileid, [2, 26], '*uint64', 'ieee-le');
fclose(fileid);
% create an anonymous function that returns the k-th subarray
% from the values array:
getsubarray = @(k) v(:,i(1,k)+1:i(2,k));
% example to read third (k=3) subarray:
sa = getsubarray(3);

Mathematica:
------------
(* read indices array, to be used on values array later: *)
i = BinaryReadList["indices/arrayvalues.bin", "Integer64", ByteOrdering -> -1];
i = ArrayReshape[i, {9, 2}];
(* read uint64 values array: *)
v = BinaryReadList["values/arrayvalues.bin", "UnsignedInteger64", ByteOrdering -> -1];
v = ArrayReshape[v, {26, 2}];
(* create a function that returns the k-th subarray
   from the values array *):
getsubarray[k_?IntegerQ] := 
    Module[{l},
        l = k;
        starti = i[[l,1]] + 1;
        endi = i[[l,2]];
        v[[starti;;endi]]]
(* example to read third (k=3) subarray: *)
sa = getsubarray[3]

Scilab:
-------
/* read indice array, to be used on values array later: */
fileid = mopen("indices/arrayvalues.bin", "rb");
i = mgeti(18, "ll", fileid);
i = matrix(i, [2, 9]);
mclose(fileid);
/* read uint64 values array: */
fileid = mopen("values/arrayvalues.bin", "rb");
v = mgeti(52, "ull", fileid);
v = matrix(v, [2, 26]);
mclose(fileid);
/* create an anonymous function that returns the k-th subarray */
/* from the values array: */
deff("sa = getsubarray(k)", "sa = v(:,i(1,k)+1:i(2,k))")
/* example to read third (k=3) subarray: */
sa = getsubarray(3);


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

Further, Python starts counting at 0. So the first subarray in a ragged array
has index number 0. This is also true for IDL/GDL. However, Julia, Scilab,
Mathematica, Matlab/Octave, R, and Maple start counting at 1, so the first
subarray has index number 1 in these languages. Finally, in Python indexing
the end index is non-inclusive. E.g., a[0:2] returns a[0] and a[1], but not
a[2]. However, all other languages for which reading code is provided, Julia,
Scilab, Mathematica, Matlab/Octave, R, Maple, and IDL/GDL have an inclusive
end index. The reading code provided takes these differences into account.