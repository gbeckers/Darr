Rationale
=========

There are many great formats for storing scientific data. However, the
advantages they offer go hand in hand with complexity and dependence on
external libraries, or on specific knowledge that is not included with the
data. This is necessary and tolerable in specific use cases. Yet, it can be
a hindrance when sharing data with other people who work with different
tools. Complex data formats can even hinder in exploring your own data,
when using different tools for different types of analyses, or just when
trying to quickly read the data you worked on a few years ago without having
the software at hand to do so.

And the thing is, often your data just exists of (multi-dimensional) arrays of
numbers with some metadata, which in itself does not have to be represented in
a complex and cryptic way. Life as a scientist is a lot easier if such data
were stored in a way that is simple and self-explanatory. This allows you and
others to use the data without complications in different environments without
having to install special libraries or having to look up things. It would also
enable you to share data without any hassle with your colleagues, who work
with, say, R instead of Python. Sometimes you want to try out an algorithm that
someone wrote in Matlab, but you do not want to export large amounts of data
into some different format, or even spend time on figuring out how to do this.
Indeed, why export gigabytes of data for just to yield the exact same data
but now with a slightly different header? Often, these things could be, and
should be, simple and painless, but unfortunately they often are not (see this
`blog by Cyrille Rossant <http://cyrille.rossant.net/moving-away-hdf5/>`__
that echos my own experiences).

Data that is difficult to read will be read less, and, as a result, will be an
impediment to scientific progress. This is why Darr was created.

First objective of Darr
-----------------------

The first objective of Darr is to provide an easy way of working with
with numeric data arrays and metadata, without having to worry about the
things above. Data are persistent on disk in a tool-independent way and
include documention, making it trivially easy to access in different analysis
environments.

Darr stores the numeric array data in a flat binary file (i.e. no header).
This is a future-proof way of storing numeric data, as long as clear
information is  provided on how the binary data is organized. Information
about the organization of the data is provided in separate text-based
files that are both human- and computer-readable. For a variety of current
analysis tools, Darr even provides example code of how to read the data. E.g.
Python/NumPy (without the Darr library), R, Julia, MatLab/Octave, and
Mathematica (see :doc:`here <readcode>`). Just a quick copy-paste of the code
in the README is enough to read your data in any of those environments and
start working with them. Every array that you work with can be simply be
provided as such to others with minimal explanation.

The combination of flat binary and text files leads to a self-documenting
format that anyone can easily explore on any computer, operating system, and
programming language, without installing dependencies, and without any
specific pre-existing knowledge on the format or reading long format
specifications. In decades to come, your files are much more likely to be
widely readable in this format than in specialized formats such as
`HDF5 <https://www.hdfgroup.org/>`__ or
`npy <https://docs.scipy.org/doc/numpy-dev/neps/npy-format.html>`__.

Second objective of Darr
------------------------

The second objective of Darr is to provide direct, out-of-core access to
these disk-persistent arrays. In many science applications data arrays can be
very large. It is not always necessary or even possible to load the whole
array in RAM for analysis. For example, long sound or brain activity
recordings. Darr provides a very fast, easy and efficient way of working
with such data.

In principle, working with Darr arrays is very similar to working with NumPy
memmory-mapped arrays (which it uses under the hood), but in addition it
provides self-documentation including reading code snippets for different
languages, easy use of metadata, append functionality, ragged arrays, and
archiving functionality.

Potential disadvantages
-----------------------

There may also be disadvantages to Darr's approach.

-  To keep things as simple as possible, Darr does not provide direct access
   to compressed data. However, it does provide an `archive` method that
   compresses data into one file, for archiving.
-  Your data is not stored in one file, but in a directory that contains
   3-4 files (depending if you save metadata), at least 2 of which are
   small text files (~150 b - 1.7 kb). In many file systems, files take up a
   minimum amount of disk space (normally 512 b - 4 kb) even if the data
   they contain is not that large. Darr's way of storing data is thus
   space-inefficient if you have zillions of very small data arrays stored
   separately.
