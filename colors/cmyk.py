class CMYK:
    def __init__(self, C, M, Y, K):
        """
        Инициализация класса CMYK.
        :param C: Голубой (0-1)
        :param M: Пурпурный (0-1)
        :param Y: Желтый (0-1)
        :param K: Черный (0-1)
        """
        self.C = C
        self.M = M
        self.Y = Y
        self.K = K

    def __str__(self):
        return f"CMYK(C={self.C}, M={self.M}, Y={self.Y}, K={self.K})"