class YCbCr:
    def __init__(self, Y, Cb, Cr):
        """
        Инициализация класса YCbCr
        """
        self.Y = Y
        self.Cb = Cb
        self.Cr = Cr

    def __str__(self):
        return f"YCbCr(Y={self.Y}, Cb={self.Cb}, Cr={self.Cr})"