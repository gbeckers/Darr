Release notes
=============

Version 0.1.12
--------------
- improved explanation in array README
- better documentation of ragged arrays

Version 0.1.11
--------------
- fixed bugs in read code generation Matlab
- removed dependency on numpy.testing (was giving problems with pytest and
  numpy 1.15)
- iterappend for ragged arrays (not optimally efficient yet)

Version 0.1.10
--------------
- cleaned up checksum handling
- refactored handling read code for other languages
- read code for ragged arrays (experimental)
- improved ragged arrays (experimental)

Version 0.1.9
-------------
- archive and compress darr objects

Version 0.1.8
-------------
- create and open arbitrary (non-protected) files in darr array directory
- export darr to `zarr <https://github.com/zarr-developers/zarr>`__
- asarray works on zarr arrays more efficiently
- added support for Maple
- removed set_accessmode method, now set accessmode attribute directly

Version 0.1.7
-------------
License file included, necessary for conda-forge

Version 0.1.6
-------------
More tests and documentation

Version 0.1.3
-------------
Fixed delete bug array list

Version 0.1.2
-------------
Fixed truncate bug on Windows