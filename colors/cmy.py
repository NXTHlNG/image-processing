from colors.cmyk import CMYK


class CMY:
    def __init__(self, C, M, Y):
        """
        Инициализация класса CMY.
        :param C: Голубой (0-1)
        :param M: Пурпурный (0-1)
        :param Y: Желтый (0-1)
        """
        self.C = C
        self.M = M
        self.Y = Y

    def to_cmyk(self):
        """
        Преобразует CMY в CMYK.
        :return: Объект класса CMYK
        """
        var_K = 1

        if self.C < var_K:
            var_K = self.C
        if self.M < var_K:
            var_K = self.M
        if self.Y < var_K:
            var_K = self.Y

        if var_K == 1:
            C = 0
            M = 0
            Y = 0
        else:
            C = (self.C - var_K) / (1 - var_K)
            M = (self.M - var_K) / (1 - var_K)
            Y = (self.Y - var_K) / (1 - var_K)

        K = var_K
        return CMYK(C, M, Y, K)

    def __str__(self):
        return f"CMY(C={self.C}, M={self.M}, Y={self.Y})"