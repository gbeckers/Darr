Maximizing readability of your data
===================================

The purpose of Darr is to make numeric array data as widely and as easily
readable as possible through automatic self-documentation, which includes code
for reading in other languages. Darr is NumPy-based and therefore supports
many numeric types: int8, uint8, int16, uint16, int32, uint32, int64, uint64,
float16, float32, float64, complex64 and complex128. Not all of those types
are supported in other languages though, so your choice of the numeric type
of your data influences how widely readable it is.

The page :doc:`Reading data in other environments <readcode>` provides a
table on compatibility of numeric types and languages. From this, a number of
conclusions can be drawn:

- The following types are unproblematic in all languages: int16, int32,
  float32, float64, except that R represents the minimum value of an
  int32 (-2147483648) as NA. If possible, use one of these types.

- Complex128 is relatively well supported, except for Maple. In Matlab and
  plain Python reading code is provided but it is workaround code that is
  less efficient .

- All unsigned integers are not supported in Maple. R only supports unsigned
  integers that are 8 or 16 bits.

- float16 is not widely supported, but it is supported by two modern,
  open source computing packages: Julia and Python with Numpy. It is best
  avoided. Use float32, unless there are disk space concerns. Matlab can read
  it indirectly, using a temporary array and type casting, which can be
  problematic when arrays are very large and RAM is limited. Octave does not
  support it (yet).

- If compatibility with R is important to you, have a good look at the table
  in :doc:`Reading data in other environments <readcode>`. Despite all its
  merits, R is quite limited in the numeric types that it can read and handle.
  It is surprising that it doesn't even support int64. In Python, int64
  is the default for integers so if you create an array without specifying
  that it should be int32, it will be int64 and not readable in R.

To help deciding on numeric type, the minimum and maximum values that are
possible for integer types are listed below.

Minimum and maximum values for integers
---------------------------------------

- int8: 8-bit signed integer, -128 to 127
- int16: 16‐bit signed integer, -32768 to 32767
- int32: 32‐bit signed integer, -2147483648 to 2147483647
- int64: 64‐bit signed integer, -9223372036854775808 to 9223372036854775807
- uint8: 8‐bit unsigned integer, 0 to 255
- uint16: 16‐bit unsigned integer, 0 to 65535
- uint32: 32‐bit unsigned integer, 0 to 4294967295
- uint64: 64‐bit unsigned integer, 0 to 18446744073709551615

Note that R does not represent the minimum of an int32, -2147483648. R has
-2147483647 as the mimimum value of an int32. It will represent -2147483648
it as NA.

Compatibility of ragged arrays in R
-----------------------------------
Default settings when creating RaggedArrays are chosen to maximize wide
readability. For example, index arrays that are used under the hood to find
subarrays have a signed integer type because that is most compatible with other
languages, even though in Darr/NumPy an unsigned integer would be more space
efficient. Darr chooses int64 as the default even though, bizarrely, R does not
support int64. R does support int32, but that would limit the size of Darr
ragged arrays to the extent that is impractical for some use cases. On the
other hand we'd like compatibility with R as much as possible because of its
large user base and it being open and free. For this reason R reading code
is generated for ragged arrays with int64 index arrays. Despite that R does not
officially support the type, it will read them correctly if the values are not
outsize of the int32 range. Darr will thus generate R code for ragged arrays
that are compatible, which are the ones that have values based on a
R-compatible type (int8, int16, int32, float32, float64, complex128), and that
is not larger than 2147483647 in size.
