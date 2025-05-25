Tutorial Array
==============

.. _access:
Accessing an existing array
---------------------------
Darr arrays are represented on disk by a folder with some files in it.
Assume we received an array called 'data.darr'. On disk, the 'data.darr'
folder holds 3-4 files that contain all data and documentation.

::

    data.darr (folder)
    ├── arraydescription.json (file)
    ├── arrayvalues.bin (file)
    ├── metadata.json (file, optional)
    └── README.txt (file)


To work with this array in Darr, just open and assign it to a variable as
follows:

.. code:: python

    >>> import darr
        >>> a = src.open('data.darr')
        >>> a
        darr array([[1., 2., 3., ..., 97., 98., 99.],
                    [0., 0., 0., ..., 0., 0., 0.]]) (r)

    Note that in creating the variable '*a*' above, the array data is
    >>> a = darr.open('data.darr')
    >>> a
    darr array([[1., 2., 3., ..., 97., 98., 99.],
                [0., 0., 0., ..., 0., 0., 0.]]) (r)

Note that in creating the variable '*a*' above, the array data is **not** read
into RAM. It can potentially be very large and remains on disk. It will only
be read into RAM as a NumPy array after indexing '*a*'.

.. code:: python

    >>> a[0,1:4] # returns part of the darr array as a numpy array
    array([2., 3., 4.])

To read it in RAM completely, just index to get the whole thing:

.. code:: python

    >>> b = a[:] # this returns a normal numpy array
    >>> b
    array([[1., 2., 3., ..., 97., 98., 99.],
           [0., 0., 0., ..., 0., 0., 0.]])

There is no 'close' function because, despite its name,  the 'open' function
used above does not really keep any files open. Darr opens and automatically
closes files under the hood when needed.

.. _creating:

Creating an array from a NumPy array or a sequence
--------------------------------------------------
Use the 'asarray' function. It will take numpy arrays, sequences and
iterables.

.. code:: python

    >>> import numpy as np
    >>> na = np.ones((2,1024))
    >>> a = darr.asarray('a.darr', na)
    >>> a
    darr array([[ 1.,  1.,  1., ...,  1.,  1.,  1.],
                [ 1.,  1.,  1., ...,  1.,  1.,  1.]]) (r)


Creating an array from scratch
------------------------------
Use the 'create_array' function. Particularly useful if you want to create a
gigantic array that does not fit in RAM memory so that creating a NumPy
array first is not possible. The example here uses a small array:

.. code:: python

    >>> import darr
        >>> b = src.create_array('b.darr', shape=(2,1024))
        >>> b
        darr array([[0., 0., 0., ..., 0., 0., 0.],
                    [0., 0., 0., ..., 0., 0., 0.]]) (r+)

    The default is to fill the array with zeros (of type float64) but this
    can be changed by the 'fill' and 'fillfunc' parameters. See the api.
    >>> b = darr.create_array('b.darr', shape=(2,1024))
    >>> b
    darr array([[0., 0., 0., ..., 0., 0., 0.],
                [0., 0., 0., ..., 0., 0., 0.]]) (r+)

The default is to fill the array with zeros (of type float64) but this
can be changed by the 'fill' and 'fillfunc' parameters. See the api.

.. _numptype:

To specify the numeric type, use the dtype argument:

.. code:: python

    >>> c = darr.create_array('c.darr', shape=(2,1024), dtype='uint8')

.. _documentation:

Automatic self-documentation
----------------------------
Array data is stored on disk in a folder, containing a flat binary file
('arrayvalues.bin') and a human-readble
`JSON <https://en.wikipedia.org/wiki/JSON>`__ text file
('arraydescription.json'), with information on the array dimensionality,
layout and numeric type. It also contains a 'README.txt' file explaining
the data format as well as providing instructions on how to read the
array using other tools (see `example
<https://github.com/gbeckers/Darr/tree/master/examplearrays/arrays/array_int32_2D.darr>`__).

For example, it provides the code to read the
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

To see the files that correspond to a Darr array, see the example arrays in
the source `repo <https://github.com/gbeckers/Darr/tree/master/examplearrays>`__.

See :doc:`Reading data in other environments <readcode>` for more information on
the languages that Darr can generate read code snippets for.

Note that this way Darr arrays are widely and easily readable without Darr or
Python, but the easiest for manipulation the data and metadata is of
course to use Darr if that is available.

.. _fromnumpy:


Creating an array from an iterable
----------------------------------
Sometimes you have something that produces values in chunks. Say output from
a filter over a long signal. Or, in a measurement situation, some recording
instrument that yields values.

The 'asarray' method reads iterables:

.. code:: python

    >>> def yield_values():
    ...     yield [1,2]
    ...     yield [3,4]
    ...     yield [5,6]
    >>> d = darr.asarray('d.darr', yield_values())
    >>> d
    darr array ([1, 2, 3, 4, 5, 6]) (r)

.. _readdata:

Reading data
------------

The disk-based array can be read as a numpy array into RAM by using
NumPy indexing.

.. code:: python

    >>> a[:,-2]
    array([ 1.,  1.])

