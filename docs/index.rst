.. Darr documentation master file, created by
   sphinx-quickstart on Sat Feb 17 16:29:23 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Darr
====


|Travis Status| |Appveyor Status| |PyPi version| |Coverage Status|
|Docs Status| |Repo Status| |Codacy Badge| |PyUp Badge|


Darr is a Python science library for storing and sharing numeric data arrays
in a way that is open, simple, and self-explanatory. Save and use
your numeric arrays and metadata with one line of code while long-term and
tool-independent accessibility and easy shareability is ensured. In
addition, Darr provides fast memory-mapped read/write access to such
disk-based data and the ability to append data, , so that arrays may be
larger than available RAM..

To maximize wide readability of your data, Darr is based on a combination of
flat binary and human-readable text files. It automatically saves a
description of how the data is stored, together with code for reading the
specific data in a variety of current scientific data tools such as
Python, R, Julia, IDL, Matlab, Maple, and Mathematica (see `example array
<https://github.com/gbeckers/Darr/tree/master/examplearray.darr>`__).

Darr is currently pre-1.0, still undergoing significant development. It is
open source and freely available under the `New BSD License
<https://opensource.org/licenses/BSD-3-Clause>`__ terms.

Features
--------

Pro's:

-  Purely based on **flat binary** and **text** files, tool independence.
-  **Human-readable explanation of how the binary data is stored** is
   saved in a README text file.
-  Includes **examples of how to read the array** in popular
   analysis environments such as Python (without Darr), R, Julia,
   Octave/Matlab, GDL/IDL, and Mathematica.
-  Supports **very large data arrays** through **memory-mapped** file
   access.
-  Data read/write access is simple through **NumPy indexing** (see
   `here <https://docs.scipy.org/doc/numpy-1.13.0/reference/arrays.indexing.html>`__).
-  Data is easily **appendable**.
-  **Many numeric types** are supported: (u)int8-(u)int64, float16-float64,
   complex64, complex128.
-  Easy use of **metadata**, stored in a separate
   `JSON <https://en.wikipedia.org/wiki/JSON>`__ text file.
-  **Minimal dependencies**, only `NumPy <http://www.numpy.org/>`__.
-  **Integrates easily** with the
   `Dask <https://dask.pydata.org/en/latest/>`__ or
   `NumExpr <https://numexpr.readthedocs.io/en/latest/>`__ libraries for
   **numeric computation on very large Darr arrays**.

Con's:

-  **No compression**, although it is of course possible to compress darr files
   for archiving purposes.
-  **Inefficient (storage-wise) for very small arrays**. If you have a
   zillion small arrays, and storage space is a concern, use other approaches.


Installation
------------

Darr depends on Python 3.6 or higher and NumPy 1.12 or higher.

Install Darr from PyPI::

    $ pip install darr



Status
------
Darr is relatively new, and therefore in its alpha stage. It is being used in
practice in the lab, and test coverage is over 90%, but first beta release will
have to wait until test coverage is near 100% and the API is more stable. The
naming of some functions/methods may still change.


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


.. |Travis Status| image:: https://travis-ci.org/gbeckers/Darr.svg?branch=master
   :target: https://travis-ci.org/gbeckers/Darr?branch=master
.. |Appveyor Status| image:: https://ci.appveyor.com/api/projects/status/github/gbeckers/darr?svg=true
   :target: https://ci.appveyor.com/project/gbeckers/darr
.. |PyPy version| image:: https://img.shields.io/badge/pypi-v0.1.9-orange.svg
   :target: https://pypi.org/project/darr/
.. |Coverage Status| image:: https://coveralls.io/repos/github/gbeckers/Darr/badge.svg?branch=master
   :target: https://coveralls.io/github/gbeckers/Darr?branch=master
.. |Docs Status| image:: https://readthedocs.org/projects/darr/badge/?version=latest
   :target: https://darr.readthedocs.io/en/latest/

Darr is BSD licensed (BSD 3-Clause License). (c) 2017-2018, Gabriël
Beckers