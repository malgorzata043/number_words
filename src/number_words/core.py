"""Render integers as English words.

Supports the range -2**53 .. 2**53-1, which is the range of integers exactly
representable in IEEE-754 double precision. This ceiling also keeps the output
string comfortably within practical length limits ("nine quadrillion ...").

Design decisions, stated plainly:
- Negative numbers are rendered with a leading "negative". The brief says
  "integers"; we support signed integers and use "negative" rather than
  "minus" because this is a spelling-out library, not an arithmetic one.
- Zero is "zero".
- Scales follow the short-scale naming used in modern US/UK English
  (million, billion, trillion, ...). No long-scale support is provided.
- The output is lowercase and uses hyphens for compounds ("twenty-one") and
  spaces between groups. No title case, no Oxford-comma handling.
- The largest supported scale word is "quadrillion" (10**15), chosen because it
  is the highest named scale needed to express the full signed 2**53 range.

The awkward teens (eleven, twelve, ..., nineteen) each have their own word and
must not be decomposed ("ten-one" is wrong). We special-case the whole teen
band rather than trying to reuse the tens logic, because the irregularity is
not algorithmic.
"""

_UPPER_BOUND = 2 ** 53  # exclusive: largest value handled is this minus one.
_LOWER_BOUND = -_UPPER_BOUND  # inclusive: largest negative magnitude.

_ONES = [
    "",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]

_TEENS = [
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
]

# Tens words for values 20, 30, ..., 90. Index by tens digit.
_TENS = [
    "",
    "",
    "twenty",
    "thirty",
    "forty",
    "fifty",
    "sixty",
    "seventy",
    "eighty",
    "ninety",
]

# (magnitude, scale word). Ordered from largest to smallest so we greedily
# peel off the biggest chunk first.
_SCALES = [
    (10 ** 15, "quadrillion"),
    (10 ** 12, "trillion"),
    (10 ** 9, "billion"),
    (10 ** 6, "million"),
    (10 ** 3, "thousand"),
]


def _below_thousand(n: int) -> str:
    """Spell out 0 <= n < 1000.

    This is the building block for the scaled recursion. It is kept separate
    because the teens irregularity lives here, and isolating it makes the
    behaviour easy to audit.
    """
    if n == 0:
        return ""
    parts: list[str] = []
    hundreds, rem = divmod(n, 100)
    if hundreds:
        parts.append(f"{_ONES[hundreds]} hundred")
    if rem:
        if rem < 10:
            parts.append(_ONES[rem])
        elif rem < 20:
            parts.append(_TEENS[rem - 10])
        else:
            tens, ones = divmod(rem, 10)
            if ones:
                parts.append(f"{_TENS[tens]}-{_ONES[ones]}")
            else:
                parts.append(_TENS[tens])
    return " ".join(parts)


def int_to_words(n: int) -> str:
    """Convert an integer to its English-words spelling.

    Args:
        n: An int in the range [-2**53, 2**53). Values outside this range raise
            ValueError; this bound exists because the largest scale word we
            define is "quadrillion" (10**15), and 2**53 is the smallest power
            of two whose magnitude would require a scale word beyond that.

    Returns:
        The lowercase English spelling of ``n``.

    Raises:
        ValueError: If ``n`` is outside the supported range or not an int.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise ValueError(f"int_to_words requires an int, got {type(n).__name__}")
    if n < _LOWER_BOUND or n >= _UPPER_BOUND:
        raise ValueError(
            f"int_to_words supports integers in [{_LOWER_BOUND}, {_UPPER_BOUND - 1}]"
        )

    if n == 0:
        return "zero"

    negative = n < 0
    magnitude = -n if negative else n

    chunks: list[str] = []
    remaining = magnitude
    for divisor, word in _SCALES:
        quotient, remaining = divmod(remaining, divisor)
        if quotient:
            chunks.append(f"{_below_thousand(quotient)} {word}")
    if remaining:
        chunks.append(_below_thousand(remaining))

    text = " ".join(c for c in chunks if c)
    return f"negative {text}" if negative else text
