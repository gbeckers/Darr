Format Design
=============

Binary array data and text metadata in separate files
-----------------------------------------------------

- The numeric array is saved in a flat binary file called 'arrayvalues.bin'.
- Information on the array's shape, type, memory layout and byte order is
  stored in a JSON text file called 'arraydescription.json'.
- Metadata is stored in a JSON text file called 'metadata.json'.
- Human-readable documentation, with full format descriptions and code
  snippets to ready the array data in many language are stored in a UTF-8
  text file called 'README.txt'.
- These four files are stored in a separate directory, which represents the
  Darr array.
