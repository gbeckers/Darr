.. Darr documentation master file, created by
   sphinx-quickstart on Sat Feb 17 16:29:23 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Darr
====


|Travis Status| |Appveyor Status| |PyPi version| |Conda Forge| |Coverage Status|
|Docs Status| |Repo Status| |PyUp Badge|

Darr is a Python science library for working efficiently with potentially
large, disk-based numeric arrays and metadata, without depending on
tool-specific or complicated data formats. Data is persistent on disk in a
self-explanatory way, making it trivially easy to share it and use it in
different environments. No need to export anything or to provide much
explanation, and no need to assume that a specific tool will be available.

Tool-independent and easy access to data is in line with good scientific
practice as it promotes wide and long-term availability, to others and
to yourself. More rationale for this approach is provided
`here <https://darr.readthedocs.io/en/latest/rationale.html>`__.

Darr supports efficient out-of-core read/write/append access and is based
on universally readable flat binary files and automatically generated text
files that explain precisely the nature of your array data and how it is
stored. It also automatically generates specific code that reads the data in
a variety of  current scientific data tools such as Python, R, Julia, IDL,
Matlab, Maple, and Mathematica (see
`example array <https://github.com/gbeckers/Darr/tree/master/examplearrays/examplearray_uint64.darr>`__).

Darr currently supports numerical N-dimensional arrays, and experimentally
supports numerical ragged arrays, i.e. a series of arrays in which one
dimension varies in length.

See this `tutorial <https://darr.readthedocs.io/en/latest/tutorial.html>`__
for a brief introduction, or the
`documentation <http://darr.readthedocs.io/>`__ for more info.

Darr is currently pre-1.0, still undergoing significant development. It is
open source and freely available under the `New BSD License
<https://opensource.org/licenses/BSD-3-Clause>`__ terms.

Features
--------

Pro's:

-  Data persists on-disk, purely based on flat binary and text files,
   **tool independence**.
-  README text file with **human-readable explanation** of how the binary data
   is stored.
-  README includes **examples of how to read the array** in a number of popular
   data analysis environments, such as Python (without Darr), R, Julia,
   Octave/Matlab, GDL/IDL, and Mathematica.
-  Works with **data arrays larger than RAM**.
-  Data read/write access is simple and powerful through **NumPy indexing**
   (see
   `here <https://docs.scipy.org/doc/numpy-1.13.0/reference/arrays.indexing.html>`__).
-  Data is easily **appendable**.
-  **Many numeric types** are supported: (u)int8-(u)int64, float16-float64,
   complex64, complex128.
-  Easy use of **metadata**, stored in a separate
   `JSON <https://en.wikipedia.org/wiki/JSON>`__ text file.
-  **Minimal dependencies**, only `NumPy <http://www.numpy.org/>`__.
-  Integrates easily with the `Dask <https://dask.pydata.org/en/latest/>`__
   library for out-of-core **computation on very large arrays**.
-  Supports **ragged arrays** (still experimental).

Con's:

-  **No compression**, although compression for archiving purposes is
   supported.

Darr depends on Python 3.6 or higher and NumPy 1.12 or higher.

Install Darr from PyPI::

    $ pip install darr

Or, install Darr via conda::

    $ conda install -c conda-forge darr

To install the latest development version, use pip with the latest GitHub
master::

    $ pip install git+https://github.com/gbeckers/darr@master


Status
------
Darr is relatively new, and therefore in its alpha stage. It is being used in
practice in the lab, and test coverage is allmost 100%, but first beta release
will have to wait until the API is more stable. The naming of some
functions/methods may still change.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   tutorial
   rationale
   contributing
   testing
   releasenotes
   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. |Travis Status| image:: https://travis-ci.com/gbeckers/Darr .svg?branch=master
   :target: https://travis-ci.com/gbeckers/Darr?branch=master
.. |Appveyor Status| image:: https://ci.appveyor.com/api/projects/status/github/gbeckers/darr?svg=true
   :target: https://ci.appveyor.com/project/gbeckers/darr
.. |PyPi version| image:: https://img.shields.io/badge/pypi-0.3.3-orange.svg
   :target: https://pypi.org/project/darr/
.. |Conda Forge| image:: https://anaconda.org/conda-forge/darr/badges/version.svg
   :target: https://anaconda.org/conda-forge/darr
.. |Coverage Status| image:: https://coveralls.io/repos/github/gbeckers/Darr/badge.svg?branch=master
   :target: https://coveralls.io/github/gbeckers/Darr?branch=master
.. |Docs Status| image:: https://readthedocs.org/projects/darr/badge/?version=stable
   :target: https://darr.readthedocs.io/en/stable/
.. |Repo Status| image:: https://www.repostatus.org/badges/latest/active.svg
   :alt: Project Status: Active – The project has reached a stable, usable state and is being actively developed.
   :target: https://www.repostatus.org/#active
.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/c0157592ce7a4ecca5f7d8527874ce54
   :alt: Codacy Badge
   :target: https://app.codacy.com/app/gbeckers/Darr?utm_source=github.com&utm_medium=referral&utm_content=gbeckers/Darr&utm_campaign=Badge_Grade_Dashboard
.. |PyUp Badge| image:: https://pyup.io/repos/github/gbeckers/Darr/shield.svg
   :target: https://pyup.io/repos/github/gbeckers/Darr/
   :alt: Updates

Darr is BSD licensed (BSD 3-Clause License). (c) 2017-2021, Gabriël
Beckers