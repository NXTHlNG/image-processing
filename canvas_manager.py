# canvas_manager.py

from PIL import Image, ImageTk, ImageEnhance
import tkinter as tk
import cv2
import numpy as np

class CanvasManager:
    def __init__(self, canvas):
        self.canvas = canvas
        self.img = None
        self.original_img = None
        self.photo = None
        self.original_width = 0
        self.original_height = 0
        self.scaled_width = 0
        self.scaled_height = 0
        self.offset_x = 0
        self.offset_y = 0
        self.brightness = 1.0
        self.contrast = 1.0
        self.color = 1.0
        self.sharpness = 1.0
        self.mode = "RGB"

    def load_image(self, file_path):
        """Загружает изображение и инициализирует обработку"""
        self.original_img = Image.open(file_path)
        self.img = self.original_img.copy()
        self.original_width, self.original_height = self.img.size
        self.mode = self.img.mode
        self.render()

    def render(self):
        """Отрисовывает изображение на холсте с сохранением пропорций"""
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if self.original_width == 0 or self.original_height == 0:
            return

        img_ratio = self.original_width / self.original_height
        canvas_ratio = canvas_width / canvas_height

        if img_ratio > canvas_ratio:
            self.scaled_width = canvas_width
            self.scaled_height = int(canvas_width / img_ratio)
        else:
            self.scaled_height = canvas_height
            self.scaled_width = int(canvas_height * img_ratio)

        scaled_image = self.img.resize(
            (self.scaled_width, self.scaled_height),
            Image.Resampling.LANCZOS
        )
        self.photo = ImageTk.PhotoImage(scaled_image)
        
        self.canvas.delete("all")
        self.offset_x = (canvas_width - self.scaled_width) // 2
        self.offset_y = (canvas_height - self.scaled_height) // 2
        self.canvas.create_image(
            self.offset_x, 
            self.offset_y, 
            anchor=tk.NW, 
            image=self.photo
        )

    def get_pixel_color(self, x, y):
        """Возвращает цвет пикселя по координатам на холсте"""
        if self.img and (
            self.offset_x <= x < self.offset_x + self.scaled_width and
            self.offset_y <= y < self.offset_y + self.scaled_height
        ):
            img_x = int((x - self.offset_x) * (self.original_width / self.scaled_width))
            img_y = int((y - self.offset_y) * (self.original_height / self.scaled_height))
            return self.img.getpixel((img_x, img_y))
        return None
    
    def change_image(self, brightness: float, contrast: float, color: float, sharpness: float, mode: str):
        print(f'Change brightness from {self.brightness} to {brightness}')
        self.brightness = brightness
        self.img = ImageEnhance.Brightness(self.original_img).enhance(brightness)
        print(f'Change contrast from {self.contrast} to {contrast}')
        self.contrast = contrast
        self.img = ImageEnhance.Contrast(self.img).enhance(contrast)
        print(f'Change color from {self.color} to {color}')
        self.color = color
        self.img = ImageEnhance.Color(self.img).enhance(color)
        print(f'Change sharpness from {self.sharpness} to {sharpness}')
        self.sharpness = sharpness
        self.img = ImageEnhance.Sharpness(self.img).enhance(sharpness)
        print(f'Change mode from {self.mode} to {mode}')
        self.mode = mode
        self.img = self.img.convert(mode)
        self.render()

    def pil_to_cv2(self):
        """Конвертирует PIL Image в совместимый с OpenCV формат"""
        try:
            # Конвертируем в RGB для удаления альфа-канала и других специальных режимов
            if self.img.mode != 'RGB':
                if self.img.mode == 'L':
                    # Градации серого
                    return np.array(self.img)
                else:
                    rgb_img = self.img.convert('RGB')
                    return np.array(rgb_img)[:, :, ::-1]
            else:
                # Стандартный RGB
                return np.array(self.img)[:, :, ::-1]  # RGB -> BGR
                
        except Exception as e:
            print(f"Ошибка конвертации: {str(e)}")
            raise

    def cv2_to_pil(self, cv_image):
        """Конвертирует OpenCV image обратно в PIL Image"""
        try:
            if len(cv_image.shape) == 2:
                # Одноканальное изображение (grayscale)
                return Image.fromarray(cv_image, 'L')
            elif cv_image.shape[2] == 3:
                # Цветное изображение (BGR -> RGB)
                return Image.fromarray(cv_image[:, :, ::-1], 'RGB')
            elif cv_image.shape[2] == 4:
                # С альфа-каналом (не поддерживается OpenCV)
                return Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGRA2RGBA), 'RGBA')
        except Exception as e:
            print(f"Ошибка обратной конвертации: {str(e)}")
            raise

    # Обновленный метод apply_morph_operation
    def apply_morph_operation(self, operation, kernel, iterations=1):
        """Применяет морфологическую операцию"""
        try:
            # Конвертация в OpenCV формат
            cv_image = self.pil_to_cv2()
            
            # Применение операции
            if operation == 'Erosion':
                result = cv2.erode(cv_image, kernel['matrix'], iterations=iterations)
            elif operation == 'Dilation':
                result = cv2.dilate(cv_image, kernel['matrix'], iterations=iterations)
            elif operation == 'Opening':
                result = cv2.morphologyEx(cv_image, cv2.MORPH_OPEN, kernel['matrix'], iterations=iterations)
            elif operation == 'Closing':
                result = cv2.morphologyEx(cv_image, cv2.MORPH_CLOSE, kernel['matrix'], iterations=iterations)
            elif operation == 'Gradient':
                result = cv2.morphologyEx(cv_image, cv2.MORPH_GRADIENT, kernel['matrix'], iterations=iterations)

            # Обратная конвертация
            self.img = self.cv2_to_pil(result)
            self.render()

        except Exception as e:
            print(f"Ошибка операции: {str(e)}")
            raise