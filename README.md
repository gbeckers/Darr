dArray
======

[![image](https://travis-ci.org/gbeckers/dArray.svg?branch=master)](https://travis-ci.org/gbeckers/dArray?branch=master)
[![image](https://ci.appveyor.com/api/projects/status/github/gbeckers/darray?svg=true)](https://ci.appveyor.com/project/gbeckers/darray)
[![image](https://img.shields.io/badge/pypi-v0.1.1-orange.svg)](https://pypi.org/project/darray/)
[![Coverage Status](https://coveralls.io/repos/github/gbeckers/dArray/badge.svg?branch=master)](https://coveralls.io/github/gbeckers/dArray?branch=master)

dArray is a Python science library for storing numeric data arrays in a
way that is open, simple, and self-explanatory. It also enables fast
memory-mapped read/write access to such disk-based data, the ability to
append data, and the flexible use of metadata. It is primarily designed
for scientific use cases. Save and use your numeric arrays and metadata
with one line of code while easy, long-term and tool-independent
accessibility is ensured.

To avoid tool-specific data formats, dArray is exclusively based on a
combination of flat binary and text files. It automatically saves a
clear text description of how exactly the data is stored, as well as
example code to read the specific data in a variety of current
scientific data tools.

dArray is open source and freely available under the [New BSD
License](https://opensource.org/licenses/BSD-3-Clause) terms.

Version: 0.1.1 Alpha

dArray is BSD licensed (BSD 3-Clause License). (c) 2017-2018, Gabriël
Beckers

Features
--------

Pro's:

-   **Simple data format** based on **flat binary** and **text** files.
-   Supports **very large data arrays** through **memory-mapped** file
    access.
-   Data read/write access through **NumPy indexing** (see
    [here](https://docs.scipy.org/doc/numpy-1.13.0/reference/arrays.indexing.html)).
-   Data is easily **appendable**.
-   **Human-readable explanation of how the binary data is stored** is
    saved in a README text file.
-   README also contains **examples of how to read the array** in
    popular analysis environments such as Python (without dArray), R,
    Julia, Octave/Matlab, GDL/IDL, and Mathematica.
-   **Many numeric types** are supported: (u)int8-(u)int64,
    float16-float64, complex64, complex128.
-   Easy use of **metadata**, stored in a separate
    [JSON](https://en.wikipedia.org/wiki/JSON) text file.
-   **Minimal dependencies**, only [NumPy](http://www.numpy.org/).
-   **Integrates easily** with the
    [Dask](https://dask.pydata.org/en/latest/) or
    [NumExpr](https://numexpr.readthedocs.io/en/latest/) libraries for
    **numeric computation on very large darrays**.

Con's:

-   **No compression**, although it is of course possible to simply
    compress the darray files with a compression tool for archiving
    purposes.
-   **Multiple files**. The data, the data description, and the metadata
    are stored in separate files, though all within a single directory.
-   **Inefficient (storage-wise) for very small arrays**. If you have a
    zillion small arrays, and storage space in a concern, use other
    approaches.

Examples
--------

**Creating an array**

``` {.sourceCode .python}
>>> import darray as da
>>> a = da.create_array('a1.da', shape=(2,1024))
>>> a
>>> array([[0., 0., 0., ..., 0., 0., 0.],
           [0., 0., 0., ..., 0., 0., 0.]]) (r+)
```

The default is to fill the array with zeros (of type float64) but this
can be changed by the 'fill' and 'fillfunc' parameters. See the api.

The data is now stored on disk in a directory named 'ar1.da', containing
a flat binary file ('arrayvalues.bin') and a human-readble
[JSON](https://en.wikipedia.org/wiki/JSON) text file
('arraydescription.json'), with information on the array dimensionality,
layout and numeric type. It also contains a 'README.txt' file explaining
the data format as well as providing instructions on how to read the
array using other tools. For example, it provides the code to read the
array in [Octave](https://www.gnu.org/software/octave/)/Matlab:

``` {.sourceCode .octave}
fileid = fopen('arrayvalues.bin');
a = fread(fileid, [1024, 2], '*float64', 'ieee-le');
fclose(fileid);
```

Or in [R](https://cran.r-project.org/):

``` {.sourceCode .R}
to.read = file("arrayvalues.bin", "rb")
a = readBin(con=to.read, what=numeric(), n=2048, size=8, endian="little")
a = array(data=a, dim=c(1024, 2), dimnames=NULL)
close(to.read)
```

Or in [Julia](https://julialang.org/):

``` {.sourceCode .julia}
fid = open("arrayvalues.bin","r");
x = map(ltoh, read(fid, Float64, (1024, 2)));
close(fid);
```

To see the files that correspond to a dArray array, see
'examplearray.da' in the source
[repo](https://github.com/gjlbeckers-uu/dArray).

**Different numeric type**

``` {.sourceCode .python}
>>> a = da.create_array('a2.da', shape=(2,1024), dtype='uint8')
>>> a
array([[0, 0, 0, ..., 0, 0, 0],
       [0, 0, 0, ..., 0, 0, 0]], dtype=uint8) (r+)
```

**Creating array from NumPy array**

``` {.sourceCode .python}
>>> import numpy as np
>>> na = np.ones((2,1024))
>>> a = da.asarray('a3.da', na)
>>> a
array([[ 1.,  1.,  1., ...,  1.,  1.,  1.],
       [ 1.,  1.,  1., ...,  1.,  1.,  1.]]) (r)
```

**Reading data**

The disk-based array is memory-mapped and can be used to read data into
RAM using NumPy indexing.

``` {.sourceCode .python}
>>> a[:,-2]
array([ 1.,  1.])
```

Note that that creates a NumPy array. The darray itself is not a NumPy
array, nor does it behave like one except for indexing. The simplest way
to use the data for computation is to, read (or view, see below) the
data first as a NumPy array:

``` {.sourceCode .python}
>>> 2 * a[:]
array([[2., 2., 2., ..., 2., 2., 2.],
       [2., 2., 2., ..., 2., 2., 2.]])
```

If your data is too large to read into RAM, you could use the
[Dask](https://dask.pydata.org/en/latest/) or the
[NumExpr](https://numexpr.readthedocs.io/en/latest/) library for
computation (see example below).

**Writing data**

Writing is also done through NumPy indexing. Writing directly leads to
changes on disk. Our example array is read-only because we did not
specify otherwise in the 'asdarray' function above, so we'll set it to
be writable first:

``` {.sourceCode .python}
>>> a.set_accessmode('r+')
>>> a[:,1] = 2.
>>> a
array([[ 1.,  2.,  1., ...,  1.,  1.,  1.],
       [ 1.,  2.,  1., ...,  1.,  1.,  1.]]) (r+)
```

**Efficient I/O**

To get maximum speed when doing multiple operations open a direct view
on the disk-based array so as to opens the underlying files only once:

``` {.sourceCode .python}
>>> with a.view() as v:
...     v[0,0] = 3.
...     v[0,2] = 4.
...     v[1,[0,2,-1]] = 5.
>>> a
array([[ 3.,  2.,  4., ...,  1.,  1.,  1.],
      [ 5.,  2.,  5., ...,  1.,  1.,  5.]]) (r+)
```

**Appending data**

You can easily append data to a darray, which is immediately reflected
in the disk-based files. This is a big plus in many situations. Think
for example of saving data as they are generated by an instrument. A
restriction is that you can only append to the first axis:

``` {.sourceCode .python}
>>> a.append(np.ones((3,1024)))
>>> a
array([[3., 2., 4., ..., 1., 1., 1.],
       [5., 2., 5., ..., 1., 1., 5.],
       [1., 1., 1., ..., 1., 1., 1.],
       [1., 1., 1., ..., 1., 1., 1.],
       [1., 1., 1., ..., 1., 1., 1.]]) (r+)
```

The associated 'README.txt' and 'arraydescription.json' texts files are
also automatically updated to reflect these changes. There is an
'iterappend' method for efficient serial appending. See the api.

**Copying and type casting data**

``` {.sourceCode .python}
>>> ac = a.copy('ac.da')
>>> acf16 = a.copy('acf16.da', dtype='float16')
>>> acf16
array([[3., 2., 4., ..., 1., 1., 1.],
       [5., 2., 5., ..., 1., 1., 5.],
       [1., 1., 1., ..., 1., 1., 1.],
       [1., 1., 1., ..., 1., 1., 1.],
       [1., 1., 1., ..., 1., 1., 1.]], dtype=float16) (r)
```

Note that the type of the array can be changed when copying. Data is
copied in chunks, so very large arrays will not flood RAM memory.

**Larger than memory computation**

For computing with very large darrays, I recommend the
[Dask](https://dask.pydata.org/en/latest/) library, which works nicely
with darray. I'll base the example on a small array though:

``` {.sourceCode .python}
>>> import dask.array
>>> a = da.create_array('ar1.da', shape=(1024**2), fill=2.5, overwrite=True)
>>> a
array([2.5, 2.5, 2.5, ..., 2.5, 2.5, 2.5]) (r+)
>>> dara = dask.array.from_array(a, chunks=(512))
>>> ((dara + 1) / 2).store(a)
>>> a
array([1.75, 1.75, 1.75, ..., 1.75, 1.75, 1.75]) (r+)
```

So in this case we overwrote the data in a with the results of the
computation, but we could have stored the result in a different darray
of the same shape. Dask can do more powerful things, for which I refer
to the [Dask
documentation](https://dask.pydata.org/en/latest/index.html). The point
here is that darrays can be both sources and stores for Dask.

Alternatively, you can use the
[NumExpr](https://numexpr.readthedocs.io/en/latest/) library using a
view of the darray, like so:

``` {.sourceCode .python}
>>> import numexpr as ne
>>> a = da.create_array('a3.da', shape=(1024**2), fill=2.5)
>>> with a.view() as v:
...     ne.evaluate('(v + 1) / 2', out=v)
>>> a
array([1.75, 1.75, 1.75, ..., 1.75, 1.75, 1.75]) (r+)
```

**Metadata**

Metadata can be read and written like a dictionary. Changes correspond
to changes in a human-readable and editable JSON text file that holds
the metadata on disk.

``` {.sourceCode .python}
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
```

Since JSON is used to store the metadata, you cannot store arbitrary
python objects. You can only store:

-   strings
-   numbers
-   booleans (True/False)
-   None
-   lists
-   dictionaries with string keys

Rationale
---------

There are many great formats for storing scientific data. Nevertheless,
the advantages they offer often go hand in hand with complexity and
dependence on external libraries, or on specific knowledge that is not
included with the data. Preferably, however, scientific data is stored
in a way that is simple and self-explanatory. For one thing, this is in
line with the principle of openness and facilitates re-use and
reproducibility of scientific results by others. Additionally,
experience teaches that simple formats and independence of specific
tools are a very good idea, even when just working with your own data
(see this [blog by Cyrille
Rossant](http://cyrille.rossant.net/moving-away-hdf5/) that echos my own
experiences).

The goal of dArray is to help you save and use numeric data arrays from
within Python in a way that is consistent with this idea. It is not a
file format, but a standardized way of saving data that maximizes
readability.

dArray stores the data itself in a flat binary file. This is a
future-proof way of storing numeric data, as long as clear information
is provided on how the binary data is organized. There is no header,
because we want to assume as little a priori knowledge as possible.
Instead, dArray writes the information about the organization of the
data to separate text files.

The combination of flat binary and text files leads to a
self-documenting format that anyone can easily explore on any computer,
operating system, and programming language, without installing
dependencies, and without any specific pre-existing knowledge on the
format. In decades to come, your files are much more likely to be
readable in this format than in specific formats such as
[HDF5](https://www.hdfgroup.org/) or
[.npy](https://docs.scipy.org/doc/numpy-dev/neps/npy-format.html).

For a variety of current analysis tools dArray helps you make your data
even more accessible as it generates a README text file that, in
addition to explaining the format, contains example code of how to read
the data. E.g. Python/NumPy (without the dArray library), R, Julia,
MatLab/Octave, and Mathematica. Just copy and paste the code in the
README to read the data. Every array that you save can be simply be
provided as such to your colleagues with minimal explanation.

There are of course also disadvantages to this approach.

-   Although the data is widely readable by many scientific analysis
    tools and programming languages, it lacks the ease of 'double-click
    access' that specific data file formats may have. For example, if
    your data is a sound recording, saving it in '.wav' format enables
    you to directly open it in any audio program.
-   To keep things as simple as possible, dArray does not use
    compression. Depending on the data, storage can thus take more disk
    space than necessary. If you are archiving your data and insist on
    minimizing disk space usage you can compress the data files with a
    general compression tool that is likely to be still supported in the
    distant future, such as bzip2. Sometimes, compression is used to
    speed up data transmission to the processor cache (see for example
    [blosc](https://github.com/Blosc/c-blosc)). You are missing out on
    that as well. However, in addition to making your data less easy to
    read, this type of compression may require careful tweaking of
    parameters depending on how you typically read and write the data,
    and failing to do so may lead to access that is in fact slower.
-   Your data is not stored in one file, but in a directory that
    contains 3-4 files (depending if you save metadata), at least 2 of
    which are small text files (\~150 b - 1.7 kb). This has two
    disadvantages:
    -   It is less ideal when transferring data, for example by email.
        You may want to archive them into a single file first (zip,
        tar).
    -   In many file systems, files take up a minimum amount of disk
        space (normally 512 b - 4 kb) even if the data they contain is
        not that large. dArray's way of storing data is thus
        space-inefficient if you have zillions of very small data arrays
        stored separately.

Requirements
------------

dArray requires Python 3.6+ and NumPy.

Development and Contributing
----------------------------

This library is developed by Gabriël Beckers. It is being used in
practice in the lab, but first beta release will be done when there
are more unit tests. The naming of some functions/methods may
still change. Any help / suggestions / ideas / contributions are very
welcome and appreciated. For any comment, question, or error, please
open an [issue](https://github.com/gjlbeckers-uu/dArray/issues) or
propose a [pull](https://github.com/gjlbeckers-uu/dArray/pulls) request
on GitHub.

Code can be found on GitHub: <https://github.com/gjlbeckers-uu/dArray>

Testing
-------

To run the test suite:

``` {.sourceCode .python}
>>> import darray as da
>>> da.test()
..............................
----------------------------------------------------------------------
Ran 31 tests in 1.627s

OK
<unittest.runner.TextTestResult run=31 errors=0 failures=0>
```

Other interesting projects
--------------------------

-   [exdir](https://github.com/CINPLA/exdir/)
-   [h5py](https://github.com/h5py/h5py)
-   [pytables](https://github.com/PyTables/PyTables)
-   [zarr](https://github.com/zarr-developers/zarr)