Note that the darr array itself is not a NumPy array, nor does it behave
like one except for indexing. The simplest way to use the data for
computation is to, read (or view, see below) the data first as a NumPy array:

.. code:: python

    >>> 2 * a[:]
    array([[2., 2., 2., ..., 2., 2., 2.],
           [2., 2., 2., ..., 2., 2., 2.]])

If your data is too large to read into RAM, you could use the
`Dask <https://dask.pydata.org/en/latest/>`__ library for
computation (see example below).

.. _writedata:

Writing data
------------

Writing is also done through NumPy indexing. Writing directly leads to
changes on disk. Our example array is read-only because we did not
specify otherwise in the 'asarray' function above, so we'll set it to
be writable first:

.. code:: python

    >>> a.accessmode = 'r+'
    >>> a[:,1] = 2.
    >>> a
    darr array([[ 1.,  2.,  1., ...,  1.,  1.,  1.],
                [ 1.,  2.,  1., ...,  1.,  1.,  1.]]) (r+)


.. _efficientio:

Efficient I/O
-------------

To get maximum speed when doing multiple operations, first open the disk-based
array so as to open and close the underlying files only once:

.. code:: python

    >>> with a.open_array():
    ...     a[0,0] = 3.
    ...     a[0,2] = 4.
    ...     a[1,[0,2,-1]] = 5.
    >>> a
    darr array([[ 3.,  2.,  4., ...,  1.,  1.,  1.],
                [ 5.,  2.,  5., ...,  1.,  1.,  5.]]) (r+)

.. _appending:

Appending data
--------------

You can easily append data to a Darr array, which is immediately reflected
in the disk-based files. The append operation is efficient (in place, unlike
Numpy's append which copies the data to append to). This is a big plus in
many situations. Think for example of saving data by appending as they are
generated by an instrument. A restriction is that you can only append to the
first axis:

.. code:: python

    >>> a.append(np.ones((3,1024)))
    >>> a
    darr array([[3., 2., 4., ..., 1., 1., 1.],
                [5., 2., 5., ..., 1., 1., 5.],
                [1., 1., 1., ..., 1., 1., 1.],
                [1., 1., 1., ..., 1., 1., 1.],
                [1., 1., 1., ..., 1., 1., 1.]]) (r+)

The associated 'README.txt' and 'arraydescription.json' texts files are
also automatically updated to reflect these changes. There is an
'iterappend' method for efficient serial appending. See the api.

.. _copying:

Copying and type casting data
-----------------------------

.. code:: python

    >>> ac = a.copy('ac.darr')
    >>> acf16 = a.copy('acf16.darr', dtype='float16')
    >>> acf16
    darr array([[3., 2., 4., ..., 1., 1., 1.],
                [5., 2., 5., ..., 1., 1., 5.],
                [1., 1., 1., ..., 1., 1., 1.],
                [1., 1., 1., ..., 1., 1., 1.],
                [1., 1., 1., ..., 1., 1., 1.]], dtype=float16) (r)

Note that the type of the array can be changed when copying. Data is
copied in chunks, so very large arrays will not flood RAM memory.

.. _outofcore:

Out of core computation
-----------------------

For computations on larger-than-RAM arrays, I recommend the
`Dask <https://dask.pydata.org/en/latest/>`__ library, which works
nicely with darr. I'll base the example on a small array though:

.. code:: python

    >>> import dask.array
    >>> e = darr.create_array('e.darr', shape=(1024**2), fill=2.5)
    >>> e
    darr array([2.5, 2.5, 2.5, ..., 2.5, 2.5, 2.5]) (r+)
    >>> with e.open_array():
    ...     daskar = dask.array.from_array(e, chunks=(512))
    ...     ((daskar + 1) / 2).store(e)
    >>> e
    darr array([1.75, 1.75, 1.75, ..., 1.75, 1.75, 1.75]) (r+)

So in this case we overwrote the data in a with the results of the
computation, but we could have stored the result in a different darr array
of the same shape. Dask can do more powerful things, for which I refer
to the `Dask documentation <https://dask.pydata.org/en/latest/index
.html>`__. The point here is that darr arrays can be both sources and
stores for Dask.

.. _metadata:

Metadata
--------

Metadata can be read and written like a dictionary. Changes correspond
directly to changes in a human-readable and editable JSON text file that holds
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

Darr tries its best to convert numpy objects in metadata to corresponding
Python objects. I.e. if you have a numpy.float64 object and save it as
metadata, it will be converted to a Python float.

Quickly reading your array in a different language
--------------------------------------------------

Darr automatically provides code snippets to read the array in different
languages (e.g. Matlab, R, Julia, Mathematica) in the README that comes with
it, but you can also get that code on-the-fly, e.g. for Mathematica:

.. code:: python

    >>> print(a.readcode('mathematica'))
    a = BinaryReadList["arrayvalues.bin", "Real64", ByteOrdering -> -1];
    a = ArrayReshape[a, {2, 1024}];

Just copy-paste the output code in Mathematica and access you data from there.

See :doc:`Reading data in other environments <readcode>` for more information.

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
     'numpymemmap',
     'scilab')

Ragged Arrays
-------------

See :doc:`Tutorial RaggedArray <tutorialraggedarray>` for more
information.
