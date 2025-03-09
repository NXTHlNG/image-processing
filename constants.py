# constants.py

# Размеры для уменьшения изображения (thumbnail)
from color_conversion import CMYK, HSL, LAB, HSV, YCBCR


THUMBNAIL_SIZE = (1600, 900)

# Путь к файлу с функциями преобразования цветов
COLOR_CONVERSION_FILE = "color_conversion.py"

# Форматы изображений, которые можно загружать
SUPPORTED_IMAGE_FORMATS = [
    ("JPEG files", "*.jpg"),
    ("PNG files", "*.png"),
    ("All files", "*.*")
]

# Глубина цвета для разных режимов изображения
COLOR_DEPTH = {
    "L": 8,      # Градации серого
    "RGB": 24,   # TrueColor
    "RGBA": 32   # TrueColor + альфа-канал
}

# Названия цветовых моделей
COLOR_MODELS = [
    CMYK,
    HSL,
    LAB,
    HSV,
    YCBCR,
]