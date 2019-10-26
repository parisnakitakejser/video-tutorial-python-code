from datetime import date

class Person:
    @staticmethod
    def __alcohol_restrictions_to_buy():
        # age 16-18: < 16.5%
        # age 18 and over: > 16.5%

        return [
            (18, 100.0),
            (16, 16.5)
        ]

    def allowed_to_buy_alcohol(self, birthday, alcohol_percentage):
        today = date.today()
        age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

        for artb in self.__alcohol_restrictions_to_buy():
            if age >= artb[0] and alcohol_percentage <= artb[1]:
                return True

        return False

    def allowed_to_buy_tobacco(self, birthday):
        # age 18 and over
        pass
