Reading data in other environments
==================================

An important feature of Darr is that it is self-documented and includes code
to read the array in other analysis platforms. Currently supported are:

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

However, not all array types are supported in all environments (see table
below). For example Maple does not have unsigned integers, and Python
without numpy does not support multi-dimensional arrays. Hence Darr will not
include code for such arrays.

Example arrays with code can be found `here <https://github
.com/gbeckers/Darr/tree/master/examplearrays>`__.

Compatibility array data types in other environments
----------------------------------------------------

+------------+-----+-------+-------+-------------+--------+-------+--------+----+
|            | IDL | Julia | Maple | Mathematica | Matlab | Numpy | Python | R  |
+============+=====+=======+=======+=============+========+=======+========+====+
| int8       |     |   X   |   X   |      X      |   X    |   X   |   X    | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| int16      | X   |   X   |   X   |      X      |   X    |   X   |   X    | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| int32      | X   |   X   |   X   |      X      |   X    |   X   |   X    | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| int64      | X   |   X   |   X   |      X      |   X    |   X   |   X    | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| uint8      | X   |   X   |       |      X      |   X    |   X   |   X    | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| uint16     | X   |   X   |       |      X      |   X    |   X   |   X    | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| uint32     | X   |   X   |       |      X      |   X    |   X   |   X    | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| uint64     | X   |   X   |       |      X      |   X    |   X   |   X    | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| float16    |     |   X   |       |             |        |   X   |        | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| float32    | X   |   X   |   X   |      X      |   X    |   X   |   X    | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| float64    | X   |   X   |   X   |      X      |   X    |   X   |   X    | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| complex64  | X   |   X   |       |      X      |        |   X   |        |    |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+
| complex128 | X   |   X   |       |      X      |        |   X   |        | X  |
+------------+-----+-------+-------+-------------+--------+-------+--------+----+

X = supported
