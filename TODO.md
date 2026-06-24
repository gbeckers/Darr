# Darr — remaining issues / TODO

Outstanding items from the code review. The three correctness bugs and the
deprecation-version inconsistencies were already fixed (commit `b4cf187`);
what follows is the remaining backlog.

## Correctness / robustness

- [x] **`_archunkgenerator` zero-length edge case** (`src/darr/array.py`).
  The `hasattr(array, '__len__')` branch called `array.astype(dtype)` when
  `totallen == 0`, which assumed a NumPy array; an empty plain list/sequence
  raised `AttributeError`. Fixed to use `np.asarray(array, dtype=dtype)`.
- [x] **`asarray` generator with mismatched chunk shapes** (`array.py`). A
  generator yielding chunks whose trailing (non-first) dimensions differ used
  to fail with a cryptic "binary file size" error. Now validated per chunk
  with a clear `ValueError`.
- [x] **Zero-length non-first axis** (`array.py`). `create_array(shape=(5,0))`
  and `asarray(np.zeros((5,0)))` raised `ZeroDivisionError` in the chunk-size
  calculation. Now handled: such (data-less) arrays are created and round-trip
  with shape `(5, 0)`.
- [x] **Empty `arrayiterable`** (`raggedarray.py`). `asraggedarray(path, [])`
  raised a bare `StopIteration`. Now raises a clear `ValueError` pointing to
  `create_raggedarray` for empty ragged arrays.

## API completeness (existing TODO/FIXME markers)

- [x] **`RaggedArray` docstrings** — `# TODO needs doc` (`raggedarray.py:17`).
- [x] **`RaggedArray.open_array` method** — `# TODO an open_array method`
  (`raggedarray.py:18`), to mirror `Array.open_array`.
- [x] **`Array.__eq__`** — implemented as whole-array content equality
  (returns a bool: same shape + all elements equal; `False` for non-array-like
  others). Added `__ne__`, set `__hash__ = None` (unhashable, like ndarray),
  with tests.
- [x] **`RaggedArray.append` efficiency** — `# TODO ... use _append on
  self._values` (`raggedarray.py:227`).
- [x] **`DataDir.copy` tests** — added `TestCopy` (contents copied + returns a
  `DataDir`; existing dst raises `OSError`).
- [x] **`DataDir.open_file` overwrite param** — resolved: the `accessmode`
  string already controls overwrite/append/exclusive semantics (it delegates
  to builtin `open`), so no extra parameter is needed; clarified in docstring.
- [x] **`MetaData.pop` / `popitem` overlap** — factored out `_check_writeable`
  and `_save` helpers, shared by `pop`, `popitem`, and `update`.
- [x] **Dedup temp-dir helpers** — `tempdirfile` now delegates to `tempdir`;
  also moved `mkdtemp` out of the `try` so a failed creation can't raise in the
  `finally`.
- [x] **Allow NumPy ints where Python ints are required** — `truncate_array`
  and `truncate_raggedarray` now accept `(int, np.integer)`, with tests.

## Cleanup

- [x] **Stale distutils TODO** (`array.py:12`). The `# TODO replace distutils`
  comment is obsolete — distutils is no longer imported anywhere. Remove it.
- [x] **Mixed Unicode/ASCII hyphens** (`src/darr/numtype.py`). Several
  `numtypesdescr` strings used U+2010 (`‐`) instead of ASCII `-`,
  inconsistently with neighbouring lines. Replaced all with ASCII `-` and
  normalised the spaced `32 - bit` / `64 - bit` in the complex-number
  descriptions to `32-bit` / `64-bit`.
- [x] **flake8 noise** (substantive findings). Fixed the meaningful ones:
  3 bare `except:` (E722), the ambiguous variable name `l` (E741), and 16
  f-strings with no placeholders (F541). The remaining findings are purely
  cosmetic (continuation-line indentation, blank lines, trailing whitespace)
  and the star-import warnings in `__init__.py` (F403/F405) are intentional,
  so CI still keeps `--exit-zero` on the second flake8 pass for now.

## Project / packaging

- [x] **Two divergent CI configs**. Removed the abandoned `azure-pipelines.yml`
  (Python 3.9/3.11); `.github/workflows/python_package.yml` (3.10/3.13) is now
  the single CI source of truth.
- [x] **Stale dev pins**. Refreshed `requirements_dev.txt` to current releases
  (pytest 9.1.1, pytest-cov 7.1.0, coverage 7.14.3, coveralls 4.1.0).
- [x] **Dependency duplication**. Removed `requirements.txt` (it only
  duplicated `numpy`); `pyproject.toml` is now the single source of truth for
  runtime deps and CI installs the package itself with `pip install .`.
  (`docs/requirements.txt` is docs-only and left as is.)
