class HSV:
    def __init__(self, H, S, V):
        """
        Инициализация класса HSV.
        :param H: Оттенок (0-1)
        :param S: Насыщенность (0-1)
        :param V: Яркость (0-1)
        """
        self.H = H
        self.S = S
        self.V = V

    def __str__(self):
        return f"HSV(H={self.H}, S={self.S}, V={self.V})"