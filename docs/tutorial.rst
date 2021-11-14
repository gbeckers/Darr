Tutorial
========

.. contents:: Table of Contents
    :depth: 3

.. _access:

Accessing an existing array
---------------------------

.. code:: python

    >>> import darr
    >>> a = darr.Array('data.darr')
    >>> a
    darr array([[1., 2., 3., ..., 97., 98., 99.],
                [0., 0., 0., ..., 0., 0., 0.]]) (r)

If you intend to overwrite (part of) the data or append data (see below how)
you need to specify that and set 'accesmode' to 'r+'.

.. code:: python

    >>> import darr
    >>> a = darr.Array('data.darr', accessmode='r+')
    >>> a
    darr array([[1., 2., 3., ..., 97., 98., 99.],
                [0., 0., 0., ..., 0., 0., 0.]]) (r+)

.. _creating:

Creating an array
-----------------

.. code:: python

    >>> import darr
    >>> a = darr.create_array('a1.darr', shape=(2,1024))
    >>> a
    darr array([[0., 0., 0., ..., 0., 0., 0.],
                [0., 0., 0., ..., 0., 0., 0.]]) (r+)

The default is to fill the array with zeros (of type float64) but this
can be changed by the 'fill' and 'fillfunc' parameters. See the api.

The data is now stored on disk in a directory named 'a1.darr', containing
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

To see the files that correspond to a Darr array, see the example arrays in
the source `repo <https://github.com/gbeckers/Darr/tree/master/examplearrays>`__.

Note that this way Darr arrays are intended to be widely and easily readable
without Darr or Python, but the easiest of course is still to use Darr if that
is available.

.. _numptype:

To specify the numeric type, use the dtype argument:

.. code:: python

    >>> a = darr.create_array('a2.darr', shape=(2,1024), dtype='uint8')
    >>> a
    darr array([[0, 0, 0, ..., 0, 0, 0],
                [0, 0, 0, ..., 0, 0, 0]], dtype=uint8) (r+)

.. _fromnumpy:

Creating an array from a NumPy array or a sequence
--------------------------------------------------

.. code:: python

    >>> import numpy as np
    >>> na = np.ones((2,1024))
    >>> a = darr.asarray('a3.darr', na)
    >>> a
    darr array([[ 1.,  1.,  1., ...,  1.,  1.,  1.],
                [ 1.,  1.,  1., ...,  1.,  1.,  1.]]) (r)

This also works for anything that can be converted into a numpy array, such
as lists, tuples.

Creating an array from an iterable
----------------------------------
Sometimes you have something that produces values in chunks. Say output from
a filter over a long signal. The 'asarray' method reads iterables:

.. code:: python

    >>> def yield_values():
    ...     yield [1,2]
    ...     yield [3,4]
    ...     yield [5,6]
    >>> b = darr.asarray('b.darr', yield_values())
    >>> b
    darr array ([1, 2, 3, 4, 5, 6]) (r)

.. _readdata:

Reading data
------------

The disk-based array can be used to read data into RAM using NumPy indexing.

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

    >>> a.set_accessmode('r+')
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
in the disk-based files. This is a big plus in many situations. Think
for example of saving data as they are generated by an instrument. A
restriction is that you can only append to the first axis:

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
    >>> a = darr.create_array('ar1.darr', shape=(1024**2), fill=2.5)
    >>> a
    darr array([2.5, 2.5, 2.5, ..., 2.5, 2.5, 2.5]) (r+)
    >>> with a.open_array():
    ...     dara = dask.array.from_array(a, chunks=(512))
    ...     ((dara + 1) / 2).store(a)
    >>> a
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

Darr automatically provides code to read the array in different languages (e.g.
Matlab, R, Julia, Mathematica) in the README that comes with it, but
you can also get that code on-the-fly:

.. code:: python

    >>> print(a.readcode('mathematica'))
    a = BinaryReadList["arrayvalues.bin", "Real64", ByteOrdering -> -1];
    a = ArrayReshape[a, {2, 1024}];

Just copy-paste the output code in, e.g., Mathematica, access you data from
there.

For Darr Arrays, you can choose from the following languages:

- idl: for IDL/GDL
- julia_ver0: for Julia, versions < 1.0
- julia_ver1: for Julia, versions > 1.0
- mathematica: for Mathematica
- matlab: for Matlab or Octave
- maple: for Maple
- numpy: for Numpy (without Darr)
- numpymemmap: for Numpy, using memmap (for large arrays)
- R: for R

Note that not every numeric type is readable in all languages. For example
float16 cannot be read in Matlab, and Darr will not produce code for it.

Darr Ragged Arrays do not support all these languages yet.