import unittest

from library.person import Person


class TestAllowedToBuyAlcohol(unittest.TestCase):
    def setUp(self) -> None:
        self.__person = Person()

    def tearDown(self) -> None:
        del self.__person

    def test_age_are_to_low_to_buy(self):
        self.assertEqual(True, self.__person.allowed_to_buy_alcohol('', 4.6))

    def test_age_its_allowed_to_buy(self):
        self.assertEqual(True, self.__person.allowed_to_buy_alcohol('', 46.6))


if __name__ == '__main__':
    unittest.main()
