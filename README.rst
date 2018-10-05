=========
DiskArray
=========

DiskArray is a Python library for storing numeric data arrays in a format
that is as open and simple as possible. It is primarily designed for
scientific use cases, when accessibility of data is of fundamental
importance. It also provides easy and fast memory-mapped read/write access
to such disk-based data, using `NumPy indexing`_, and allows for the
flexible use of metadata.

To avoid tool- or library-specific data formats, DiskArray is exclusively
based on self-explaining flat binary and text files. It automatically
generates and saves a clear text description of how exactly the
data is stored, and provides example code to read the specific data in a
variety of current scientific data tools.

DiskArray is open source and freely available under the `New BSD License`_
terms.

Version: 0.1

DiskFile is BSD licensed (BSD 3-Clause License).
(c) 2018, Gabriël Beckers

.. contents::


Features
--------
Pros
****

- Very **simple data format** based on **flat binary** and **text**
  files. This maximizes readability by other software and analysis tools,
  now and in many years to come.
- Numeric data is accessed through a **memory-mapped** file, allowing for
  direct access to **very large data arrays**, even larger than available RAM
  memory.
- Data is selected for reading/writing through **NumPy indexing** (see
  `here`_) and is easily **appendable**.
- **Human-readable explanation of how the binary data is stored** is saved
  in a README text file, which also contains **examples of how to read the
  specific array data in a few lines of code** in popular analysis environments
  such as Python (without DiskArray), R, Julia, Octave/Matlab, GDL/IDL,
  and Mathematica.
- **Many numeric types** are supported:  int8, int16, int32, int64, uint8,
  uint16, uint32, uint64, float16, float32, float64, complex64, complex128.
- Easy use of **metadata**, stored in a separate text file.
- **Minimal dependencies**, only `NumPy`_.
- **Small** library. Just one module file that can be easily included in your
  own code if you want to avoid dependence on external libraries.

Cons
****

- **No compression**. This to keep things as simple and accessible as
  possible. For archiving the data, you can of course simply compress the file
  with any compression tool if you wish.
- **Multiple files**. The data, the data description, and the metadata are
  stored in separate files, though all within a single directory.
- **Inefficient for very small arrays**. Do use other approaches if you have
  a zillion small arrays. A DiskArrayList is being developed to deal with
  the latter, but it is still very experimental.



Examples
--------

**Creating diskarray from NumPy array**

.. code-block:: python

    >>> import numpy as np
    >>> import diskarray as da
    >>> ar = np.ones(2,1024)
    >>> ar
    array([[ 1.,  1.,  1., ...,  1.,  1.,  1.],
           [ 1.,  1.,  1., ...,  1.,  1.,  1.]])
    >>> dar = da.asdiskarray('ar1.da', ar)
    >>> dar
    diskarray([[ 1.,  1.,  1., ...,  1.,  1.,  1.],
               [ 1.,  1.,  1., ...,  1.,  1.,  1.]]) (r)


The data is now stored on disk in a directory named 'ar.da', containing a flat
binary file ('arrayvalues.bin') and a human-readble
`JSON`_ text file ('arraydescription.json'), with information on the
array dimensionality, layout and numeric type. It also contains a 'README.txt' file
explaining the data format as well as providing instructions on how to read the
array using other tools. For example, it provides the code to read the array in
`Octave`_/Matlab:


.. code-block:: octave

    fileid = fopen('arrayvalues.bin');
    a = fread(fileid, [1024, 2], '*float64', 'ieee-le');
    fclose(fileid);

Or in `R`_:

.. code-block:: R

    to.read = file("arrayvalues.bin", "rb")
    a = readBin(con=to.read, what=numeric(), n=2048, size=8, endian="little")
    a = array(data=a, dim=c(1024, 2), dimnames=NULL)
    close(to.read)

Or in `Julia`_:

.. code-block:: julia

    fid = open("arrayvalues.bin","r");
    x = map(ltoh, read(fid, Float64, (1024, 2)));
    close(fid);

**Reading data**

The disk-based array is memory-mapped and can be used to read data using NumPy
indexing.

.. code-block:: python

    >>> dar[:,-2]
    array([ 1.,  1.])

