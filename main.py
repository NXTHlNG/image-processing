# main.py

import tkinter as tk
from tkinter import filedialog
import os
from color_conversion import RGB_CONVERSIONS  # Импорт словаря функций преобразования
from constants import THUMBNAIL_SIZE, SUPPORTED_IMAGE_FORMATS, COLOR_DEPTH, COLOR_MODELS  # Импорт констант
from canvas_manager import CanvasManager  # Импорт класса для работы с холстом
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np

# Глобальные переменные для хранения текущего выбранного пикселя
current_pixel = None
current_contrast = 1.0
current_brightness = 1.0
current_color = 1.0
current_model = 'RGB'

# Функция для загрузки изображения
def load_image():
    global current_pixel, current_contrast, current_brightness, current_color, current_model
    current_pixel = None
    current_contrast = 1.0
    current_brightness = 1.0
    current_color = 1.0
    current_model = 'RGB'
    try:
        file_path = filedialog.askopenfilename(filetypes=SUPPORTED_IMAGE_FORMATS)
        if file_path:
            global file_size, file_format
            canvas_manager.load_image(file_path)
            
            file_size = os.path.getsize(file_path)
            file_size_kb = file_size / 1024
            file_size_mb = file_size_kb / 1024
            file_format = canvas_manager.img.format
            depth = COLOR_DEPTH.get(canvas_manager.img.mode, "Неизвестно")
            color_model = canvas_manager.img.mode
            current_model = color_model

            update_image_info(canvas_manager.original_width, canvas_manager.original_height, file_size_kb, file_size_mb, file_format, depth, color_model)
            reset_pixel_selection()
            plot_histogram(canvas_manager.img)
    except Exception as e:
        print(f"Ошибка при загрузке изображения: {e}")

# Функция для обновления информации об изображении
def update_image_info(width, height, size_kb, size_mb, format, depth, color_model):
    info_text = (
        f"Информация об изображении:\n"
        f"Размер изображения: {width}x{height} пикселей\n"
        f"Размер файла: {size_kb:.2f} KB ({size_mb:.2f} MB)\n"
        f"Формат файла: {format}\n"
        f"Глубина цвета: {depth} бит\n"
        f"Цветовая модель: {color_model}"
    )
    info_label.config(text=info_text)

# Функция для выбора пикселя
def select_pixel(event):
    global current_pixel
    if canvas_manager.img:  # Проверяем, что изображение загружено
        x, y = event.x, event.y
        # Учитываем смещение изображения на холсте
        if (canvas_manager.offset_x <= x < canvas_manager.offset_x + canvas_manager.scaled_width and
            canvas_manager.offset_y <= y < canvas_manager.offset_y + canvas_manager.scaled_height):
            # Пересчитываем координаты относительно оригинального изображения
            img_x = int((x - canvas_manager.offset_x) * (canvas_manager.original_width / canvas_manager.scaled_width))
            img_y = int((y - canvas_manager.offset_y) * (canvas_manager.original_height / canvas_manager.scaled_height))
            rgb = canvas_manager.img.getpixel((img_x, img_y))
            current_pixel = rgb  # Сохраняем текущий пиксель
            pixel_info.config(text=f"Выбранный пиксель: ({img_x}, {img_y})\n RGB: {rgb}")
            update_color_display(rgb)  # Обновляем цвет квадрата
            convert_color(rgb)  # Выполняем преобразование
        else:
            pixel_info.config(text="Выберите пиксель на изображении")
    else:
        pixel_info.config(text="Сначала загрузите изображение")

# Функция для обновления цвета квадрата
def update_color_display(rgb):
    # Преобразуем RGB в HEX
    hex_color = "#{:02x}{:02x}{:02x}".format(*rgb)
    # Устанавливаем цвет фона для квадрата
    color_display.config(bg=hex_color)

# Функция для сброса выбора пикселя
def reset_pixel_selection():
    global current_pixel
    current_pixel = None  # Сбрасываем текущий пиксель
    pixel_info.config(text="Выберите пиксель на изображении")
    result_label.config(text="Результат:")
    # Сбрасываем цвет квадрата
    color_display.config(bg="lightgray")

# Функция для перевода цвета
def convert_color(rgb):
    model = model_var.get()
    if model in RGB_CONVERSIONS:
        result = RGB_CONVERSIONS[model](*rgb)
        # Округляем результат до 2 знаков после запятой
        rounded_result = tuple(round(value, 2) for value in result)
        result_label.config(text=f"{model}: {rounded_result}")
    else:
        print(f"Operation '{model}' is not supported.")

# Функция для обработки изменения модели
def on_model_change(*args):
    if current_pixel:  # Если пиксель выбран, выполняем перерасчет
        convert_color(current_pixel)

def apply_transformations():
    canvas_manager.change_image(current_brightness, current_contrast, current_color, current_model)
    # plot_histogram(canvas_manager.img)

