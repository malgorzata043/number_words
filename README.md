# Number Words

Render integers as English words, including the awkward teens.

```python
from number_words import int_to_words

print(int_to_words(0))     # zero
print(int_to_words(13))    # thirteen
print(int_to_words(21))    # twenty-one
print(int_to_words(321))   # three hundred twenty-one
print(int_to_words(-1001)) # negative one thousand one
```

## Why this exists

Converting an integer to its English spelling looks trivial until you meet the
teens. "Eleven" and "twelve" are irregular, "thirteen" through "nineteen"
refuse to decompose into tens-plus-ones, and the whole band sits awkwardly
between the ones column and the multiples of ten. This library exists to handle
that one irregularity correctly instead of papering over it.

The scope is deliberately narrow: signed integers only, short-scale naming
(million, billion, trillion, quadrillion), lowercase output, hyphens for
compounds ("twenty-one"), and spaces between scale groups. There is no
title-case, no comma insertion, and no long-scale support. Picking one
spelling convention and holding to it is the point.

## The awkward edge you will hit

`int_to_words` rejects integers outside `[-2**53, 2**53 - 1]`. The upper bound
is set by the largest scale word this library defines ("quadrillion", 10**15);
2**53 is the smallest power of two whose magnitude would require a scale beyond
that. If you pass a value outside the range, you get `ValueError`. `bool` is also
rejected, even though it is technically an `int` subclass, because spelling
`True` as "one" is the kind of surprise that belongs in a bug report.

The other edge is the teens themselves: numbers 11 through 19 are spelled with
their own words (`eleven`, `twelve`, `thirteen`, ... `nineteen`) and are never
decomposed. This is the whole reason the library exists.

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

