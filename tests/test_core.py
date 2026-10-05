import unittest

from number_words import int_to_words


class TestIntToWords(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(int_to_words(0), "zero")

    def test_ones(self):
        self.assertEqual(int_to_words(1), "one")
        self.assertEqual(int_to_words(9), "nine")

    def test_ten_and_teens(self):
        self.assertEqual(int_to_words(10), "ten")
        self.assertEqual(int_to_words(11), "eleven")
        self.assertEqual(int_to_words(12), "twelve")
        self.assertEqual(int_to_words(13), "thirteen")
        self.assertEqual(int_to_words(15), "fifteen")
        self.assertEqual(int_to_words(18), "eighteen")
        self.assertEqual(int_to_words(19), "nineteen")

    def test_tens_with_hyphen(self):
        self.assertEqual(int_to_words(20), "twenty")
        self.assertEqual(int_to_words(21), "twenty-one")
        self.assertEqual(int_to_words(99), "ninety-nine")

    def test_hundreds(self):
        self.assertEqual(int_to_words(100), "one hundred")
        self.assertEqual(int_to_words(101), "one hundred one")
        self.assertEqual(int_to_words(115), "one hundred fifteen")
        self.assertEqual(int_to_words(321), "three hundred twenty-one")
        self.assertEqual(int_to_words(999), "nine hundred ninety-nine")

    def test_thousand(self):
        self.assertEqual(int_to_words(1000), "one thousand")
        self.assertEqual(int_to_words(1001), "one thousand one")
        self.assertEqual(int_to_words(1111), "one thousand one hundred eleven")
        self.assertEqual(int_to_words(999999), (
            "nine hundred ninety-nine thousand nine hundred ninety-nine"
        ))

    def test_million_and_above(self):
        self.assertEqual(int_to_words(1_000_000), "one million")
        self.assertEqual(int_to_words(1_000_001), "one million one")
        self.assertEqual(int_to_words(1_000_000_000), "one billion")
        self.assertEqual(int_to_words(1_000_000_000_000), "one trillion")
        self.assertEqual(int_to_words(1_000_000_000_000_000), "one quadrillion")

    def test_mixed_scale(self):
        self.assertEqual(int_to_words(1_000_045), "one million forty-five")
        self.assertEqual(int_to_words(1_234_567), (
            "one million two hundred thirty-four thousand five hundred sixty-seven"
        ))
        self.assertEqual(int_to_words(1_000_000_015), "one billion fifteen")

    def test_negative(self):
        self.assertEqual(int_to_words(-1), "negative one")
        self.assertEqual(int_to_words(-21), "negative twenty-one")
        self.assertEqual(int_to_words(-100), "negative one hundred")

    def test_upper_bound(self):
        # 2**53 - 1 must work; it is the largest value in range.
        self.assertEqual(int_to_words(2 ** 53 - 1), (
            "nine quadrillion seven trillion one hundred ninety-nine billion "
            "two hundred fifty-four million seven hundred forty thousand "
            "nine hundred ninety-one"
        ))

    def test_out_of_range(self):
        with self.assertRaises(ValueError):
            int_to_words(2 ** 53)
        with self.assertRaises(ValueError):
            int_to_words(-(2 ** 53) - 1)

    def test_rejects_non_int(self):
        with self.assertRaises(ValueError):
            int_to_words(3.0)
        with self.assertRaises(ValueError):
            int_to_words("7")
        # bool is a subclass of int but must be rejected to avoid surprises.
        with self.assertRaises(ValueError):
            int_to_words(True)


if __name__ == "__main__":
    unittest.main()
