.. Darr documentation master file, created by
   sphinx-quickstart on Sat Feb 17 16:29:23 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Darr
====

|Github CI Status| |Appveyor Status| |PyPi version| |Conda Forge|
|Coverage Status| |Docs Status| |Repo Status| |PyUp Badge|

Darr is a Python science library for disk-based NumPy arrays that
persist in a format that is simple, self-documented and tool-independent.
It enables you to work efficiently with potentially very large arrays, while
keeping your data easily accessible from a wide range of computing
environments. Even if you don't work with very large arrays, Darr is a very
convenient way to store your arrays in a way that keeps them universally
readable and documented, which is in line with good scientific practice. More
rationale for this approach is provided
`here <https://darr.readthedocs.io/en/latest/rationale .html>`__.

Flat binary files and (JSON) text files are accompanied by a README text file
that explains how the array and metadata are stored and how they can
be read. This includes code for reading the array in a variety of current
scientific data tools such as Python, R, Julia, IDL, Matlab, Maple, and
Mathematica. It is trivially easy to share your data with others or with
yourself when working in different computing environments, because it always
contains a clear and specific description of how to read it. Say you quickly
want to run some R code from a colleague on your arrays. No need to export
anything or to provide elaborate explanation. No dependence on complicated
formats or specialized tools. Self-documentation and code examples are
automatically updated as you change your arrays when working with them.

Darr uses NumPy memmory-mapped arrays under the hood, which you can
access directly for full NumPy compatibility and efficient out-of-core
read/write access to potentially very large arrays. In addition, Darr supports
the possibility to append and truncate arrays, and the use of ragged arrays
(still experimental).

See this `tutorial <https://darr.readthedocs.io/en/latest/tutorial.html>`__
for a brief introduction, or the
`documentation <http://darr.readthedocs.io/>`__ for more info.

Darr is currently pre-1.0, still undergoing significant development. It is
open source and freely available under the `New BSD License
<https://opensource.org/licenses/BSD-3-Clause>`__ terms.

Features
--------

-  Disk-persistent array data is directly accessible through `NumPy
   indexing <https://numpy.org/doc/stable/reference/arrays.indexing.html>`__.
-  Works with **data arrays larger than RAM**.
-  Data is stored purely based on flat binary and text files, maximizing
   **tool independence**.
-  Data is automatically documented and includes a README text file with
   **human-readable explanation** of how the data is stored.
-  README includes **examples of how to read the array** in a number of popular
   data analysis environments, such as Python (without Darr), R, Julia,
   Octave/Matlab, GDL/IDL, and Mathematica (see `example array <https://github.com/gbeckers/Darr/tree/master/examplearrays/examplearray_uint64.darr>`__).
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
Darr is relatively new, and therefore in its beta stage. It is being used in
practice in the lab, and test coverage is allmost 100%, but first official
release will have to wait until the API is more stable. The naming of some
functions/methods may still change.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   tutorial
   rationale
   readcode
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
.. |Appveyor Status| image:: https://ci.appveyor.com/api/projects/status/github/gbeckers/darr?svg=true
   :target: https://ci.appveyor.com/project/gbeckers/darr
.. |PyPi version| image:: https://img.shields.io/badge/pypi-0.4.0-orange.svg
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

Darr is BSD licensed (BSD 3-Clause License). (c) 2017-2022, Gabriël
Beckers