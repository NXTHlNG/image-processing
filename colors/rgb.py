from colors.cmy import CMY
from colors.hsl import HSL
from colors.hsv import HSV
from colors.ycbcr import YCbCr


class RGB:
    def __init__(self, R, G, B):
        """
        Инициализация класса RGB.
        :param R: Значение красного (0-255)
        :param G: Значение зеленого (0-255)
        :param B: Значение синего (0-255)
        """
        self.R = R
        self.G = G
        self.B = B

    def to_hsv(self):
        """
        Преобразует RGB в HSV.
        :return: Объект класса HSV
        """
        var_R = self.R / 255
        var_G = self.G / 255
        var_B = self.B / 255

        var_Min = min(var_R, var_G, var_B)  # Минимальное значение из RGB
        var_Max = max(var_R, var_G, var_B)  # Максимальное значение из RGB
        del_Max = var_Max - var_Min         # Разница между максимальным и минимальным значениями

        V = var_Max

        if del_Max == 0:  # Если это оттенок серого, нет цветности...
            H = 0
            S = 0
        else:  # Если есть цветность...
            S = del_Max / var_Max

            del_R = (((var_Max - var_R) / 6) + (del_Max / 2)) / del_Max
            del_G = (((var_Max - var_G) / 6) + (del_Max / 2)) / del_Max
            del_B = (((var_Max - var_B) / 6) + (del_Max / 2)) / del_Max

            if var_R == var_Max:
                H = del_B - del_G
            elif var_G == var_Max:
                H = (1 / 3) + del_R - del_B
            elif var_B == var_Max:
                H = (2 / 3) + del_G - del_R

            if H < 0:
                H += 1
            if H > 1:
                H -= 1

        return HSV(H, S, V)

    def to_cmy(self):
        """
        Преобразует RGB в CMY.
        :return: Объект класса CMY
        """
        C = 1 - (self.R / 255)
        M = 1 - (self.G / 255)
        Y = 1 - (self.B / 255)
        return CMY(C, M, Y)

    def to_cmyk(self):
        """
        Преобразует RGB в CMYK.
        :return: Объект класса CMYK
        """
        cmy = self.to_cmy()
        return cmy.to_cmyk()

    def to_hsl(self):
        """
        Преобразует RGB в HSL.
        :return: Объект класса HSL
        """
        var_R = self.R / 255
        var_G = self.G / 255
        var_B = self.B / 255

        var_Min = min(var_R, var_G, var_B)
        var_Max = max(var_R, var_G, var_B)
        del_Max = var_Max - var_Min

        L = (var_Max + var_Min) / 2

        if del_Max == 0:
            H = 0
            S = 0
        else:
            if L < 0.5:
                S = del_Max / (var_Max + var_Min)
            else:
                S = del_Max / (2 - var_Max - var_Min)

            del_R = (((var_Max - var_R) / 6) + (del_Max / 2)) / del_Max
            del_G = (((var_Max - var_G) / 6) + (del_Max / 2)) / del_Max
            del_B = (((var_Max - var_B) / 6) + (del_Max / 2)) / del_Max

            if var_R == var_Max:
                H = del_B - del_G
            elif var_G == var_Max:
                H = (1 / 3) + del_R - del_B
            elif var_B == var_Max:
                H = (2 / 3) + del_G - del_R

            if H < 0:
                H += 1
            if H > 1:
                H -= 1

        return HSL(H, S, L)
    
    def to_ycbcr(self):
        """
        Преобразует RGB в YCbCr по стандарту ITU-R BT.60.
        :return: Объект класса YCbCr
        """
        Y = 0.299 * self.R + 0.587 * self.G + 0.114 * self.B
        Cb = -0.168736 * self.R - 0.331264 * self.G + 0.5 * self.B + 128
        Cr = 0.5 * self.R - 0.418688 * self.G - 0.081312 * self.B + 128

        # Ограничение значений Y, Cb, Cr в диапазоне 0-255
        Y = max(0, min(255, int(Y)))
        Cb = max(0, min(255, int(Cb)))
        Cr = max(0, min(255, int(Cr)))

        return YCbCr(Y, Cb, Cr)
    
    def to_ycbcr_bt709(self):
        """
        Преобразует RGB в YCbCr по стандарту ITU-R BT.709
        :return: Объект класса YCbCr
        """
        # Преобразование RGB в YCbCr по стандарту ITU-R BT.709
        Y = 0.2126 * self.R + 0.7152 * self.G + 0.0722 * self.B
        Cb = -0.114572 * self.R - 0.385428 * self.G + 0.5 * self.B + 128
        Cr = 0.5 * self.R - 0.454153 * self.G - 0.045847 * self.B + 128

        # Ограничение значений Y, Cb, Cr в диапазоне 0-255
        Y = max(0, min(255, int(Y)))
        Cb = max(0, min(255, int(Cb)))
        Cr = max(0, min(255, int(Cr)))

        return YCbCr(Y, Cb, Cr)

    def __str__(self):
        return f"RGB(R={self.R}, G={self.G}, B={self.B})"