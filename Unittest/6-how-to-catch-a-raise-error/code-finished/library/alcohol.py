class Alcohol:
    @staticmethod
    def calc_unit(cl, percentage):
        if not isinstance(percentage, int) and not isinstance(percentage, float):
            raise ValueError
        elif not isinstance(cl, int) and not isinstance(cl, float):
            raise ValueError
        elif percentage > 100 or percentage < 0:
            raise ValueError

        return round((cl * percentage) / (100 * 1.5), 2)

    @staticmethod
    def unit_to_gram(units):
        return round(units * 12)