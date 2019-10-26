import unittest

from library.person import Person


class TestAllowedToBuyAlcohol(unittest.TestCase):
    def test_age_are_to_low_to_buy(self):
        self.assertEqual(True, False)

    def test_age_its_allowed_to_buy(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
