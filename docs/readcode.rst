Reading data in other environments
==================================

The most important feature that makes Darr stand out for scientific use, is
that it is self-documented and includes code to read the array in other
analysis platforms. This maximizes the chances that your data will be
accessible to anyone for a long time to come. In most cases, a quick
copy-paste from the README.txt file will suffice to read your array data in
other scientific computing environments.

Currently, Darr arrays provide read code examples for:

- Python (just standard library)
- Python with Darr library
- Python with Numpy library
- Python with Numpy, based on memmap for very large arrays
- R
- Matlab/Octave
- Julia (version < 1.0)
- Julia (version >= 1.0)
- IDL/GDL
- Mathematica
- Maple

For example, for an 81 by 23 unsigned int32 array, the README.txt will
provide a code snippet to read the array data in Julia:

.. code:: julia

    fileid = open("arrayvalues.bin","r");
    a = map(ltoh, read!(fileid, Array{UInt32}(undef, 23, 81)));
    close(fileid);

Read code can also be generated on the fly using the 'readcode' method on
(ragged) arrays in Python:

.. code:: python

    >>> print(a.readcode('mathematica'))
    a = BinaryReadList["arrayvalues.bin", "Real64", ByteOrdering -> -1];
    a = ArrayReshape[a, {2, 1024}];

However, not all array types are supported in all environments (see table
below). For example, Maple does not have unsigned integers, and Python
without numpy does not support multi-dimensional arrays. Darr will not
always include code for such cases, but it will include code if there are ways
around this and the solution makes practical sense. For example, Matlab/Octave
does not directly read complex numbers from file, or float16 numbers. But with
slightly more involved code it can be done, and Darr will generate code for
it. You don't have to worry about the code being more complex, because just
copy-pasting the code will suffice.

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
     'numpymemmap')

Example arrays with code for all numeric types can be found `here
<https://github.com/gbeckers/Darr/tree/master/examplearrays>`__.

Compatibility read code numeric types in other environments
-----------------------------------------------------------

+------------+-----+-------+-------+-------------+--------+-------+--------+----+
|            | IDL | Julia | Maple | Mathematica | Matlab | Numpy | Python | R  |
+============+=====+=======+=======+=============+========+=======+========+====+
| int8       |     |   X   |   X   |      X      |   X    |   X   |   X    | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| int16      |  X  |   X   |   X   |      X      |   X    |   X   |   X    | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| int32      |  X  |   X   |   X   |      X      |   X    |   X   |   X    | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| int64      |  X  |   X   |   X   |      X      |   X    |   X   |   X    | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| uint8      |  X  |   X   |       |      X      |   X    |   X   |   X    | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| uint16     |  X  |   X   |       |      X      |   X    |   X   |   X    | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| uint32     |  X  |   X   |       |      X      |   X    |   X   |   X    | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| uint64     |  X  |   X   |       |      X      |   X    |   X   |   X    | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| float16    |     |   X   |       |             |   X    |   X*  |        | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| float32    |  X  |   X   |   X   |      X      |   X    |   X   |   X    | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| float64    |  X  |   X   |   X   |      X      |   X    |   X   |   X    | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| complex64  |  X  |   X   |       |      X      |   X    |   X*  |   X**  |    |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| complex128 |  X  |   X   |       |      X      |   X    |   X*  |   X**  | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+

X : fully supported, i.e. efficient code can read the array data directly.

*: type natively supported, but reading code requires workaround that may be
less efficient in terms of memory use, depending on use.

**: not natively supported, but practical work around code is provided.

Compatibility multidimensional arrays in other environments
-----------------------------------------------------------

+------------+-----+-------+-------+-------------+--------+-------+--------+----+
|            | IDL | Julia | Maple | Mathematica | Matlab | Numpy | Python | R  |
+============+=====+=======+=======+=============+========+=======+========+====+
| 1-D array  |  X  |   X   |   X   |      X      |   X    |   X   |   X    | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| N-D array  |  X  |   X   |   X   |      X      |   X    |   X   |        | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+

1-D : One-dimensional,
N-D : Multi-dimensional