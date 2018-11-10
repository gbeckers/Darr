.. Darr documentation master file, created by
   sphinx-quickstart on Sat Feb 17 16:29:23 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Darr
====

|Travis Status| |Appveyor Status| |PyPy version| |Coverage Status| |Docs Status|


Darr is a Python science library for storing and sharing numeric data arrays
in a way that is open, simple, and self-explanatory. It also enables fast
memory-mapped read/write access to such disk-based data, the ability to append
data, and the flexible use of metadata. It is primarily designed for
scientific use cases. Save and use your numeric arrays and metadata with one
line of code while long-term and tool-independent accessibility and easy
shareability is ensured.

To avoid dependency on specific tools, Darr is based on a combination of
flat binary and human-readable text files. It automatically saves a clear
text description of how the data is stored, together with code for reading
the specific data in a variety of current scientific data tools such as
Python, R, Julia, IDL, Matlab, Maple and Mathematica (see `example array
<https://github.com/gbeckers/Darr/tree/master/examplearray.darr>`__).

Darr is currently pre-1.0, still undergoing significant development. It
is open source and freely available under the `New BSD
License <https://opensource.org/licenses/BSD-3-Clause>`__ terms.

Code can be found on GitHub: https://github.com/gbeckers/Darr

Features
--------

Pro's:

-  **Transparent data format** based on **flat binary** and **text**
   files.
-  Supports **very large data arrays** through **memory-mapped** file
   access.
-  Data read/write access through **NumPy indexing** (see
   `here <https://docs.scipy.org/doc/numpy-1.13.0/reference/arrays.indexing.html>`__).
-  Data is easily **appendable**.
-  **Human-readable explanation of how the binary data is stored** is
   saved in a README text file.
-  README also contains **examples of how to read the array** in popular
   analysis environments such as Python (without Darr), R, Julia,
   Octave/Matlab, GDL/IDL, Maple and Mathematica.
-  **Many numeric types** are supported: (u)int8-(u)int64,
   float16-float64, complex64, complex128.
-  Easy use of **metadata**, stored in a separate
   `JSON <https://en.wikipedia.org/wiki/JSON>`__ text file.
-  **Minimal dependencies**, only `NumPy <http://www.numpy.org/>`__.
-  **Integrates easily** with the
   `Dask <https://dask.pydata.org/en/latest/>`__ or
   `NumExpr <https://numexpr.readthedocs.io/en/latest/>`__ libraries for
   **numeric computation on very large Darr arrays**.

Con's:

-  **No direct access to compressed data**, although it is of course possible
   to simply compress darr files for archiving purposes.
-  **Inefficient (storage-wise) for very small arrays**. If you have a
   zillion small arrays, and storage space is a concern, use other
   approaches.


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
.. |PyPy version| image:: https://img.shields.io/badge/pypi-v0.1.7-orange.svg
   :target: https://pypi.org/project/darr/
.. |Coverage Status| image:: https://coveralls.io/repos/github/gbeckers/Darr/badge.svg?branch=master
   :target: https://coveralls.io/github/gbeckers/Darr?branch=master
.. |Docs Status| image:: https://readthedocs.org/projects/darr/badge/?version=latest
   :target: https://darr.readthedocs.io/en/latest/

Darr is BSD licensed (BSD 3-Clause License). (c) 2017-2018, Gabriël
Beckers