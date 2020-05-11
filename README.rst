Darr
====

|Travis Status| |Appveyor Status| |PyPi version| |Conda Forge| |Coverage Status|
|Docs Status| |Repo Status| |PyUp Badge|


Darr is a Python science library that enables you to store and access
disk-based numeric arrays, without depending on tool-specific data formats.
This makes it easy to access the same data in many different languages and on
different analysis platforms. No exporting required and, as the data is saved
in a self-explanatory way, not much explanation required either when sharing
or archiving your data. Tool-independent and easy access to data is in line
with good scientific practice as it promotes wide and long-term availability,
to others but also to yourself. More rationale for this approach is provided
`here <https://darr.readthedocs.io/en/latest/rationale.html>`__.

Darr supports efficient read/write/append access and is based on universally
readable flat binary files and automatically generated text files, containing
human-readable explanation of precisely how your binary data is stored. It
also provides specific code that reads the data in a variety of current
scientific data tools such as Python, R, Julia, IDL, Matlab, Maple, and
Mathematica (see
`example array <https://github.com/gbeckers/Darr/tree/master/examplearrays/examplearray_uint64.darr>`__).

Darr currently supports numerical N-dimensional arrays, and experimentally
supports numerical ragged arrays, i.e. a series of arrays in which one
dimension varies in length.

See this `tutorial <https://darr.readthedocs.io/en/latest/tutorial.html>`__
for a brief introduction, or the
`documentation <http://darr.readthedocs.io/>`__ for more info.

Darr is currently pre-1.0, still undergoing significant development. However
we have been using it in practice in our lab for more than a year on both
Linux and Windows machines. It is open source and freely available under the
`New BSD License <https://opensource.org/licenses/BSD-3-Clause>`__ terms.

Features
--------

Pro's:

-  Data storage purely based on **flat binary** and **text** files, tool
   independence.
-  **Human-readable explanation of how the binary data is stored** is
   saved in a README text file.
-  README includes **examples of how to read the particular array** in popular
   analysis environments such as Python (without Darr), R, Julia,
   Octave/Matlab, GDL/IDL, and Mathematica.
-  Supports **very large data arrays**, larger than RAM, through memory-mapping.
-  Data read/write access is simple and powerful through **NumPy indexing**
   (see
   `here <https://docs.scipy.org/doc/numpy-1.13.0/reference/arrays.indexing.html>`__).
-  Data is easily **appendable**.
-  **Many numeric types** are supported: (u)int8-(u)int64, float16-float64,
   complex64, complex128.
-  Easy use of **metadata**, stored in a separate
   `JSON <https://en.wikipedia.org/wiki/JSON>`__ text file.
-  **Minimal dependencies**, only `NumPy <http://www.numpy.org/>`__.
-  **Integrates easily** with the
   `Dask <https://dask.pydata.org/en/latest/>`__ library for
   **numeric computation on very large arrays**.
-  Supports **ragged arrays** (still experimental).

Con's:

-  **No compression**, although compression for archiving purposes is
   supported.
-  **Inefficient (storage-wise) for very small arrays**. If you have a
   zillion small arrays, and storage space is a concern, use other
   approaches, unless you can concatenate them in a ragged array, which Darr
   does support (experimentally).

Installation
------------

Darr depends on Python 3.6 or higher and NumPy 1.12 or higher.

Install Darr from PyPI::

    $ pip install darr

Or,iInstall Darr via conda::

    $ conda install -c conda-forge darr

To install the latest development version, use pip with the latest GitHub
master::

    $ pip install git+https://github.com/gbeckers/darr@master


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



Darr is BSD licensed (BSD 3-Clause License). (c) 2017-2020, Gabriël
Beckers

.. |Travis Status| image:: https://travis-ci.org/gbeckers/Darr.svg?branch=master
   :target: https://travis-ci.org/gbeckers/Darr?branch=master
.. |Appveyor Status| image:: https://ci.appveyor.com/api/projects/status/github/gbeckers/darr?svg=true
   :target: https://ci.appveyor.com/project/gbeckers/darr
.. |PyPi version| image:: https://img.shields.io/badge/pypi-0.2.2-orange.svg
   :target: https://pypi.org/project/darr/
.. |Conda Forge| image:: https://camo.githubusercontent.com/2593f6b7a8118cd866588efe0018cbc87f89cee9/68747470733a2f2f696d672e736869656c64732e696f2f636f6e64612f766e2f636f6e64612d666f7267652f646172722e737667
   :target: https://anaconda.org/conda-forge/darr
.. |Coverage Status| image:: https://coveralls.io/repos/github/gbeckers/Darr/badge.svg?branch=master
   :target: https://coveralls.io/github/gbeckers/Darr?branch=master&kill_cache=1
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