Note that reading data through indexing creates a NumPy array. The diskarray
itself is not a NumPy array. For computation, read (or view, see below) the
data, using indexing, first:

.. code-block:: python

    >>> 2 * dar[:]
    array([[2., 2., 2., ..., 2., 2., 2.],
           [2., 2., 2., ..., 2., 2., 2.]])

If your diskarray is too large to read into RAM, you could use the `Dask`_ or
the `NumExpr`_ library for computation (see example below).


**Writing data**

Writing is also done through NumPy indexing. Writing directly leads to changes
on disk. Our example array is read-only because we did not specify otherwise
in the 'asdiskarray' function above, so we'll set it to be writable
first:

.. code-block:: python

    >>> dar.set_accessmode('r+')
    >>> dar[:,1] = 2.
    >>> dar
    diskarray([[ 1.,  2.,  1., ...,  1.,  1.,  1.],
               [ 1.,  2.,  1., ...,  1.,  1.,  1.]]) (r+)

Of course, you could have done that with the NumPy array before converting
it to a diskarray, but working with a memory-mapped array on disk can be
advantageous when arrays are very large.

**Efficient I/O**

To get maximum speed when doing multiple operations open a direct view on
the disk-based array:

.. code-block:: python

    >>> with dar.view() as v:
    ...     v[0,0] = 3.
    ...     v[0,2] = 4.
    ...     v[1,[0,2,-1]] = 5.
    >>> dar
    diskarray([[ 3.,  2.,  4., ...,  1.,  1.,  1.],
               [ 5.,  2.,  5., ...,  1.,  1.,  5.]]) (r+)

If not opened explicitly like this, every read and write operation will
under the hood open and close the underlying file(s) when necessary, making
it potentially slower.

**Creating diskarray from scratch**

Diskarrays can also be created de novo. We now choose a different numeric type:

.. code-block:: python

    >>> dar2 = da.create_diskarray('ar2.da', shape=(2,1024), dtype='uint8')
    >>> dar2
    diskarray([[0, 0, 0, ..., 0, 0, 0],
               [0, 0, 0, ..., 0, 0, 0]], dtype=uint8) (r+)

The default is to fill the array with zeros but the 'fill' parameter can
change this value. There is also a 'fillfunc' parameter to fill the array non-
uniformly, in more complex ways. See the :doc:`api`.

**Appending data**
You can easily append data to a diskarray, which is immediately reflected in
the disk-based files. This is big plus in many situations. Think for
example of saving data as it is generated by an instrument. A restriction
is that you can only append to the first axis:

.. code-block:: python

    >>> dar2.append(np.ones((3,1024)))
    >>> dar2
    diskarray([[0, 0, 0, ..., 0, 0, 0],
               [0, 0, 0, ..., 0, 0, 0],
               [1, 1, 1, ..., 1, 1, 1],
               [1, 1, 1, ..., 1, 1, 1],
               [1, 1, 1, ..., 1, 1, 1]], dtype=uint8) (r+)

The associated 'README.txt' and 'arraydescription.json' texts files are
also automatically updated to reflect these changes. There is an
'iterappend' method for efficient serial appending. See the :doc:`api`.

**Copying and type casting data**

.. code-block:: python

    >>> dar3 = dar2.copy('ar3.da')
    >>> dar4 = dar2.copy('ar4.da', dtype='float16')
    >>> dar4
    diskarray([[ 0.,  0.,  0., ...,  0.,  0.,  0.],
               [ 0.,  0.,  0., ...,  0.,  0.,  0.],
               [ 1.,  1.,  1., ...,  1.,  1.,  1.],
               [ 1.,  1.,  1., ...,  1.,  1.,  1.],
               [ 1.,  1.,  1., ...,  1.,  1.,  1.]], dtype=float16) (r)

Note that the type of the array can be changed when copying. Data is copied
in chunks, so very large arrays will not flood RAM memory.


**Larger than memory computation**

For computing with very large diskarrays, I recommend the `Dask`_ library,
which works nicely with diskarray. I'll base the example on a small array
though:

