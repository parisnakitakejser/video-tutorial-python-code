import unittest
from datetime import datetime, date

from library.person import Person


class TestAllowedToBuyAlcohol(unittest.TestCase):
    def setUp(self) -> None:
        self.__test_date_str = '1985-10-21'
        self.__person = Person()

    def tearDown(self) -> None:
        del self.__person

    @staticmethod
    def convert_str_to_datetime(date_str, age_limit=None):
        today = date.today()

        dt = datetime.strptime(date_str, '%Y-%m-%d')
        age = today.year - dt.year - ((today.month, today.day) < (dt.month, dt.day))

        if age_limit and age > age_limit:
            add_years = age - age_limit
            dt = dt.replace(year=dt.year + add_years)

        return dt

    def test_age_are_to_low_to_buy(self):
        self.assertEqual(False, self.__person.allowed_to_buy_alcohol(self.convert_str_to_datetime(date_str=self.__test_date_str, age_limit=15), 4.6))
        self.assertEqual(False, self.__person.allowed_to_buy_alcohol(self.convert_str_to_datetime(date_str=self.__test_date_str, age_limit=17), 30.4))
        self.assertEqual(False, self.__person.allowed_to_buy_alcohol(self.convert_str_to_datetime(date_str=self.__test_date_str, age_limit=16), 24))

    def test_age_its_allowed_to_buy(self):
        self.assertEqual(True, self.__person.allowed_to_buy_alcohol('', 46.6))


if __name__ == '__main__':
    unittest.main()
