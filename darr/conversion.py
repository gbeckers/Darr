"""

"""

from .array import Array

__all__ = ['aszarrarray']

def aszarrarray(da, chunks=True, dtype=None, compressor='default',
                order='C', store=None, synchronizer=None, overwrite=False,
                path=None, chunk_store=None, filters=None, cache_metadata=True,
                cache_attrs=True, read_only=False, object_codec=None, **kwargs):
    """Convert a Darr array to a Zarr array.

    Parameters
    ----------
    da : Darr Array or Path to it
    chunks : int or tuple of ints, optional
        Chunk shape. If True, will be guessed from `shape` and `dtype`. If
        False, will be set to `shape`, i.e., single chunk for the whole array.
    dtype : string or dtype, optional
        NumPy dtype.
    compressor : Codec, optional
        Primary compressor.
    fill_value : object
        Default value to use for uninitialized portions of the array.
    order : {'C', 'F'}, optional
        Memory layout to be used within each chunk.
    store : MutableMapping or string
        Store or path to directory in file system or name of zip file.
    synchronizer : object, optional
        Array synchronizer.
    overwrite : bool, optional
        If True, delete all pre-existing data in `store` at `path` before
        creating the array.
    path : string, optional
        Path under which array is stored.
    chunk_store : MutableMapping, optional
        Separate storage for chunks. If not provided, `store` will be used
        for storage of both chunks and metadata.
    filters : sequence of Codecs, optional
        Sequence of filters to use to encode chunk data prior to compression.
    cache_metadata : bool, optional
        If True, array configuration metadata will be cached for the
        lifetime of the object. If False, array metadata will be reloaded
        prior to all data access and modification operations (may incur
        overhead depending on storage and data access pattern).
    cache_attrs : bool, optional
        If True (default), user attributes will be cached for attribute read
        operations. If False, user attributes are reloaded from the store prior
        to all attribute read operations.
    read_only : bool, optional
        True if array should be protected against modification.
    object_codec : Codec, optional
        A codec to encode object arrays, only needed if dtype=object.

    Returns
    -------
    zarr.core.Array

    Examples
    --------
    >>> import darr
    >>> da = darr.create_array('test.darr', shape=(2,1024), metadata={'a':1})
    >>> from darr.conversion import aszarrarray
    >>> za = aszarrarray(da, 'test.zarr')
    >>> za
    <zarr.core.Array (2, 1024) float64>
    >>> dict(za.attrs) # metadata is preserved as attrs
    {'a': 1}

    Notes
    -----
    See https://zarr.readthedocs.io/en/stable/tutorial.html for more info on
    Zarr

    The doc string here is largely copied from that of zarr.core.Array

    """

    try:
        import zarr
    except ModuleNotFoundError:
        print('Could not find the Zarr library. Is it installed?')
        raise
    try:
        if not isinstance(da, Array): # probably a path
            da = Array(da)
    except Exception:
        raise TypeError(f"'{da}' not recognized as a Darr array")
    # zarr apparently nicely takes chunks of data so that RAM does not get
    # flooded when arrays are very large.
    za = zarr.creation.array(data=da, chunks=chunks, dtype=dtype,
                             compressor=compressor, order=order, store=store,
                             synchronizer=synchronizer, overwrite=overwrite,
                             path=path, chunk_store=chunk_store,
                             filters=filters, cache_metadata=cache_metadata,
                             cache_attrs=cache_attrs, read_only=read_only,
                             object_codec=object_codec, **kwargs)
    for k, v in da.metadata.items():
        za.attrs[k] = v
    return za


