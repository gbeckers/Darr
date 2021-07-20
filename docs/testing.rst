Testing
=======

To run the test suite:

.. code:: python

    >>> import darr as da
    >>> da.test()
    .............................................................................................................................................................................................................
    ----------------------------------------------------------------------
    Ran 205 tests in 15.099s

    OK
    <unittest.runner.TextTestResult run=205 errors=0 failures=0>
    >>>

Note that tests require the creation and deletion of temporary files. In some
operation systems you cannot delete a file if another process accesses it,
which may be the case when files are synchronized by something like Dropbox or
read by a virus scanner. If, so you may get errors when testing that are not
related to Darr, but to other programs that are accessing Darr files.