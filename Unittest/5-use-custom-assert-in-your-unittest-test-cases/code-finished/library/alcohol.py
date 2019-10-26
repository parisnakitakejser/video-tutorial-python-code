class Alcohol:
    @staticmethod
    def calc_unit(cl, percentage):
        return round((cl * percentage) / (100 * 1.5), 2)

    @staticmethod
    def unit_to_gram(units):
        return round(units * 12)