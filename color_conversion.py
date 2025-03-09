# color_conversion.py

RGB = "RGB" 
HSV = "HSV"
HSL = "HSL"
CMY = "CMY"
CMYK = "CMYK"
XYZ = "XYZ"
YCBCR = "YCbCr"
SRGB = "sRGB"
HUNTER_LAB = "HUNTER_LAB"
LAB = "LAB"


# R, G и B входные значения в диапазоне 0 ÷ 255
# H, S и V выходные значения в диапазоне 0 ÷ 1.0

def rgb_to_hsv(R, G, B):
    var_R = R / 255
    var_G = G / 255
    var_B = B / 255

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

    return H, S, V

def rgb_to_cmy(R, G, B):
    C = 1 - (R / 255)
    M = 1 - (G / 255)
    Y = 1 - (B / 255)
    return C, M, Y

def cmy_to_cmyk(C, M, Y):
    var_K = 1  # Инициализация переменной для черного (Key/Black)

    # Находим минимальное значение из C, M, Y
    if C < var_K:
        var_K = C
    if M < var_K:
        var_K = M
    if Y < var_K:
        var_K = Y

    # Если var_K == 1, это означает, что цвет черный
    if var_K == 1:
        C = 0
        M = 0
        Y = 0
    else:
        # Корректируем значения C, M, Y
        C = (C - var_K) / (1 - var_K)
        M = (M - var_K) / (1 - var_K)
        Y = (Y - var_K) / (1 - var_K)

    K = var_K  # Значение черного (Key/Black)

    return C, M, Y, K

def rgb_to_cmyk(r, g, b):
    return cmy_to_cmyk(*rgb_to_cmy(r, g, b))

def rgb_to_hsl(R, G, B):
    var_R = R / 255
    var_G = G / 255
    var_B = B / 255

    var_Min = min(var_R, var_G, var_B)  # Минимальное значение из RGB
    var_Max = max(var_R, var_G, var_B)  # Максимальное значение из RGB
    del_Max = var_Max - var_Min         # Разница между максимальным и минимальным значениями

    L = (var_Max + var_Min) / 2  # Lightness (Яркость)

    if del_Max == 0:  # Если это оттенок серого, нет цветности...
        H = 0
        S = 0
    else:  # Если есть цветность...
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

    return H, S, L

def srgb_to_xyz(sR, sG, sB):
    # Нормализация значений sRGB в диапазон 0 ÷ 1
    var_R = sR / 255
    var_G = sG / 255
    var_B = sB / 255

    # Преобразование sRGB в линейное RGB
    if var_R > 0.04045:
        var_R = ((var_R + 0.055) / 1.055) ** 2.4
    else:
        var_R = var_R / 12.92

    if var_G > 0.04045:
        var_G = ((var_G + 0.055) / 1.055) ** 2.4
    else:
        var_G = var_G / 12.92

    if var_B > 0.04045:
        var_B = ((var_B + 0.055) / 1.055) ** 2.4
    else:
        var_B = var_B / 12.92

    # Масштабирование значений
    var_R = var_R * 100
    var_G = var_G * 100
    var_B = var_B * 100

    # Преобразование в XYZ
    X = var_R * 0.4124 + var_G * 0.3576 + var_B * 0.1805
    Y = var_R * 0.2126 + var_G * 0.7152 + var_B * 0.0722
    Z = var_R * 0.0193 + var_G * 0.1192 + var_B * 0.9505

    return X, Y, Z

def rgb_to_ycbcr(R, G, B):
    # Преобразование RGB в YCbCr по стандарту ITU-R BT.601
    Y = 0.299 * R + 0.587 * G + 0.114 * B
    Cb = -0.168736 * R - 0.331264 * G + 0.5 * B + 128
    Cr = 0.5 * R - 0.418688 * G - 0.081312 * B + 128

    # Ограничение значений Y, Cb, Cr в диапазоне 0-255
    Y = max(0, min(255, int(Y)))
    Cb = max(0, min(255, int(Cb)))
    Cr = max(0, min(255, int(Cr)))

    return Y, Cb, Cr

def rgb_to_ycbcr_bt709(R, G, B):
    # Преобразование RGB в YCbCr по стандарту ITU-R BT.709
    Y = 0.2126 * R + 0.7152 * G + 0.0722 * B
    Cb = -0.114572 * R - 0.385428 * G + 0.5 * B + 128
    Cr = 0.5 * R - 0.454153 * G - 0.045847 * B + 128

    # Ограничение значений Y, Cb, Cr в диапазоне 0-255
    Y = max(0, min(255, int(Y)))
    Cb = max(0, min(255, int(Cb)))
    Cr = max(0, min(255, int(Cr)))

    return Y, Cb, Cr


