Darr
====

|Travis Status| |Appveyor Status| |PyPy version| |Coverage Status| |Docs Status|


Darr is a Python science library for storing numeric data arrays in a way
that is open, simple, and self-explanatory. It enables fast memory-mapped
read/write access to such disk-based data, the ability to append data, and
the flexible use of metadata. It is primarily designed for scientific use
cases. Save and use your numeric arrays and metadata with one line of code
while long-term and tool-independent accessibility and easy shareability
is ensured.

To avoid dependency on specific tools, Darr is based on a combination of
flat binary and human-readable text files. It automatically saves a clear
text description of how the data is stored, together with code for reading
the specific data in a variety of current scientific data tools such as
Python, R, Julia, Matlab and Mathematica.

Darr is open source and freely available under the `New BSD
License <https://opensource.org/licenses/BSD-3-Clause>`__ terms.

Version: 0.1.3 alpha

Darr is BSD licensed (BSD 3-Clause License). (c) 2017-2018, Gabriël
Beckers

.. contents:: Contents
    :depth: 2

Features
--------

Pro's:

-  **Transparent data format** based on **flat binary** and **text**
   files.
-  Supports **very large data arrays** through **memory-mapped** file
   access.
-  Data read/write access through **NumPy indexing** (see
   `here <https://docs.scipy.org/doc/numpy-1.13.0/reference/arrays.indexing.html>`__).
-  Data is easily **appendable**.
-  **Human-readable explanation of how the binary data is stored** is
   saved in a README text file.
-  README also contains **examples of how to read the array** in popular
   analysis environments such as Python (without Darr), R, Julia,
   Octave/Matlab, GDL/IDL, and Mathematica.
-  **Many numeric types** are supported: (u)int8-(u)int64,
   float16-float64, complex64, complex128.
-  Easy use of **metadata**, stored in a separate
   `JSON <https://en.wikipedia.org/wiki/JSON>`__ text file.
-  **Minimal dependencies**, only `NumPy <http://www.numpy.org/>`__.
-  **Integrates easily** with the
   `Dask <https://dask.pydata.org/en/latest/>`__ or
   `NumExpr <https://numexpr.readthedocs.io/en/latest/>`__ libraries for
   **numeric computation on very large Darr arrays**.

Con's:

-  **No compression**, although it is of course possible to simply
   compress the darr files with a compression tool for archiving
   purposes.
-  **Multiple files**. The data, the data description, and the metadata
   are stored in separate files, though all within a single directory.
-  **Inefficient (storage-wise) for very small arrays**. If you have a
   zillion small arrays, and storage space in a concern, use other
   approaches.

Examples
--------

**Creating an array**

.. code:: python

    >>> import darr as da
        >>> a = da.create_array('a1.da', shape=(2,1024))
        >>> a
        >>> array([[0., 0., 0., ..., 0., 0., 0.],
                   [0., 0., 0., ..., 0., 0., 0.]]) (r+)

    The default is to fill the array with zeros (of type float64) but this
    can be changed by the 'fill' and 'fillfunc' parameters. See the api.

    The data is now stored on disk in a directory named 'ar1.da', containing
    a flat binary file ('arrayvalues.bin') and a human-readble
    >>> a = da.create_array('a1.da', shape=(2,1024))
    >>> a
    >>> array([[0., 0., 0., ..., 0., 0., 0.],
               [0., 0., 0., ..., 0., 0., 0.]]) (r+)

The default is to fill the array with zeros (of type float64) but this
can be changed by the 'fill' and 'fillfunc' parameters. See the api.

The data is now stored on disk in a directory named 'ar1.da', containing
a flat binary file ('arrayvalues.bin') and a human-readble
`JSON <https://en.wikipedia.org/wiki/JSON>`__ text file
('arraydescription.json'), with information on the array dimensionality,
layout and numeric type. It also contains a 'README.txt' file explaining
the data format as well as providing instructions on how to read the
array using other tools. For example, it provides the code to read the
array in `Octave <https://www.gnu.org/software/octave/>`__/Matlab:

.. code:: octave

    fileid = fopen('arrayvalues.bin');
    a = fread(fileid, [1024, 2], '*float64', 'ieee-le');
    fclose(fileid);

