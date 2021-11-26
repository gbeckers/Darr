Rationale
=========

There are many great formats for storing scientific data. However, the
advantages they offer go hand in hand with complexity and dependence on
external libraries, or on specific knowledge that is not included with the
data. This is necessary and tolerable in specific use cases. Yet, it can be
a hindrance when sharing data with other people who work with different
tools. Complex data formats can even hinder you in exploring your own data,
when you use different tools for different types of analyses, or just when
you want to have a look at that data you worked on a few years ago, and
you don't have the old analysis environment available any more.

In many cases life as a scientist is a lot easier if data is stored in a way
that is simple and self-explanatory. You want to be able to use the data
without complications in different environments without having to install
special libraries or having to look up things. You also want to share data
without any hassle with your colleagues, who work with, say, R
instead of Python. Sometimes you want to try out an algorithm that someone
wrote in Matlab, but you do not want to export large amounts of data into
some different format, or even spend time on figuring out how to do this.
These things often could be, and should be simple and painless. Unfortunately
they often are not (see this
`blog by Cyrille Rossant <http://cyrille.rossant.net/moving-away-hdf5/>`__
that echos my own experiences). This is why Darr was created.

The **first objective of Darr** is to provide an easy way of working with
with numeric data arrays and metadata, without having to worry about the
things above. Data are persistent on disk in a self-explaining way, making
them trivially easy to access in different analysis environments without
needing additional explanation of how data is stored.

Darr stores the numeric array data in a flat binary file (i.e. no header).
This is a future-proof way of storing numeric data, as long as clear
information is  provided on how the binary data is organized. Information
about the organization of the data is provided in separate text-based
files that are both human- and computer-readable. For a variety of current
analysis tools, Darr even provides example code of how to read the data. E.g.
Python/NumPy (without the Darr library), R, Julia, MatLab/Octave, and
Mathematica. Just copy and paste the code in the README to read the data.
Every array that you create can be simply be provided as such to others with
minimal explanation.

The combination of flat binary and text files leads to a
self-documenting format that anyone can easily explore on any computer,
operating system, and programming language, without installing
dependencies, and without any specific pre-existing knowledge on the
format or reading long format specifications. In decades to come, your files
are much more likely to be widely readable in this format than in specific
formats such as `HDF5 <https://www.hdfgroup.org/>`__ or
`.npy <https://docs.scipy.org/doc/numpy-dev/neps/npy-format.html>`__.

The **second objective of Darr** is to provide direct, out-of-core access to
these disk-persistent arrays. In many science applications data arrays can be
very large. It is not always necessary or even possible to load the whole
array in RAM for analysis. For example, long sound or brain activity
recordings. Darr provide a very fast, easy and efficient way of working
with such data.

In principle, working with Darr arrays is very similar to working with NumPy
memmory-mapped arrays (which it uses under the hood), but in addition it
provides self-documentation, easy use of metadata, append functionality, ragged
arrays, and archiving functionality.

There are of course also disadvantages to Darr's approach.

-  To keep things as simple as possible, Darr does not provide direct access
   to compressed data. However, it does provide an `archive` method that
   compresses data into one file, for archiving.
-  Your data is not stored in one file, but in a directory that contains
   3-4 files (depending if you save metadata), at least 2 of which are
   small text files (~150 b - 1.7 kb). In many file systems, files take up a
   minimum amount of disk space (normally 512 b - 4 kb) even if the data
   they contain is not that large. Darr's way of storing data is thus
   space-inefficient if you have zillions of very small, non-uniform data
   arrays stored separately.

**Other interesting projects**

-  `asdf <https://github.com/asdf-format/asdf>`__
-  `exdir <https://github.com/CINPLA/exdir/>`__
-  `h5py <https://github.com/h5py/h5py>`__
-  `pyfbf <https://github.com/davidh-ssec/pyfbf>`__
-  `pytables <https://github.com/PyTables/PyTables>`__
-  `zarr <https://github.com/zarr-developers/zarr>`__
