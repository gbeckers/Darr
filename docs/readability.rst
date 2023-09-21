Maximizing readability of your data
===================================

The purpose of Darr is to make numeric array data as widely and as easily
readable as possible through automatic self-documentation, which includes code
for reading the data in many scientific computing languages. Darr is
NumPy-based and therefore supports many numeric types: int8, uint8, int16,
uint16, int32, uint32, int64, uint64, float16, float32, float64, complex64
and complex128. Not all of those types are supported in other languages
though, so your choice of the numeric type of your data influences how widely
readable it is.

The page :doc:`Reading data in other environments <readcode>` provides a
table on compatibility of numeric types and languages. From this, a number of
conclusions can be drawn:

- The following types are unproblematic in all languages: int16, int32,
  float32, float64. If possible, use one of these types.

- Complex128 is relatively well supported, except for Maple. In Matlab and
  plain Python reading code is provided but it is workaround code that is
  less efficient .

- All unsigned integers are not supported in Maple. R only supports unsigned
  integers that are 8 or 16 bits.

- Float16 is not widely supported, but it is supported by two modern,
  open source computing packages: Julia and Python with Numpy. It is best
  avoided from a compatibility perspective. Use float32, unless there are disk
  space concerns. Matlab can read float16 indirectly, using a temporary array
  and type casting, which can be problematic when arrays are very large and
  RAM is limited. Octave does not support it (yet).

- If compatibility with R is important to you, have a good look at the table
  in :doc:`Reading data in other environments <readcode>`. Despite all its
  merits, R is quite limited in the numeric types that it can read and handle.
  For example it doesn't support int64 (!). Darr/NumPy int64 arrays are not
  readable in R (but see below how this sometimes can be circumvented for
  RaggedArrays).

To help deciding on numeric type, the minimum and maximum values that are
possible for integer types are listed below.

Minimum and maximum values for integers
---------------------------------------

- int8: 8-bit signed integer, -128 to 127
- int16: 16‐bit signed integer, -32,768 to 32,767
- int32: 32‐bit signed integer, -2,147,483,648 to 2,147,483,647
- int64: 64‐bit signed integer, -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807
- uint8: 8‐bit unsigned integer, 0 to 255
- uint16: 16‐bit unsigned integer, 0 to 65,535
- uint32: 32‐bit unsigned integer, 0 to 4,294,967,295
- uint64: 64‐bit unsigned integer, 0 to 18,446,744,073,709,551,615

.. Note::
    For some reason R does not represent the minimum of an int32, -2147483648. R
    has -2147483647 as the mimimum value of an int32. It will represent
    the number -2147483648 as *NA*.

Compatibility of ragged arrays in R
-----------------------------------
When creating RaggedArrays, default settings are chosen so as to maximize wide
readability. For example, index arrays that are used under the hood to find
subarrays have a signed integer type (int64) because that is most compatible
with other languages, even though in Darr/NumPy itself an unsigned integer
(uint64) would be more space efficient. There is a prominent exception
though: int64 is not supported by R. R does support int32, but choosing that
for indices in Darr RaggedArrays would limit their size to the extent that
it would be impractical for some use cases. On the other hand, we'd like
compatibility with R as much as possible because of its large user base and
it being open and free. Fortunately, despite that R does not officially
support the type, it will read int64 correctly if values do not exceed the
int32 range. Darr will thus generate R code for ragged arrays when they are
compatible, which is the case if they have have values based on a
R-compatible type (int8, int16, int32, float32, float64, complex128), and
are not larger than 2147483647 in size.
