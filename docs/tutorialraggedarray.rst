Tutorial RaggedArray
====================

.. contents:: Table of Contents
    :depth: 3


Look at the :doc:`general tutorial <tutorialarray>` for Arrays first, if you
haven't done so.

.. _access:

What is a ragged array?
-----------------------
A ragged array (also called a jagged array) can be seen as a sequence
of subarrays that may be multidimensional and that may vary in the length of
their first dimension only.

In the simplest case it is a sequence of variable-length one-dimensional
arrays, e.g.:

.. code:: python

  [[1,2],[3,4,5],[6],[7,8,9,10]]



