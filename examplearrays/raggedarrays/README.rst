Example Ragged Arrays
=====================
Darr ragged arrays consist of a folder (here with a '.darr' suffix) contain two
subfolders each representing a Darr array, and to JSON and README text files.

A ragged array (also called a jagged array) can be seen as a sequence
of subarrays that may be multidimensional and that may vary in the length of
their first dimension only.

In the simplest case it is a sequence of variable-length one-dimensional
subarrays, e.g.::

  [[1,2],
   [3,4,5],
   [6],
   [7,8,9,10]]

But they may also be variable-length multi-dimensional subarrays, e.g.::

  [[[1,2],[3,4]],
   [[5,6],[7,8],[9,10]],
   [[11,12]],
   [[13,14],[15,16]]]

See `here for a short tutorial
<https://darr.readthedocs.io/en/latest/tutorialraggedarray.html>`__.