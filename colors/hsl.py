class HSL:
    def __init__(self, H, S, L):
        """
        Инициализация класса HSL.
        :param H: Оттенок (0-1)
        :param S: Насыщенность (0-1)
        :param L: Светлота (0-1)
        """
        self.H = H
        self.S = S
        self.L = L

    def __str__(self):
        return f"HSL(H={self.H}, S={self.S}, L={self.L})"