def plot_histogram(image):
    if image is None:
        return

    # Создаем фигуру и оси
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)

    if image.mode == "L":
        # Для черно-белого изображения
        ax.hist(np.array(image).ravel(), bins=256, color='black', alpha=0.75)
    else:
        # Для цветного изображения
        colors = ("r", "g", "b")
        for i, color in enumerate(colors):
            ax.hist(np.array(image)[:, :, i].ravel(), bins=256, color=color, alpha=0.75)

    ax.set_title("Гистограмма изображения")
    ax.set_xlabel("Значение яркости")
    ax.set_ylabel("Количество пикселей")

    # Очищаем предыдущий график (если есть)
    for widget in histogram_frame.winfo_children():
        widget.destroy()

    # Встраиваем график в интерфейс
    canvas = FigureCanvasTkAgg(fig, master=histogram_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Добавляем панель инструментов (опционально)
    toolbar = NavigationToolbar2Tk(canvas, histogram_frame)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def update_brightness(event=None):
    global current_brightness
    current_brightness = brightness_scale.get()  # Обновляем значение яркости
    apply_transformations()  # Применяем оба преобразования

def update_contrast(event=None):
    global current_contrast
    current_contrast = contrast_scale.get()  # Обновляем значение контрастности
    apply_transformations()  # Применяем оба преобразования

def update_color(event=None):
    global current_color
    current_color = color_scale.get()  # Обновляем значение контрастности
    apply_transformations()  # Применяем оба преобразования

def apply_grayscale(event=None):
    global current_model
    current_model = "L"
    apply_transformations()  # Применяем оба преобразования

# Создание GUI
root = tk.Tk()
root.title("ААААААААААААААА")

# Левая часть: изображение и кнопка загрузки
left_frame = tk.Frame(root)
left_frame.grid(row=0, column=0, padx=10, pady=10)

# Холст для отображения изображения
canvas = tk.Canvas(left_frame, width=THUMBNAIL_SIZE[0], height=THUMBNAIL_SIZE[1], bg="lightgray")
canvas.pack(pady=10)

# Плейсхолдер для изображения
canvas.create_text(
    THUMBNAIL_SIZE[0] // 2, THUMBNAIL_SIZE[1] // 2,
    text="Загрузите изображение",
    font=("Arial", 14),
    fill="gray"
)

# Кнопка для загрузки изображения
load_button = tk.Button(left_frame, text="Загрузить изображение", command=load_image)
load_button.pack(pady=10)

# Правая часть: информация, выбор модели и результаты
right_frame = tk.Frame(root)  # Фиксированная ширина
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")
# right_frame.grid_propagate(False)  # Фиксируем размер фрейма


# Поле для вывода информации о выбранном пикселе
pixel_info = tk.Label(right_frame, text="Выберите пиксель на изображении")
pixel_info.pack(pady=10)

pixel_frame = tk.Frame(right_frame)
pixel_frame.pack(pady = 10)

# Квадрат для отображения цвета выбранного пикселя
color_display = tk.Label(pixel_frame, width=10, height=2, bg="lightgray", relief="solid")
color_display.pack(side=tk.LEFT, padx=5)

# Кнопка для сброса выбора пикселя
reset_button = tk.Button(pixel_frame, text="Сбросить", command=reset_pixel_selection)
reset_button.pack(side=tk.LEFT, padx=5)

convert_frame = tk.Frame(right_frame)
convert_frame.pack(pady = 10)

tk.Label(convert_frame, text="Конвертация пикселя:", anchor='w', justify=tk.LEFT).pack(pady=5)

# Выпадающий список для выбора модели
model_var = tk.StringVar(value=COLOR_MODELS[0])  # Используем константу
model_menu = tk.OptionMenu(convert_frame, model_var, *COLOR_MODELS)  # Используем константу
model_menu.pack(side=tk.LEFT, padx=5)

# Привязываем событие изменения модели
model_var.trace("w", on_model_change)

# Поле для вывода результата
result_label = tk.Label(convert_frame, text="Результат:", width=30, anchor='w', justify=tk.LEFT)
result_label.pack(side=tk.LEFT, padx=5)


adjust_frame = tk.Frame(right_frame)
adjust_frame.pack(pady=10)

# Добавляем ползунок для яркости
brightness_label = tk.Label(adjust_frame, text="Яркость:")
brightness_label.grid(column=0, row=0, sticky='ws')

brightness_scale = tk.Scale(adjust_frame, from_=0, to=2.0, resolution=0.01, orient=tk.HORIZONTAL, length=200)
brightness_scale.set(1.0)  # Устанавливаем начальное значение
brightness_scale.grid(column=1, row=0)

# Добавляем ползунок для контрастности
contrast_label = tk.Label(adjust_frame, text="Контрастность:")
contrast_label.grid(column=0, row=1, sticky='ws')

contrast_scale = tk.Scale(adjust_frame, from_=0, to=2.0, resolution=0.01, orient=tk.HORIZONTAL, length=200)
contrast_scale.set(1.0)  # Устанавливаем начальное значение
contrast_scale.grid(column=1, row=1)

color_label = tk.Label(adjust_frame, text="Насыщенность:")
color_label.grid(column=0, row=2, sticky='ws')

color_scale = tk.Scale(adjust_frame, from_=0, to=2.0, resolution=0.01, orient=tk.HORIZONTAL, length=200)
color_scale.set(1.0)  # Устанавливаем начальное значение
color_scale.grid(column=1, row=2)

# Привязываем события изменения ползунков к функциям
brightness_scale.bind("<ButtonRelease-1>", update_brightness)
contrast_scale.bind("<ButtonRelease-1>", update_contrast)
color_scale.bind("<ButtonRelease-1>", update_color)


# Поле для вывода информации об изображении
info_label = tk.Label(right_frame, text="Информация об изображении", justify=tk.LEFT)
info_label.pack(pady=10)

histogram_frame = tk.Frame(right_frame)
histogram_frame.pack(fill=tk.BOTH, expand=True)

# Создаем экземпляр CanvasManager
canvas_manager = CanvasManager(canvas)

# Привязываем событие клика к функции выбора пикселя
canvas.bind("<Button-1>", select_pixel)

# Добавляем кнопки для новых функций
grayscale_button = tk.Button(left_frame, text="В градации серого", command=lambda: apply_grayscale())
grayscale_button.pack(pady=5)

histogram_button = tk.Button(left_frame, text="Построить гистограмму", command=lambda: plot_histogram(canvas_manager.img))
histogram_button.pack(pady=5)

# Запуск приложения
root.mainloop()