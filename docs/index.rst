.. Darr documentation master file, created by
   sphinx-quickstart on Sat Feb 17 16:29:23 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Darr
====

|Github CI Status| |PyPi version| |Conda Forge| |Codecov Badge| |Docs Status|
|Zenodo Badge|

Darr is a Python science library that allows you to work efficiently with
potentially very large, disk-based Numpy arrays that are widely readable and
self-documented. Documentation includes copy-paste ready code to read arrays
in many popular data science languages such as R, Julia, Scilab, IDL,
Matlab, Maple, and Mathematica, or in Python/Numpy without Darr. Without
exporting them and with minimal effort.

Universal readability of data is a pillar of good scientific practice. It is
also generally a good idea for anyone who wants to flexibly move between
analysis environments, who wants to save data for the longer term, or who
wants to share data with others without spending much time on figuring out
and/or explaining how the receiver can read it. No idea how to read your
7-dimensional uint32 numpy array in Matlab to quickly try out an algorithm
your colleague wrote? No worries, a quick copy-paste of code from the array
documentation is all that is needed to read your data in, e.g. R or Matlab
(see `example
<https://github.com/gbeckers/Darr/tree/master/examplearrays/arrays/array_int32_2D.darr>`__).
As you work with your array, its documentation is automatically kept up to
date. No need to export anything, make notes, or to provide elaborate
explanation. No looking up things. No dependence on complicated formats or
specialized libraries for reading you data elsewhere later.

In essence, Darr makes it trivially easy to share your numerical arrays with
others or with yourself when working in different computing environments,
and stores them in a future-proof way.

More rationale for a tool-independent approach to numeric array storage is
provided `here <https://darr.readthedocs.io/en/latest/rationale.html>`__.

Under the hood, Darr uses NumPy memory-mapped arrays, which is a widely
established and trusted way of working with disk-based numerical data, and
which makes Darr fully NumPy compatible. This enables efficient out-of-core
read/write access to potentially very large arrays. In addition to automatic
documentation, Darr adds other functionality to NumPy's memmap, such as easy
the appending and truncating of data, support for ragged arrays, the ability
to create arrays from iterators, and easy use of metadata. Flat binary files
and (JSON) text files are accompanied by a README text file that explains how
the array and metadata are stored (`see example arrays
<https://github.com/gbeckers/Darr/tree/master/examplearrays/>`__).

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
   Python (without Darr), R, Julia, Scilab, Octave/Matlab, GDL/IDL, and
   Mathematica
   (see `example array
   <https://github.com/gbeckers/Darr/tree/master/examplearrays/arrays/array_int32_2D.darr>`__).
-  Disk-persistent array data is directly accessible through `NumPy
   indexing <https://numpy.org/doc/stable/reference/arrays.indexing.html>`__
   and may be larger than RAM
-  Easy and efficient appending of data (`see example <https://darr.readthedocs.io/en/latest/tutorialarray.html#appending-data>`__).
-  Supports ragged arrays.
-  Easy use of metadata, stored in a widely readable separate
   JSON text file (`see example
   <https://darr.readthedocs.io/en/latest/tutorialarray.html#metadata>`__).
-  Many numeric types are supported: (u)int8-(u)int64, float16-float64,
   complex64, complex128.
-  Integrates easily with the `Dask <https://dask.pydata.org/en/latest/>`__
   library for out-of-core computation on very large arrays.
-  Minimal dependencies, only `NumPy <http://www.numpy.org/>`__.

Limitations
-----------
- No `structured (record) arrays <https://numpy.org/doc/stable/user/basics.rec.html>`__
  supported yet, just
  `ndarrays <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`__
- No string data, just numeric.
- No compression, although compression for archiving purposes is supported.
- Uses multiple files per array, as binary data is separated from text
  documentation and metadata. This can be a disadvantage in terms of storage
  space if you have very many very small arrays.

Darr officially depends on Python 3.9 or higher. Older versions may work
(probably >= 3.6) but are not tested anymore.

Install Darr from PyPI::

    $ pip install darr

Or, install Darr via conda::

    $ conda install -c conda-forge darr

To install the latest development version, use pip with the latest GitHub
master::

    $ pip install git+https://github.com/gbeckers/darr@master


Status
------
Darr is relatively new, and therefore in its beta stage. It is being used in
practice in the lab, and test coverage is allmost 100%, but first official
release will have to wait until the API is more stable. The naming of some
functions/methods may still change.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   tutorialarray
   tutorialraggedarray
   rationale
   readcode
   readability
   troubleshooting
   contributing
   testing
   releasenotes
   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. |Github CI Status| image:: https://github.com/gbeckers/Darr/actions/workflows/python_package.yml/badge.svg
   :target: https://github.com/gbeckers/Darr/actions/workflows/python_package.yml
.. |PyPi version| image:: https://img.shields.io/badge/pypi-0.6.3-orange.svg
   :target: https://pypi.org/project/darr/
.. |Conda Forge| image:: https://anaconda.org/conda-forge/darr/badges/version.svg
   :target: https://anaconda.org/conda-forge/darr
.. |Docs Status| image:: https://readthedocs.org/projects/darr/badge/?version=stable
   :target: https://darr.readthedocs.io/en/stable/
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


Darr is BSD licensed (BSD 3-Clause License). (c) 2017-2025, Gabriël
Beckers