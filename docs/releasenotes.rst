Release notes
=============

Version 0.6.3
-------------
- correct packaging mistake in 0.6.1

Version 0.6.1
-------------
- test if files are accessible for Windows
- restructure package structure
- simplify testing

Version 0.6.0
-------------
- make compatible with numpy 2

Version 0.5.5
-------------
- implement read code for Scilab.
- pydata sphinx theme doc.

Version 0.5.4
--------------
- `iterappend` method of RaggedArray more efficient, faster.

Version 0.5.2
-------------
- fixed packaging dependency.

Version 0.5.2
-------------
- `open` function that returns or Arrays and RaggedArray depending on what
  the path contains.
- adhere to new standard version parsing with packaging module, preventing
  warning messages.

Version 0.5.1
-------------
- automatically convert numpy datetime64 to str in json metadata

Version 0.5.0
-------------
- implement read code for complex types in Matlab/Octave (which cannot do
  this directly).
- implement read code for float16 type in Matlab (which cannot do
  this directly).
- implement 'readcodelanguages' property to get the languages that an array
  or ragged array can produce coding code for.
- implement practical workaround code to read complex arrays into plain
  Python; we produce separate real and imaginary arrays.
- implement Julia (version >= 1) read code for ragged arrays
- implement Maple read code for ragged arrays
- implement IDL read code for ragged arrays
- improve Maple read code arrays
- implement flexible paths read code functions
- Array and RaggedArray README.txt files now contain explanation on row- vs
  column-major, counting from 0/1, and in/exclusive end index.
- RaggedArrays supports empty subarrays in R and IDL
- Check length of Ragged Arrays for compatibility with R. If too long, no R
  code.
- implemented functions that allow for easier testing compatibility other
  laguages.

Version 0.4.1
-------------
- improve array format README description.
- add pure Python read code for 1D arrays.
- add archive methods to arrays and raggedarrays
- archives do not contain absolute path to array anymore

Version 0.4.0
-------------
- changed name 'open' method to 'open_array' for Arrays.
- fixed bug setting metadata on RaggedArrays (would generate error)

Version 0.3.3
-------------
- create temporary arrays that are deleted after use in context
- add readcode methods to Array and RaggedArray, to produce read code strings
  in other languages.
- improved read code RaggedArray (now based on anonymous
  function for Matlab, support for ndim > 3).


Version 0.3.2
-------------
- copy function DataDir
- add skipkeys argument for saving json data in DataDir
- improve json handling by converting numpy objects automatically
- implemented __contains__ for metadata


Version 0.3.1
-------------
- Array and RaggedArray now have a `datadir` attribute instead of being a
  subclass of BaseDataDir.
- BasedDataDir renamed to DataDir


Version 0.2.2
-------------
- fixed bug that sometimes wouldn't allow for deleting a file on Windows
  because of a Windows timing issue
- add more tests
- create conda-forge package


Version 0.2.1
-------------
- fixed bug checking file consistency for very large files


Version 0.2.0
--------------
- improved the ability to work with multiple references to same array
- implement truncate ragged array
- remove 'view' method as it created problems on Windows
- added 'open' method to partially replace view
- fixed truncate bug that sometimes occurred in Windows
- improved explanation in array README
- better documentation of ragged arrays
- refactoring code into more, smaller modules


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