Or in `R <https://cran.r-project.org/>`__:

.. code:: R

    fileid = file("arrayvalues.bin", "rb")
    a = readBin(con=fileid, what=numeric(), n=2048, size=8, endian="little")
    a = array(data=a, dim=c(1024, 2), dimnames=NULL)
    close(fileid)

Or in `Julia <https://julialang.org/>`__:

.. code:: julia

    fid = open("arrayvalues.bin","r");
    x = map(ltoh, read(fid, Float64, (1024, 2)));
    close(fid);

To see the files that correspond to a Darr array, see
'examplearray.da' in the source
`repo <https://github.com/gjlbeckers-uu/Darr>`__.

**Different numeric type**

.. code:: python

    >>> a = da.create_array('a2.da', shape=(2,1024), dtype='uint8')
    >>> a
    array([[0, 0, 0, ..., 0, 0, 0],
           [0, 0, 0, ..., 0, 0, 0]], dtype=uint8) (r+)

**Creating array from NumPy array**

.. code:: python

    >>> import numpy as np
    >>> na = np.ones((2,1024))
    >>> a = da.asarray('a3.da', na)
    >>> a
    array([[ 1.,  1.,  1., ...,  1.,  1.,  1.],
           [ 1.,  1.,  1., ...,  1.,  1.,  1.]]) (r)

**Reading data**

The disk-based array is memory-mapped and can be used to read data into
RAM using NumPy indexing.

.. code:: python

    >>> a[:,-2]
    array([ 1.,  1.])

Note that that creates a NumPy array. The darr array itself is not a NumPy
array, nor does it behave like one except for indexing. The simplest way
to use the data for computation is to, read (or view, see below) the
data first as a NumPy array:

.. code:: python

    >>> 2 * a[:]
    array([[2., 2., 2., ..., 2., 2., 2.],
           [2., 2., 2., ..., 2., 2., 2.]])

If your data is too large to read into RAM, you could use the
`Dask <https://dask.pydata.org/en/latest/>`__ or the
`NumExpr <https://numexpr.readthedocs.io/en/latest/>`__ library for
computation (see example below).

**Writing data**

Writing is also done through NumPy indexing. Writing directly leads to
changes on disk. Our example array is read-only because we did not
specify otherwise in the 'asarray' function above, so we'll set it to
be writable first:

.. code:: python

    >>> a.set_accessmode('r+')
    >>> a[:,1] = 2.
    >>> a
    array([[ 1.,  2.,  1., ...,  1.,  1.,  1.],
           [ 1.,  2.,  1., ...,  1.,  1.,  1.]]) (r+)

**Efficient I/O**

To get maximum speed when doing multiple operations open a direct view
on the disk-based array so as to opens the underlying files only once:

.. code:: python

    >>> with a.view() as v:
    ...     v[0,0] = 3.
    ...     v[0,2] = 4.
    ...     v[1,[0,2,-1]] = 5.
    >>> a
    array([[ 3.,  2.,  4., ...,  1.,  1.,  1.],
          [ 5.,  2.,  5., ...,  1.,  1.,  5.]]) (r+)

**Appending data**

You can easily append data to a Darr array, which is immediately reflected
in the disk-based files. This is a big plus in many situations. Think
for example of saving data as they are generated by an instrument. A
restriction is that you can only append to the first axis:

.. code:: python

    >>> a.append(np.ones((3,1024)))
    >>> a
    array([[3., 2., 4., ..., 1., 1., 1.],
           [5., 2., 5., ..., 1., 1., 5.],
           [1., 1., 1., ..., 1., 1., 1.],
           [1., 1., 1., ..., 1., 1., 1.],
           [1., 1., 1., ..., 1., 1., 1.]]) (r+)

The associated 'README.txt' and 'arraydescription.json' texts files are
also automatically updated to reflect these changes. There is an
'iterappend' method for efficient serial appending. See the api.

**Copying and type casting data**

.. code:: python

    >>> ac = a.copy('ac.da')
    >>> acf16 = a.copy('acf16.da', dtype='float16')
    >>> acf16
    array([[3., 2., 4., ..., 1., 1., 1.],
           [5., 2., 5., ..., 1., 1., 5.],
           [1., 1., 1., ..., 1., 1., 1.],
           [1., 1., 1., ..., 1., 1., 1.],
           [1., 1., 1., ..., 1., 1., 1.]], dtype=float16) (r)