.. code-block:: python

    >>> import dask.array
    >>> dar5 = da.create_diskarray('ar5.da', shape=(1024**2), fill=2.5)
    >>> dar5
    diskarray([2.5, 2.5, 2.5, ..., 2.5, 2.5, 2.5]) (r+)
    >>> a = dask.array.from_array(dar5, chunks=(512))
    >>> ((a + 1) / 2).store(dar5)
    >>> dar5
    diskarray([1.75, 1.75, 1.75, ..., 1.75, 1.75, 1.75]) (r+)

So in this case we overwrote the data in dar5 with the results of the computation,
but we could have stored the result in a different diskarray of the same shape. Dask
can do more powerful things, for which I refer to the `Dask documentation`_. The
point here is that diskarrays can be both sources and stores for Dask.

Alternatively, you can use the `NumExpr`_ library using a view of the diskarray,
like so:

.. code-block:: python

    >>> import numexpr as ne
    >>> dar6 = da.create_diskarray('ar6.da', shape=(1024**2), fill=2.5)
    >>> with dar6.view() as v:
    ...     ne.evaluate('(v + 1) / 2', out=v)
    >>> dar6
    diskarray([1.75, 1.75, 1.75, ..., 1.75, 1.75, 1.75]) (r+)

**Metadata**

Metadata can be read and written as a dictionary. Changes correspond to
changes in a human-readable JSON text file that holds the metadata on disk.

.. code-block:: python

    >>> dar2.metadata
    {}
    >>> dar2.metadata['samplingrate'] = 1000.
    >>> dar2.metadata
    {'samplingrate': 1000.0}
    >>> dar2.metadata.update({'starttime': '12:00:00', 'electrodes': [2, 5]})
    >>> dar2.metadata
    {'electrodes': [2, 5], 'samplingrate': 1000.0, 'starttime': '12:00:00'}
    >>> dar2.metadata['starttime'] = '13:00:00'
    >>> dar2.metadata
    {'electrodes': [2, 5], 'samplingrate': 1000.0, 'starttime': '13:00:00'}
    >>> del dar2.metadata['starttime']
    dar2.metadata
    {'electrodes': [2, 5], 'samplingrate': 1000.0}


When making multiple changes it is more
efficient to use the 'update' method to make them all at once, as shown above.

Since JSON is used to store the metadata, you cannot store arbitrary python
objects. You can only store:

- strings
- numbers
- booleans (True/False)
- None
- lists
- dictionaries with string keys


Rationale
---------

Scientific data should preferably be stored or at least archived in a file
format that is as simple as possible. This ensures readability by a variety
of currently used analysis tools (Python, R, Octave/Matlab, Julia, GDL/IDL,
Mathematic, Igor Pro, etc) as well as future tools. This is in line with the
principle of openness and facilitates re-use and reproducibility of
scientific results. At the same time, it would be nice if data files could
be created and accessed efficiently, also when data sets are large.

DiskArray tries to address both requirements for numeric data arrays.

It stores the data itself in a flat binary file. This is a future-proof way of
storing numeric data, as long as clear information is
provided on how the binary data is organized. Many file formats write such
information as a header in front of the numeric data. However, that requires the
reader somehow to know how long the header part of the file is and how to
interpret it. A header is clearly not the ideal solution when maximizing
readability, because we want to assume as little a priori knowledge as
possible.

DiskArray therefore writes the information about the organization of the data to
a separate file. In addition to getting rid of the header, this allows us to
write the information in plain text format. An interesting other approach
would be to simply embed this information in the name of the binary file,
see `pyfbf`_. Nevertheless, I prefer providing more comprehensive
information then could realistically fit in a file name.

This approach makes it is easy to read your numeric array data with one or a
few lines of code, or even with GUI import tools, without depending on the
DiskArray library itself. To facilitate this process, DiskArray saves
together with the data a README text file that explains the format, and that
contains example code of how to read the specific data with common tools
such as Python/NumPy, R, Julia, MatLab/Octave, and Mathematica. Just copy and
paste to read the data. Sharing your data is now very easy because
every array that you save can be simply be provided as such to your
colleagues. It already contains a text document that explains how to read the
data, in many cases with minimal effort.

