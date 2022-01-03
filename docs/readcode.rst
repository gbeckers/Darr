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

However, not all arrays are supported in all environments. For example Maple
does not have unsigned integers, and Python without numpy does not support
multi-dimensional arrays. Hence Darr will not include code for such arrays.

Example arrays with code can be found `here <https://github
.com/gbeckers/Darr/tree/master/examplearrays>`__.