# Эталонные значения для различных источников освещения и углов наблюдения
reference_values = {
    "A": {
        "2°": {"X": 109.850, "Y": 100.000, "Z": 35.585},
        "10°": {"X": 111.144, "Y": 100.000, "Z": 35.200},
    },
    "B": {
        "2°": {"X": 99.0927, "Y": 100.000, "Z": 85.313},
        "10°": {"X": 99.178, "Y": 100.000, "Z": 84.3493},
    },
    "C": {
        "2°": {"X": 98.074, "Y": 100.000, "Z": 118.232},
        "10°": {"X": 97.285, "Y": 100.000, "Z": 116.145},
    },
    "D50": {
        "2°": {"X": 96.422, "Y": 100.000, "Z": 82.521},
        "10°": {"X": 96.720, "Y": 100.000, "Z": 81.427},
    },
    "D55": {
        "2°": {"X": 95.682, "Y": 100.000, "Z": 92.149},
        "10°": {"X": 95.799, "Y": 100.000, "Z": 90.926},
    },
    "D65": {
        "2°": {"X": 95.047, "Y": 100.000, "Z": 108.883},
        "10°": {"X": 94.811, "Y": 100.000, "Z": 107.304},
    },
    "D75": {
        "2°": {"X": 94.972, "Y": 100.000, "Z": 122.638},
        "10°": {"X": 94.416, "Y": 100.000, "Z": 120.641},
    },
    "E": {
        "2°": {"X": 100.000, "Y": 100.000, "Z": 100.000},
        "10°": {"X": 100.000, "Y": 100.000, "Z": 100.000},
    },
    "F1": {
        "2°": {"X": 92.834, "Y": 100.000, "Z": 103.665},
        "10°": {"X": 94.791, "Y": 100.000, "Z": 103.191},
    },
    "F2": {
        "2°": {"X": 99.187, "Y": 100.000, "Z": 67.395},
        "10°": {"X": 103.280, "Y": 100.000, "Z": 69.026},
    },
    "F3": {
        "2°": {"X": 103.754, "Y": 100.000, "Z": 49.861},
        "10°": {"X": 108.968, "Y": 100.000, "Z": 51.965},
    },
    "F4": {
        "2°": {"X": 109.147, "Y": 100.000, "Z": 38.813},
        "10°": {"X": 114.961, "Y": 100.000, "Z": 40.963},
    },
    "F5": {
        "2°": {"X": 90.872, "Y": 100.000, "Z": 98.723},
        "10°": {"X": 93.369, "Y": 100.000, "Z": 98.636},
    },
    "F6": {
        "2°": {"X": 97.309, "Y": 100.000, "Z": 60.191},
        "10°": {"X": 102.148, "Y": 100.000, "Z": 62.074},
    },
    "F7": {
        "2°": {"X": 95.044, "Y": 100.000, "Z": 108.755},
        "10°": {"X": 95.792, "Y": 100.000, "Z": 107.687},
    },
    "F8": {
        "2°": {"X": 96.413, "Y": 100.000, "Z": 82.333},
        "10°": {"X": 97.115, "Y": 100.000, "Z": 81.135},
    },
    "F9": {
        "2°": {"X": 100.365, "Y": 100.000, "Z": 67.868},
        "10°": {"X": 102.116, "Y": 100.000, "Z": 67.826},
    },
    "F10": {
        "2°": {"X": 96.174, "Y": 100.000, "Z": 81.712},
        "10°": {"X": 99.001, "Y": 100.000, "Z": 83.134},
    },
    "F11": {
        "2°": {"X": 100.966, "Y": 100.000, "Z": 64.370},
        "10°": {"X": 103.866, "Y": 100.000, "Z": 65.627},
    },
    "F12": {
        "2°": {"X": 108.046, "Y": 100.000, "Z": 39.228},
        "10°": {"X": 111.428, "Y": 100.000, "Z": 40.353},
    },
}

# Функция для преобразования XYZ в Hunter Lab
def xyz_to_hunter_lab(X, Y, Z, Reference_X, Reference_Y, Reference_Z):
    var_Ka = (175.0 / 198.04) * (Reference_Y + Reference_X)
    var_Kb = (70.0 / 218.11) * (Reference_Y + Reference_Z)

    Hunter_L = 100.0 * (Y / Reference_Y) ** 0.5
    Hunter_a = var_Ka * (((X / Reference_X) - (Y / Reference_Y)) / (Y / Reference_Y) ** 0.5)
    Hunter_b = var_Kb * (((Y / Reference_Y) - (Z / Reference_Z)) / (Y / Reference_Y) ** 0.5)

    return Hunter_L, Hunter_a, Hunter_b

def xyz_to_lab(X, Y, Z, Reference_X, Reference_Y, Reference_Z):
    # Нормализация значений XYZ
    var_X = X / Reference_X
    var_Y = Y / Reference_Y
    var_Z = Z / Reference_Z

    # Применение нелинейного преобразования
    def f(t):
        if t > 0.008856:
            return t ** (1 / 3)
        else:
            return (7.787 * t) + (16 / 116)

    var_X = f(var_X)
    var_Y = f(var_Y)
    var_Z = f(var_Z)

    # Вычисление значений CIELAB
    CIE_L = (116 * var_Y) - 16
    CIE_a = 500 * (var_X - var_Y)
    CIE_b = 200 * (var_Y - var_Z)

    return CIE_L, CIE_a, CIE_b


def rgb_to_cie_lab(R, G, B):
    return xyz_to_lab(*srgb_to_xyz(R, G, B), reference_values["A"]["2°"]["X"], reference_values["A"]["2°"]["Y"], reference_values["A"]["2°"]["Z"])

def rgb_to_hunter_lab(R, G, B):
    return xyz_to_hunter_lab(*srgb_to_xyz(R, G, B), reference_values["A"]["2°"]["X"], reference_values["A"]["2°"]["Y"], reference_values["A"]["2°"]["Z"])


RGB_CONVERSIONS = {
    CMYK: rgb_to_cmyk,
    HSL: rgb_to_hsl,
    HSV: rgb_to_hsv,
    LAB: rgb_to_cie_lab,
    HUNTER_LAB: rgb_to_hunter_lab,
    YCBCR: rgb_to_ycbcr,
}