The choice of storing the actual data in a flat binary file may at first
seem odd given that there exist nice and broadly supported solutions
for binary scientific data, such as `HDF5`_, which feature access time and
storage space optimizations. I have used and use HDF5 a lot, and I like it,
but in my own work I find that in many cases this solution can be too complex
for my needs. Complexity has costs as well as benefits, and I now only
use it when the benefits clearly outweigh the costs, which is sometimes but
not often the case. For an interesting view on this topic I refer to a
`blog of Cyrille Rossant`_, which is in line with my own experiences.

In addition to saving and reading data in a simple and durable format,
DiskArray enables you to accesses the disk-based data in a memory-mapped
way. Data arrays can thus be very large, larger than available RAM memory,
and access is fast and efficient, based on `NumPy indexing`_.

In terms of usage from a python environment , DiskArray is very similar
to using a NumPy memory-mapped `.npy`_ file. The only differences are that the
binary data and header info are split over different files to make the data
more easily readable by other tools, that data can easily be appended,
and that you can flexibly use and store arbitrary metadata.


There are of course also disadvantages to this approach.

- Although the data is widely readable by many scientific analysis tools and
  programming languages, it lacks the ease of 'double-click access' that
  specific data file formats have. For example, if your data is a sound
  recording, saving it in '.wav' format enables you to directly open it in any
  audio program.
- To keep things as simple as possible, DiskArray does not use compression.
  Depending on the data, storage can thus take more disk space than
  necessary. If you are archiving your data and insist on minimizing
  disk space usage you can compress the data files with a general
  compression tool that is likely to be still supported in the distant future,
  such as bzip2. Sometimes, compression is used to speed up
  data transmission to the processor cache (see for example `blosc`_). You
  are missing out on that as well. However, in addition to making your data
  less easy to read, this type of compression may require careful tweaking of
  parameters depending on how you typically read and write the data, and
  failing to do so may lead to access that is in fact slower.
- Your data is not stored in one file, but in a directory that contains
  3-4 files (depending if you save metadata), at least 2 of which are small
  text files (~150 b - 1.7 kb). This has two disadvantages:

  - It is less ideal when transferring data, for example by email. You may
    want to archive them into a single file first (zip, tar).
  - In many file systems, files take up a minimum amount of disk space
    (normally 512 b - 4 kb) even if the data they contain is not that large.
    Diskarray's way of storing data is thus space-inefficient if you have
    zillions of very small data arrays stored separately.


Requirements
------------

DiskArray requires Python 3.6+ and NumPy.

Development and Contributing
----------------------------

This library is developed by Gabriël Beckers. Any help / suggestions / ideas
/ contributions are very welcome and appreciated. For any comment, question,
or error, please open an `issue`_ or propose a `pull`_ request on GitHub.

Code can be found on GitHub: https://github.com/gjlbeckers-uu/DiskArray

Testing
-------

To run the test suite:

.. code-block:: python

    >>> import diskarray as da
    >>> da.test()
    ............................
    ----------------------------------------------------------------------
    Ran 28 tests in 4.798s

    OK
    <unittest.runner.TextTestResult run=28 errors=0 failures=0>



.. _New BSD License: https://opensource.org/licenses/BSD-3-Clause
.. _NumPy indexing: https://docs.scipy.org/doc/numpy-1.13.0/reference/arrays.indexing.html
.. _JSON : https://en.wikipedia.org/wiki/JSON
.. _NumPy : http://www.numpy.org/
.. _here: https://docs.scipy.org/doc/numpy-1.13.0/reference/arrays.indexing.html
.. _R : https://cran.r-project.org/
.. _Octave : https://www.gnu.org/software/octave/
.. _Julia : https://julialang.org/
.. _Dask documentation: https://dask.pydata.org/en/latest/index.html
.. _Dask: https://dask.pydata.org/en/latest/
.. _NumExpr: https://numexpr.readthedocs.io/en/latest/
.. _.npy: https://docs.scipy.org/doc/numpy-dev/neps/npy-format.html
.. _blosc: https://github.com/Blosc/c-blosc
.. _pyfbf: https://github.com/davidh-ssec/pyfbf
.. _HDF5: https://www.hdfgroup.org/
.. _blog of Cyrille Rossant: http://cyrille.rossant.net/moving-away-hdf5/
.. _issue: https://github.com/gjlbeckers-uu/DiskArray/issues
.. _pull: https://github.com/gjlbeckers-uu/DiskArray/pulls