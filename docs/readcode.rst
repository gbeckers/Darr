Reading data in other environments
==================================

The most important feature that makes Darr stand out for scientific
use, is that it is self-documented and includes code to read the array in other
analysis platforms. This maximizes the chances that your data will be
relatively easily accessible in different environments. A quick copy-paste
from the README.txt file, and you or any one else will be looking at your
Python array in, e.g., Matlab, R or Mathematica.

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

For example, for an 8 by 2 unsigned int32 array, the README.txt will provide
the following code snippet to read the array data in Julia:

.. code:: julia

    >>> fileid = open("arrayvalues.bin","r");
    >>> a = map(ltoh, read!(fileid, Array{UInt32}(undef, 2, 8)));
    >>> close(fileid);

However, not all array types are supported in all environments (see table
below). For example Maple does not have unsigned integers, and Python
without numpy does not support multi-dimensional arrays. Hence Darr will not
include code for for these environments with such arrays.

In some environments, not all array numeric types can be read directly,
although it can be done with more effort. For example, Matlab/Octave does not
directly read complex numbers from file, or float16. In those cases, Darr
generates slightly more involved code that still does what you want. You
don't have to worry about it, because just copy-pasting the code will suffice.

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
| float16    |     |   X   |       |             |   X    |   X   |        | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| float32    |  X  |   X   |   X   |      X      |   X    |   X   |   X    | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| float64    |  X  |   X   |   X   |      X      |   X    |   X   |   X    | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| complex64  |  X  |   X   |       |      X      |   X    |   X   |        |    |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| complex128 |  X  |   X   |       |      X      |   X    |   X   |        | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+

X : supported


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