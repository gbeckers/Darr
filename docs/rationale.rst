Rationale
=========

There are many great formats for storing scientific data. However, the
advantages they offer go hand in hand with complexity and dependence on
external libraries, or on specific knowledge that is not included with the
data. This is necessary and tolerable in specific use cases. Yet, in many
cases life as a scientist is a lot easier if data is stored in a way that is
simple and self-explanatory. You want to be able to use the data without
complications in different environments without having to install special
libraries or having to look up things. You also want to share data without
any hassle with your colleagues, who work with, say, R instead of Python.
Sometimes you want to try out an algorithm that someone wrote in Matlab,
and you do not want to have to start exporting large data sets into some
different format. These things should be simple and painless. Unfortunately
they are not (see this `blog by Cyrille Rossant <http://cyrille.rossant
.net/moving-away-hdf5/>`__ that echos my own experiences), which is why I
wrote Darr.

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

**Other interesting projects**

-  `exdir <https://github.com/CINPLA/exdir/>`__
-  `h5py <https://github.com/h5py/h5py>`__
-  `pytables <https://github.com/PyTables/PyTables>`__
-  `zarr <https://github.com/zarr-developers/zarr>`__
