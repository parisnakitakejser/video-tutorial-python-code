import unittest
from datetime import datetime, date

from library.person import Person
from library.alcohol import Alcohol


class TestAllowedToBuyAlcohol(unittest.TestCase):
    def setUp(self) -> None:
        self.__test_date_str = '1985-10-21'
        self.__person = Person()
        self.__alcohol = Alcohol()

    def tearDown(self) -> None:
        del self.__person
        del self.__alcohol

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
        self.assertEqual(True, self.__person.allowed_to_buy_alcohol(self.convert_str_to_datetime(date_str=self.__test_date_str), 46.6))

    def test_alcohol_calc_units(self):
        assert 1.01 == self.__alcohol.calc_unit(cl=33, percentage=4.6)
        assert 14.0 == self.__alcohol.calc_unit(cl=70, percentage=30)
        assert 20.0 == self.__alcohol.calc_unit(cl=30, percentage=100)

    def test_convert_unit_to_gram(self):
        assert 12 == self.__alcohol.unit_to_gram(units=1)
        assert 18 == self.__alcohol.unit_to_gram(units=1.5)
        assert 45 == self.__alcohol.unit_to_gram(units=3.75)

if __name__ == '__main__':
    unittest.main()
