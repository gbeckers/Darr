Darr
====

|Github CI Status| |Appveyor Status| |PyPi version| |Conda Forge|
|Codecov Badge| |Docs Status| |Zenodo Badge|

Darr is a Python science library for working efficiently with potentially very
large Numpy arrays that persist on disk in an open format and that are
self-documented to make them universally readible. Universal readability is a
pillar of good scientific practice, but also generally a good idea for anyone
who wants to flexibly move between analysis environments, who wants to save
data for the longer term, or who wants to share data with others without
spending much time on figuring out how the receiver can read it. As you work
with you arrays, Darr arrays are automatically kept up to date with a complete
and human-readable explanation of how the data is stored, as well as
copy-paste-ready code to read the array in languages such as R, Julia, IDL,
Matlab, Maple, and Mathematica, or in Python/Numpy without Darr (see `example
<https://github.com/gbeckers/Darr/tree/master/examplearrays/arrays/array_int32_2D.darr>`__).
More rationale for a tool-independent approach to numeric array storage is
provided `here <https://darr.readthedocs.io/en/latest/rationale.html>`__.

Under the hood, Darr uses NumPy memory-mapped arrays, which is a widely
established and trusted way of working with disk-based numerical data, and
which makes Darr fully NumPy compatible. This enables efficient out-of-core
read/write access to potentially very large arrays. In addition to
automatic documentation, Darr adds other functionality to NumPy's memmap,
such as easy appending and truncating data, support for ragged arrays,
the ability to create arrays from iterators, and easy use of metadata.

Flat binary files and (JSON) text files are accompanied by a README text file
that explains how the array and metadata are stored (`see example arrays
<https://github.com/gbeckers/Darr/tree/master/examplearrays/>`__).
It is trivially easy to share your arrays with others or with yourself when
working in different computing environments because they always contains clear
documentation of the specific data at hand, including code to read it.
Does your colleague want to try out an interesting algorithm in R or Matlab
on your arrays?  No need to export anything or to provide elaborate
explanation. No dependence on complicated formats or specialized libraries.
No looking up things. A copy-paste of a few lines of code from the
documentation stored with the data is sufficient.

See this `tutorial <https://darr.readthedocs.io/en/latest/tutorialarray.html>`__
for a brief introduction, or the
`documentation <http://darr.readthedocs.io/>`__ for more info.

Darr is currently pre-1.0, still undergoing development. It is open source and
freely available under the `New BSD License
<https://opensource.org/licenses/BSD-3-Clause>`__ terms.

Features
--------
-  Data is stored purely based on flat binary and text files, maximizing
   universal readability.
-  Automatic self-documention, including copy-paste ready code snippets for
   reading the array in a number of popular data analysis environments, such as
   Python (without Darr), R, Julia, Octave/Matlab, GDL/IDL, and Mathematica
   (see `example array
   <https://github.com/gbeckers/Darr/tree/master/examplearrays/arrays/array_int32_2D.darr>`__).
-  Disk-persistent array data is directly accessible through `NumPy
   indexing <https://numpy.org/doc/stable/reference/arrays.indexing.html>`__
   and may be larger than RAM
-  Easy and efficient appending of data.
-  Supports ragged arrays.
-  Easy use of metadata, stored in a widely readable separate
   `JSON <https://en.wikipedia.org/wiki/JSON>`__ text file.
-  Many numeric types are supported: (u)int8-(u)int64, float16-float64,
   complex64, complex128.
-  Integrates easily with the `Dask <https://dask.pydata.org/en/latest/>`__
   library for out-of-core computation on very large arrays.
-  Minimal dependencies, only `NumPy <http://www.numpy.org/>`__.

Con's:

-  No compression, although compression for archiving purposes is supported.

Installation
------------

Darr depends on Python 3.6 or higher and NumPy 1.12 or higher.

Install Darr from PyPI::

    $ pip install darr

Or, install Darr via conda::

    $ conda install -c conda-forge darr

To install the latest development version, use pip with the latest GitHub
master::

    $ pip install git+https://github.com/gbeckers/darr@master


Documentation
-------------
See the `documentation <http://darr.readthedocs.io/>`_ for more information.

Contributing
------------
Any help / suggestions / ideas / contributions are welcome and very much
appreciated. For any comment, question, or error, please open an issue or
propose a pull request.


Other interesting projects
--------------------------
If Darr is not exactly what you are looking for, have a look at these projects:

-  `asdf <https://github.com/asdf-format/asdf>`__
-  `exdir <https://github.com/CINPLA/exdir/>`__
-  `h5py <https://github.com/h5py/h5py>`__
-  `pyfbf <https://github.com/davidh-ssec/pyfbf>`__
-  `pytables <https://github.com/PyTables/PyTables>`__
-  `zarr <https://github.com/zarr-developers/zarr>`__



Darr is BSD licensed (BSD 3-Clause License). (c) 2017-2022, Gabriël
Beckers

.. |Github CI Status| image:: https://github.com/gbeckers/Darr/actions/workflows/python_package.yml/badge.svg
   :target: https://github.com/gbeckers/Darr/actions/workflows/python_package.yml
.. |Appveyor Status| image:: https://ci.appveyor.com/api/projects/status/github/gbeckers/darr?svg=true
   :target: https://ci.appveyor.com/project/gbeckers/darr
.. |PyPi version| image:: https://img.shields.io/badge/pypi-0.5.4-orange.svg
   :target: https://pypi.org/project/darr/
.. |Conda Forge| image:: https://anaconda.org/conda-forge/darr/badges/version.svg
   :target: https://anaconda.org/conda-forge/darr
.. |Docs Status| image:: https://readthedocs.org/projects/darr/badge/?version=stable
   :target: https://darr.readthedocs.io/en/latest/
.. |Repo Status| image:: https://www.repostatus.org/badges/latest/active.svg
   :alt: Project Status: Active – The project has reached a stable, usable state and is being actively developed.
   :target: https://www.repostatus.org/#active
.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/c0157592ce7a4ecca5f7d8527874ce54
   :alt: Codacy Badge
   :target: https://app.codacy.com/app/gbeckers/Darr?utm_source=github.com&utm_medium=referral&utm_content=gbeckers/Darr&utm_campaign=Badge_Grade_Dashboard
.. |Zenodo Badge| image:: https://zenodo.org/badge/151593293.svg
   :target: https://zenodo.org/badge/latestdoi/151593293
.. |Codecov Badge| image:: https://codecov.io/gh/gbeckers/Darr/branch/master/graph/badge.svg?token=BBV0WDIUSJ
   :target: https://codecov.io/gh/gbeckers/Darr
