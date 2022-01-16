======================
Darr API Documentation
======================

.. contents:: :local:
   :depth: 2

Two types of numeric data structures are supported:

* arrays_
* raggedarrays_

.. automodule:: darr.array

.. _arrays:

Arrays
======

Accessing arrays
----------------
.. autoclass:: darr.Array
   :members:
   :inherited-members:

Creating arrays
---------------

.. autofunction:: darr.asarray
.. autofunction:: darr.create_array

Deleting arrays
---------------

.. autofunction:: darr.delete_array

Truncating arrays
-----------------

.. autofunction:: darr.truncate_array

.. _raggedarrays:

Ragged Arrays
=============

.. warning::
   Note that Ragged Arrays are still experimental! They do not support setting
   values yet, only creating, appending, and reading.


Accessing ragged arrays
-----------------------
.. autoclass:: darr.RaggedArray
   :members:
   :inherited-members:

Creating ragged arrays
----------------------

.. autofunction:: darr.asraggedarray
.. autofunction:: darr.create_raggedarray

Deleting ragged arrays
----------------------

.. autofunction:: darr.delete_raggedarray

Truncating ragged arrays
------------------------

.. autofunction:: darr.truncate_raggedarray