Note that the type of the array can be changed when copying. Data is
copied in chunks, so very large arrays will not flood RAM memory.

**Larger than memory computation**

For computing with very large darr arrays, I recommend the
`Dask <https://dask.pydata.org/en/latest/>`__ library, which works
nicely with darr. I'll base the example on a small array though:

.. code:: python

    >>> import dask.array
    >>> a = da.create_array('ar1.da', shape=(1024**2), fill=2.5, overwrite=True)
    >>> a
    array([2.5, 2.5, 2.5, ..., 2.5, 2.5, 2.5]) (r+)
    >>> dara = dask.array.from_array(a, chunks=(512))
    >>> ((dara + 1) / 2).store(a)
    >>> a
    array([1.75, 1.75, 1.75, ..., 1.75, 1.75, 1.75]) (r+)

So in this case we overwrote the data in a with the results of the
computation, but we could have stored the result in a different darr array
of the same shape. Dask can do more powerful things, for which I refer
to the `Dask
documentation <https://dask.pydata.org/en/latest/index.html>`__. The
point here is that darr arrays can be both sources and stores for Dask.

Alternatively, you can use the
`NumExpr <https://numexpr.readthedocs.io/en/latest/>`__ library using a
view of the Darr array, like so:

.. code:: python

    >>> import numexpr as ne
    >>> a = da.create_array('a3.da', shape=(1024**2), fill=2.5)
    >>> with a.view() as v:
    ...     ne.evaluate('(v + 1) / 2', out=v)
    >>> a
    array([1.75, 1.75, 1.75, ..., 1.75, 1.75, 1.75]) (r+)

**Metadata**

Metadata can be read and written like a dictionary. Changes correspond
to changes in a human-readable and editable JSON text file that holds
the metadata on disk.

.. code:: python

    >>> a.metadata
    {}
    >>> a.metadata['samplingrate'] = 1000.
    >>> a.metadata
    {'samplingrate': 1000.0}
    >>> a.metadata.update({'starttime': '12:00:00', 'electrodes': [2, 5]})
    >>> a.metadata
    {'electrodes': [2, 5], 'samplingrate': 1000.0, 'starttime': '12:00:00'}
    >>> a.metadata['starttime'] = '13:00:00'
    >>> a.metadata
    {'electrodes': [2, 5], 'samplingrate': 1000.0, 'starttime': '13:00:00'}
    >>> del a.metadata['starttime']
    a.metadata
    {'electrodes': [2, 5], 'samplingrate': 1000.0}

Since JSON is used to store the metadata, you cannot store arbitrary
python objects. You can only store:

-  strings
-  numbers
-  booleans (True/False)
-  None
-  lists
-  dictionaries with string keys


Installation
------------

Darr depends on Python 3.6 or higher and NumPy 1.12 or higher.

Install Darr from PyPI::

    $ pip install darr



Status
------
Darr is relatively new, and therefore in its alpha stage. It is being used in
practice in the lab, and test coverage is over 90%, but first beta release will
have to wait until test coverage is near 100% and the API is more stable. The
naming of some functions/methods may still change.


Rationale
---------
There are many great formats for storing scientific data. However, the
advantages they offer go hand in hand with complexity and dependence
on external libraries, or on specific knowledge that is not included with
the data. This is necessary and tolerable in specific use cases. Yet based on
my own experience, in many cases life is a lot easier if data is stored in a
way that is simple and self-explanatory. You want to be able to use the data
without  complications in different environments, without having to install
special libraries or having to look up things. You also want to share data
without any hassle with your colleagues, who work with, say, R instead of
Python. Sometimes you want to try out an algorithm that someone wrote in
Matlab, and you do not want to have to start exporting large data sets into
some different format. These things happen all the time and should be simple
and painless. Unfortunately they are not (see this `blog by Cyrille Rossant
<http://cyrille.rossant.net/moving-away-hdf5/>`__ that echos my own
experiences), which is why I wrote Darr.

The **first objective of Darr** is to help you save and use numeric data
arrays from within Python in a way that makes them trivially easy to use in
different analysis environments. Darr is not a file format, but a way of saving
numerical data arrays that maximizes readability.

