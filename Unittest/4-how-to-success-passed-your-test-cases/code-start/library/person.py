class Person:
    def allowed_to_buy_alcohol(self, birthday, alcohol_percentage):
        # age 16-18: < 16.5%
        # age 18 and over: > 16.5%
        print('birthday', birthday)
        print('alcohol_percentage', alcohol_percentage)

    def allowed_to_buy_tobacco(self, birthday):
        # age 18 and over
        pass
