Reading data in other environments
==================================

The most important feature that makes Darr stand out for scientific use, is
that it is self-documented and includes code to read the array in many
analysis environments. This maximizes the chances that your data will be
accessible to anyone for a long time to come. In most cases, a quick
copy-paste of a code snippet from the README.txt file will suffice to read your
array data.

Currently, Darr arrays provide read code examples for:

- IDL/GDL
- Julia (version < 1.0)
- Julia (version >= 1.0)
- Mathematica
- Matlab/Octave
- Maple
- Python with just standard library
- Python with Darr library
- Python with Numpy library
- Python with Numpy, based on memmap for very large arrays
- R
- Scilab

For example, for an 810 by 23 unsigned int32 little endian array, the README.txt
will provide a code snippet to read the array data in Julia:

.. code:: julia

    fileid = open("arrayvalues.bin","r");
    a = map(ltoh, read!(fileid, Array{UInt32}(undef, 23, 810)));
    close(fileid);

Read code can also be generated on the fly using the 'readcode' method on
(ragged) arrays in Python. Example with a different array and language:

.. code:: python

    >>> print(a.readcode('mathematica'))
    a = BinaryReadList["arrayvalues.bin", "Real64", ByteOrdering -> -1];
    a = ArrayReshape[a, {2, 1024}];

However, not all array types are supported in all environments (see table
below). For example, Maple does not have unsigned integers, and Python
without numpy does not support multi-dimensional arrays. Darr will not
always include code for such cases, but it will include code if there
are workaround solutions that makes practical sense. For example, Matlab/Octave
does not directly read complex numbers or float16 numbers from file. But with
workaround code it can be done, and Darr will provide it.

To see which languages are supported, use the 'readcodelanguages' property:

.. code:: python

    >>> a.readcodelanguages
    ('R',
     'darr',
     'idl',
     'julia_ver0',
     'julia_ver1',
     'maple',
     'mathematica',
     'matlab',
     'numpy',
     'numpymemmap',
     'scilab')

Example arrays with code for all numeric types can be found `here
<https://github.com/gbeckers/Darr/tree/master/examplearrays>`__.

If you want to maximize readability, see
:doc:`Maximizing readability of your data <readability>`

Compatibility read code numeric types in other environments
-----------------------------------------------------------

+------------+-----+-------+-------+-------------+--------+-------+--------+----+--------+
|            | IDL | Julia | Maple | Mathematica | Matlab | Numpy | Python | R  | Scilab |
+============+=====+=======+=======+=============+========+=======+========+====+========+
| int8       |     |   X   |   X   |      X      |   X    |   X   |   X    | X  |   X    |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+--------+
| int16      |  X  |   X   |   X   |      X      |   X    |   X   |   X    | X  |   X    |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+--------+
| int32      |  X  |   X   |   X   |      X      |   X    |   X   |   X    |X(1)|   X    |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+--------+
| int64      |  X  |   X   |   X   |      X      |   X    |   X   |   X    |    |   X    |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+--------+
| uint8      |  X  |   X   |       |      X      |   X    |   X   |   X    | X  |   X    |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+--------+
| uint16     |  X  |   X   |       |      X      |   X    |   X   |   X    | X  |   X    |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+--------+
| uint32     |  X  |   X   |       |      X      |   X    |   X   |   X    |    |   X    |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+--------+
| uint64     |  X  |   X   |       |      X      |   X    |   X   |   X    |    |   X    |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+--------+
| float16    |     |   X   |       |             |   X*   |   X   |        |    |        |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+--------+
| float32    |  X  |   X   |   X   |      X      |   X    |   X   |   X    | X  |   X    |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+--------+
| float64    |  X  |   X   |   X   |      X      |   X    |   X   |   X    | X  |   X    |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+--------+
| complex64  |  X  |   X   |       |      X      |   X*   |   X   |   X**  |    |   X*   |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+--------+
| complex128 |  X  |   X   |       |      X      |   X*   |   X   |   X**  | X  |   X*   |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+--------+

X : fully supported, i.e. efficient code can read the array data directly.

*: type natively supported, but cannot be read directly from file. Reading
code provides workaround solution that may be less efficient in terms of memory
use, depending on use.

**: complex numbers not natively supported, but practical workaround code is
provided so that real and imaginary parts are represented in separate arrays.

(1) : int32 is supported in R, but it won't read the minimum value of an
int32 (-2147483648) correctly. It will read it as NA. -2147483647 and higher is
fine though.

Compatibility multidimensional arrays in other environments
-----------------------------------------------------------

+------------+-----+-------+-------+-------------+--------+-------+--------+----+--------+
|            | IDL | Julia | Maple | Mathematica | Matlab | Numpy | Python | R  | Scilab |
+============+=====+=======+=======+=============+========+=======+========+====+========+
| 1-D array  |  X  |   X   |   X   |      X      |   X    |   X   |   X    | X  |   X    |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+--------+
| N-D array  |  X  |   X   |   X   |      X      |   X    |   X   |        | X  |   X    |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+--------+

1-D : One-dimensional,
N-D : Multi-dimensional

Memory layout of multi-dimensional arrays
-----------------------------------------

Darr multi-dimensional arrays are based on a row-major memory layout, which
means that elements from the last (rightmost) dimension or index are
contiguous and vary most rapidly with memory address on disk. However, in some
languages arrays are based on a column-major memory layout, which means that
elements from the first (leftmost) dimension or index are contiguous and vary
most rapidly with memory address on disk. To keep reading efficient, the
code snippets that Darr generates do not change the memory layout when reading
the array data in a different language. This means that in column-major
languages, the dimension and index axes will be *reversed* with respect to the
Darr/NumPy convention.

Row-major languages are: Mathematica and Python.

Columns-major languages are: IDL/GDL, Julia, Maple, Matlab/Octave, R, and
Scilab.

E.g., if one reads an array that has dimensions (2,4) in Darr/NumPy, the
reading code will lead to an array having dimension (4,2) in Matlab and
other column-major languages.

In Darr, create an array consisting of 2 rows and 4 columns:

.. code:: python

    >>> a = darr.asarray('test.darr', [[1,2,3,4],[5,6,7,8]])
    >>> a.shape
    (2,4)
    >>> a[0,:]
    array([1, 2, 3, 4])

Read the same array in Matlab using the code snippet in the array's README.txt:

.. code:: matlab

    > fileid = fopen('test.darr/arrayvalues.bin');
    > a = fread(fileid, [4, 2], '*int64', 'ieee-le');
    > fclose(fileid);

Now look at its dimensionality, it is reversed, as are the indexing axes. And
a Darr/NumPy row is returned as a column:

.. code:: matlab

    > size(a)
    ans =
      4   2
    > a
    a =

      1  5
      2  6
      3  7
      4  8

    > a(:,1) # matlab starts counting from 1
    ans =
      1
      2
      3
      4

If you want the dimension and index order in Matlab (and other column-major
languages) to be the same as in NumPy/Darr, you need to transpose the array
after reading it:

.. code:: matlab

    > a = a'
    > size(a)
    ans =

       2   4

    > a
    a =

      1  2  3  4
      5  6  7  8

    > a(1,:)
    ans =

      1  2  3  4

However, it may be that the original memory layout was chosen for efficiency
reasons, and hence for large arrays it may be better not to transpose the
array, and just reverse all indexing operations.