Darr stores the data itself in a flat binary file. This is a future-proof
way of storing numeric data, as long as clear information is provided on how
the binary data is organized. There is no header; information about the
organization of the data is provided in separate text files that are both
human- and computer-readable. For a variety of current analysis tools Darr
helps you make your data even more accessible as it generates a README text
file that, in addition to explaining the format, contains example code of how
to read the data. E.g. Python/NumPy (without the Darr library), R, Julia,
MatLab/Octave, and Mathematica. Just copy and paste the code in the README to
read the data. Every array that you save can be simply be provided as such to
your colleagues with minimal explanation.

The combination of flat binary and text files leads to a
self-documenting format that anyone can easily explore on any computer,
operating system, and programming language, without installing
dependencies, and without any specific pre-existing knowledge on the
format. In decades to come, your files are much more likely to be
widely readable in this format than in specific formats such as
`HDF5 <https://www.hdfgroup.org/>`__ or
`.npy <https://docs.scipy.org/doc/numpy-dev/neps/npy-format.html>`__.

The **second objective of Darr** is to provide memmory-mapped access to these
stored arrays. In many science applications data arrays can be very large.
It is not always neccesary or even possible to load the whole array in RAM for
analysis. For example, long sound or electrophysiology recordings.
Memmory-mapped arrays provide a very fast, easy and efficient way of working
with such data.

There are of course also disadvantages to Darr's approach.

-  Although the data is widely readable by many scientific analysis
   tools and programming languages, it lacks the ease of 'double-click
   access' that specific data file formats may have. For example, if
   your data is a sound recording, saving it in '.wav' format enables
   you to directly open it in any audio program.
-  To keep things as simple as possible, Darr does not use
   compression. If you are archiving your data and want to minimize disk
   space usage you can compress the data files with a general compression
   tool.
-  Your data is not stored in one file, but in a directory that contains
   3-4 files (depending if you save metadata), at least 2 of which are
   small text files (~150 b - 1.7 kb). This has two disadvantages:

   -  It is less ideal when transferring data, for example by email. You
      may want to archive them into a single file first (zip, tar).
   -  In many file systems, files take up a minimum amount of disk space
      (normally 512 b - 4 kb) even if the data they contain is not that
      large. Darr's way of storing data is thus space-inefficient if
      you have zillions of very small data arrays stored separately.


Contributing
------------

Any help / suggestions / ideas / contributions are very welcome and
appreciated. For any comment, question, or error, please open an
`issue <https://github.com/gjlbeckers-uu/Darr/issues>`__ or propose a
`pull <https://github.com/gjlbeckers-uu/Darr/pulls>`__ request on
GitHub.

Code can be found on GitHub: https://github.com/gjlbeckers-uu/Darr

Testing
-------

To run the test suite:

.. code:: python

    >>> import darr as da
    >>> da.test()
    .......................................................
    ----------------------------------------------------------------------
    Ran 55 tests in 2.181s

    OK
    <unittest.runner.TextTestResult run=53 errors=0 failures=0>

Other interesting projects
--------------------------

-  `exdir <https://github.com/CINPLA/exdir/>`__
-  `h5py <https://github.com/h5py/h5py>`__
-  `pytables <https://github.com/PyTables/PyTables>`__
-  `zarr <https://github.com/zarr-developers/zarr>`__

.. |Travis Status| image:: https://travis-ci.org/gbeckers/Darr.svg?branch=master
   :target: https://travis-ci.org/gbeckers/Darr?branch=master
.. |Appveyor Status| image:: https://ci.appveyor.com/api/projects/status/github/gbeckers/darr?svg=true
   :target: https://ci.appveyor.com/project/gbeckers/darr
.. |PyPy version| image:: https://img.shields.io/badge/pypi-v0.1.3-orange.svg
   :target: https://pypi.org/project/darr/
.. |Coverage Status| image:: https://coveralls.io/repos/github/gbeckers/Darr/badge.svg?branch=master
   :target: https://coveralls.io/github/gbeckers/Darr?branch=master
.. |Docs Status| image:: https://readthedocs.org/projects/darr/badge/?version=latest
   :target: https://darr.readthedocs.io/en/latest/
