Darr
====

|Travis Status| |Appveyor Status| |PyPi version| |Conda Forge| |Coverage Status|
|Docs Status| |Repo Status| |PyUp Badge|

Darr is a Python science library to work with potentially large NumPy arrays
and metadata that persist on disk, in a format that is simple,
self-documented and tool-independent. The goal is to keep your data easily
accessible on the short and long term, from a wide range of computing
environments. Keeping data universally readable and documented is in line with
good scientific practice. It not only makes it easy to share data with
others, but also to look at you own data with different tools. More rationale
for this approach is provided
`here <https://darr.readthedocs.io/en/latest/rationale .html>`__.

Flat binary files and (JSON) text files are accompanied by a README text file
that explains how the specific data and metadata are stored and how they can
be read. This includes code for reading the array in a variety of current
scientific data tools such as Python, R, Julia, IDL, Matlab, Maple, and
Mathematica. It is trivially easy to share your data with others or with
yourself when working in different computing environments, because it always
contains a clear and specific description of how to read it. No need to export
anything or to provide elaborate explanation. No dependence on complicated
formats or specialized tools.

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

Pro's:

-  Data persists on-disk, purely based on flat binary and text files,
   **tool independence**.
-  README text file with **human-readable explanation** of how the binary data
   is stored.
-  README includes **examples of how to read the array** in a number of popular
   data analysis environments, such as Python (without Darr), R, Julia,
   Octave/Matlab, GDL/IDL, and Mathematica (see `example array <https://github.com/gbeckers/Darr/tree/master/examplearrays/examplearray_uint64.darr>`__).
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



Darr is BSD licensed (BSD 3-Clause License). (c) 2017-2021, Gabriël
Beckers

.. |Travis Status| image:: https://travis-ci.com/gbeckers/Darr.svg?branch=master
   :target: https://travis-ci.com/gbeckers/Darr?branch=master
.. |Appveyor Status| image:: https://ci.appveyor.com/api/projects/status/github/gbeckers/darr?svg=true
   :target: https://ci.appveyor.com/project/gbeckers/darr
.. |PyPi version| image:: https://img.shields.io/badge/pypi-0.4.0-orange.svg
   :target: https://pypi.org/project/darr/
.. |Conda Forge| image:: https://anaconda.org/conda-forge/darr/badges/version.svg
   :target: https://anaconda.org/conda-forge/darr
.. |Coverage Status| image:: https://coveralls.io/repos/github/gbeckers/Darr/badge.svg?branch=master
   :target: https://coveralls.io/github/gbeckers/Darr?branch=master&kill_cache=1
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
