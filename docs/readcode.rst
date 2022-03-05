Reading data in other environments
==================================

The most important feature that makes Darr stand out for scientific use, is
that it is self-documented and includes code to read the array in many other
analysis platforms. This maximizes the chances that your data will be
accessible to anyone for a long time to come. In most cases, a quick
copy-paste from the README.txt file will suffice to read your array data in
other scientific computing environments.

Currently, Darr arrays provide read code examples for:

- Python with just standard library
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

For example, for an 810 by 23 unsigned int32 array, the README.txt will
provide a code snippet to read the array data in Julia:

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
| float16    |     |   X   |       |             |   X*   |   X   |        |    |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| float32    |  X  |   X   |   X   |      X      |   X    |   X   |   X    | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| float64    |  X  |   X   |   X   |      X      |   X    |   X   |   X    | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| complex64  |  X  |   X   |       |      X      |   X*   |   X   |   X**  |    |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| complex128 |  X  |   X   |       |      X      |   X*   |   X   |   X**  | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+

X : fully supported, i.e. efficient code can read the array data directly.

*: type natively supported, but reading code requires workaround that may be
less efficient in terms of memory use, depending on use.

**: not natively supported, but practical workaround code is provided.

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

Advice for maximizing efficient readabiliy
------------------------------------------

- From the tables above it is clear that the following types are unproblematic
  in all languages: int16, int32, int64, float32, float64. If possible, use
  these types.

- Complex128 is relatively well supported, except for Maple. It needs
  workaround code that is less efficient in Matlab and plain Python.

- All unsigned integers are not supported in Maple.

- float16 is not widely supported, but it is supported by two modern,
  open source computing packages: Julia and Python with Numpy. It is best
  avoided it and use float32, unless there are disk space concerns. Matlab
  can read it indirectly, using a temporary array and type casting, which can be
  problematic when arrays are very large and RAM is limited. Octave does not
  support it (yet).
