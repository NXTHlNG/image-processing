# canvas_manager.py

from PIL import Image, ImageTk, ImageEnhance
import tkinter as tk

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
        self.mode = "RGB"
        self.brightness_enchancer = None
        self.contrast_enchancer = None
        self.color_enchancer = None

    def load_image(self, file_path):
        """Загружает изображение и отображает его на холсте."""
        self.original_img = Image.open(file_path)
        self.img = self.original_img
        self.original_width, self.original_height = self.img.size
        self.mode = self.original_img.mode
        self.render()

    def render(self):
        """Масштабирует изображение под размер холста и центрирует его."""
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Вычисляем соотношение сторон изображения и холста
        img_ratio = self.original_width / self.original_height
        canvas_ratio = canvas_width / canvas_height

        # Масштабируем изображение с сохранением пропорций
        if img_ratio > canvas_ratio:
            # Ширина изображения больше, чем ширина холста
            self.scaled_width = canvas_width
            self.scaled_height = int(canvas_width / img_ratio)
        else:
            # Высота изображения больше, чем высота холста
            self.scaled_height = canvas_height
            self.scaled_width = int(canvas_height * img_ratio)

        # Масштабируем изображение
        scaled_image = self.img.resize((self.scaled_width, self.scaled_height), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(scaled_image)

        # Очищаем холст и отображаем изображение по центру
        self.canvas.delete("all")
        self.offset_x = (canvas_width - self.scaled_width) // 2
        self.offset_y = (canvas_height - self.scaled_height) // 2
        self.canvas.create_image(self.offset_x, self.offset_y, anchor=tk.NW, image=self.photo)

    def get_pixel_color(self, x, y):
        """Возвращает цвет пикселя по координатам на холсте."""
        if self.img:
            # Учитываем смещение изображения на холсте
            if self.offset_x <= x < self.offset_x + self.scaled_width and self.offset_y <= y < self.offset_y + self.scaled_height:
                # Пересчитываем координаты относительно изображения
                img_x = int((x - self.offset_x) * (self.original_width / self.scaled_width))
                img_y = int((y - self.offset_y) * (self.original_height / self.scaled_height))
                return self.img.getpixel((img_x, img_y))
        return None
    
    def change_image(self, brightness: float, contrast: float, color: float, mode: str):
        print(f'Change brightness from {self.brightness} to {brightness}')
        self.brightness = brightness
        self.img = ImageEnhance.Brightness(self.original_img).enhance(brightness)
        print(f'Change contrast from {self.contrast} to {contrast}')
        self.contrast = contrast
        self.img = ImageEnhance.Contrast(self.img).enhance(contrast)
        print(f'Change color from {self.color} to {color}')
        self.color = color
        self.img = ImageEnhance.Color(self.img).enhance(color)
        print(f'Change mode from {self.mode} to {mode}')
        self.mode = mode
        self.img = self.img.convert(mode)
        self.render()

