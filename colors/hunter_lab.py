class HunterLab:
    def __init__(self, L, A, B):
        """
        Инициализация класса CieLab
        """
        self.L = L
        self.A = A
        self.B = B

    def __str__(self):
        return f"HunterLab(L={self.L}, A={self.A}, B={self.B})"