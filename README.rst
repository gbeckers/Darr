Darr
====

|Travis Status| |Appveyor Status| |PyPi version| |Coverage Status|
|Docs Status| |Repo Status| |Codacy Badge| |PyUp Badge|

Darr is a Python science library for efficient read/write/append access to
disk-persistent numeric data arrays. There are other Python libraries for this,
but Darr also ensures tool-independent and long-term accessibility of your
data. It saves and automatically updates a human-readable explanation of how
your binary data is stored, together with code for reading the specific data
in a variety of current scientific data tools such as Python, R, Julia, IDL,
Matlab, Maple, and Mathematica (see `example array <https://github.com/
gbeckers/Darr/tree/master/examplearrays /examplearray_float64.darr>`__).

In essence, Darr enables you to work with potentially very large data arrays
in a Python/NumPy environment, and share this data as is with others who do
not use Darr, or even Python, without exporting anything. It is also an easy
way to make sure you can read your own data in the future when you may use
different tools.

Darr currently supports numerical N-dimensional arrays, and experimentally
supports numerical ragged arrays, i.e. a series of arrays in which one
dimension varies in length.

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


Documentation
-------------
See the `documentation <http://darr.readthedocs.io/>`_ for more information.


Other interesting projects
--------------------------
If Darr is not exactly what you are looking for, have a look at these projects:

-  `exdir <https://github.com/CINPLA/exdir/>`__
-  `h5py <https://github.com/h5py/h5py>`__
-  `pyfbf <https://github.com/davidh-ssec/pyfbf>`__
-  `pytables <https://github.com/PyTables/PyTables>`__
-  `zarr <https://github.com/zarr-developers/zarr>`__



Darr is BSD licensed (BSD 3-Clause License). (c) 2017-2018, Gabriël
Beckers

.. |Travis Status| image:: https://travis-ci.org/gbeckers/Darr.svg?branch=master
   :target: https://travis-ci.org/gbeckers/Darr?branch=master
.. |Appveyor Status| image:: https://ci.appveyor.com/api/projects/status/github/gbeckers/darr?svg=true
   :target: https://ci.appveyor.com/project/gbeckers/darr
.. |PyPi version| image:: https://img.shields.io/badge/pypi-0.1.11-orange.svg
   :target: https://pypi.org/project/darr/
.. |Coverage Status| image:: https://coveralls.io/repos/github/gbeckers/Darr/badge.svg?branch=master
   :target: https://coveralls.io/github/gbeckers/Darr?branch=master
.. |Docs Status| image:: https://readthedocs.org/projects/darr/badge/?version=latest
   :target: https://darr.readthedocs.io/en/latest/
.. |Repo Status| image:: https://www.repostatus.org/badges/latest/active.svg
   :alt: Project Status: Active – The project has reached a stable, usable state and is being actively developed.
   :target: https://www.repostatus.org/#active
.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/c0157592ce7a4ecca5f7d8527874ce54
   :alt: Codacy Badge
   :target: https://app.codacy.com/app/gbeckers/Darr?utm_source=github.com&utm_medium=referral&utm_content=gbeckers/Darr&utm_campaign=Badge_Grade_Dashboard
.. |PyUp Badge| image:: https://pyup.io/repos/github/gbeckers/Darr/shield.svg
   :target: https://pyup.io/repos/github/gbeckers/Darr/
   :alt: Updates
