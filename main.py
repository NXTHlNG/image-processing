# main.py

import tkinter as tk
from tkinter import filedialog, ttk
import os
from color_conversion import RGB_CONVERSIONS
from constants import THUMBNAIL_SIZE, SUPPORTED_IMAGE_FORMATS, COLOR_DEPTH, COLOR_MODELS
from canvas_manager import CanvasManager
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np

# Глобальные переменные
current_pixel = None
current_contrast = 1.0
current_brightness = 1.0
current_color = 1.0
current_sharpness = 1.0
current_model = 'RGB'

def load_image():
    global current_pixel, current_contrast, current_brightness, current_color, current_model, current_sharpness
    current_pixel = None
    current_contrast = 1.0
    current_brightness = 1.0
    current_color = 1.0
    current_sharpness = 1.0
    current_model = 'RGB'
    try:
        file_path = filedialog.askopenfilename(filetypes=SUPPORTED_IMAGE_FORMATS)
        if file_path:
            global file_size, file_format
            canvas_manager.load_image(file_path)
            
            file_size = os.path.getsize(file_path)
            file_size_kb = file_size / 1024
            file_size_mb = file_size_kb / 1024
            file_format = canvas_manager.original_img.format
            depth = COLOR_DEPTH.get(canvas_manager.img.mode, "Неизвестно")
            color_model = canvas_manager.img.mode
            current_model = color_model

            update_image_info(canvas_manager.original_width, canvas_manager.original_height, 
                             file_size_kb, file_size_mb, file_format, depth, color_model)
            reset_pixel_selection()
            plot_histogram(canvas_manager.img)
    except Exception as e:
        print(f"Ошибка при загрузке изображения: {e}")

def update_image_info(width, height, size_kb, size_mb, format, depth, color_model):
    info_text = (
        f"Размер: {width}x{height} пикселей\n"
        f"Размер файла: {size_kb:.2f} KB ({size_mb:.2f} MB)\n"
        f"Формат: {format}\n"
        f"Глубина цвета: {depth} бит\n"
        f"Цветовая модель: {color_model}"
    )
    info_label.config(text=info_text)

def select_pixel(event):
    global current_pixel
    if canvas_manager.img:
        x, y = event.x, event.y
        if (canvas_manager.offset_x <= x < canvas_manager.offset_x + canvas_manager.scaled_width and
            canvas_manager.offset_y <= y < canvas_manager.offset_y + canvas_manager.scaled_height):
            img_x = int((x - canvas_manager.offset_x) * (canvas_manager.original_width / canvas_manager.scaled_width))
            img_y = int((y - canvas_manager.offset_y) * (canvas_manager.original_height / canvas_manager.scaled_height))
            rgb = canvas_manager.img.getpixel((img_x, img_y))
            current_pixel = rgb
            pixel_info.config(text=f"X: {img_x}, Y: {img_y}\nRGB: {rgb}")
            update_color_display(rgb)
            convert_color(rgb)
        else:
            pixel_info.config(text="X: -, Y: -\nRGB: (-, -, -)")

def update_color_display(rgb):
    hex_color = "#{:02x}{:02x}{:02x}".format(*rgb)
    color_display.config(bg=hex_color)

def reset_pixel_selection():
    global current_pixel
    current_pixel = None
    pixel_info.config(text="X: -, Y: -\nRGB: (-, -, -)")
    result_label.config(text="Результат:")
    color_display.config(bg="lightgray")

def convert_color(rgb):
    model = model_var.get()
    if model in RGB_CONVERSIONS:
        result = RGB_CONVERSIONS[model](*rgb)
        rounded_result = tuple(round(value, 2) for value in result)
        result_label.config(text=f"{model}: {rounded_result}")
    else:
        print(f"Операция '{model}' не поддерживается")

def on_model_change(*args):
    if current_pixel:
        convert_color(current_pixel)

def apply_transformations():
    canvas_manager.change_image(current_brightness, current_contrast, current_color, current_sharpness, current_model)
    # plot_histogram(canvas_manager.img)

def plot_histogram(image):
    fig = Figure(figsize=(4, 3), dpi=100)
    ax = fig.add_subplot(111)

    if image is not None:
        if image.mode == "L":
         ax.hist(np.array(image).ravel(), bins=256, color='black', alpha=0.75)
        else:
            colors = ("r", "g", "b")
            for i, color in enumerate(colors):
                ax.hist(np.array(image)[:, :, i].ravel(), bins=256, color=color, alpha=0.75) 

    for widget in histogram_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=histogram_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    toolbar = NavigationToolbar2Tk(canvas, histogram_frame)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def update_brightness(scale):
    global current_brightness
    current_brightness = scale
    apply_transformations()

def update_contrast(scale):
    global current_contrast
    current_contrast = scale
    apply_transformations()

def update_color(scale):
    global current_color
    current_color = scale
    apply_transformations()

def update_sharpness(scale):
    global current_sharpness
    current_sharpness = scale
    apply_transformations()


def apply_grayscale(event=None):
    global current_model
    current_model = "L"
    apply_transformations()

# Морфологические операции
kernel_editor = None
kernel_matrix = []
current_kernel_size = 3

def create_kernel_grid(size):
    global kernel_editor, kernel_matrix
    if kernel_editor:
        kernel_editor.destroy()
    
    kernel_editor = tk.Canvas(kernel_editor_frame, width=size*30, height=size*30)
    kernel_editor.pack(pady=5)
    
    kernel_matrix = []
    cell_size = 30
    for i in range(size):
        row = []
        for j in range(size):
            x1 = j * cell_size
            y1 = i * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            rect = kernel_editor.create_rectangle(x1, y1, x2, y2, fill="white", outline="gray")
            kernel_editor.tag_bind(rect, "<Button-1>", lambda e, i=i, j=j: toggle_cell(i, j))
            row.append(0)
        kernel_matrix.append(row)
    return kernel_matrix

def toggle_cell(i, j):
    color = "white"
    if kernel_matrix[i][j] == 0:
        kernel_matrix[i][j] = 1
        color = "black"
    else:
        kernel_matrix[i][j] = 0
    kernel_editor.itemconfig(i*current_kernel_size + j + 1, fill=color)

def update_kernel_size():
    global current_kernel_size
    current_kernel_size = kernel_size_var.get()
    create_kernel_grid(current_kernel_size)

def get_kernel_matrix():
    return np.array(kernel_matrix, dtype=np.uint8)

def apply_morphology():
    if canvas_manager.img:
        try:
            kernel = {
                "matrix": get_kernel_matrix(),
                "anchor": (-1, -1)
            }
            canvas_manager.apply_morph_operation(
                operation=operation_var.get(),
                kernel=kernel,
                iterations=1
            )
        except Exception as e:
            print(f"Ошибка: {str(e)}")
    else:
        print("Сначала загрузите изображение")

# style = ttk.Style()
# style.configure('TFrame', background='#f0f0f0')
# style.configure('TButton', padding=3)
# style.configure('TCombobox', padding=3)
# style.configure('TLabel', padding=3, background='#f0f0f0')

root = tk.Tk()
root.title("Image Processing Tool")

# Верхний тулбар
toolbar_frame = tk.Frame(root, borderwidth=2, relief="groove")
toolbar_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

# Кнопка загрузки в тулбаре
load_button = ttk.Button(toolbar_frame, text="Загрузить изображение", command=load_image)
load_button.pack(side=tk.LEFT, padx=5, pady=2)

# Левая панель (только холст)
left_frame = tk.Frame(root)
left_frame.grid(row=1, column=0, padx=5, pady=5)

# Холст для изображения
canvas = tk.Canvas(left_frame, width=THUMBNAIL_SIZE[0], height=THUMBNAIL_SIZE[1], bg="lightgray")
canvas.pack(pady=5)
canvas.create_text(THUMBNAIL_SIZE[0]//2, THUMBNAIL_SIZE[1]//2, 
                 text="Загрузите изображение", font=("Arial", 14), fill="gray")

# Правая панель
right_frame = tk.Frame(root)
right_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

# Создаем Canvas и Scrollbar 
right_canvas = tk.Canvas(right_frame, borderwidth=0, width=400)
scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=right_canvas.yview)
scrollable_frame = ttk.Frame(right_canvas)

# Настройка прокрутки
scrollable_frame.bind(
    "<Configure>",
    lambda e: right_canvas.configure(
        scrollregion=right_canvas.bbox("all")
    )
)

right_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
right_canvas.configure(yscrollcommand=scrollbar.set)

# Размещаем элементы
right_canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Блок информации о пикселе
pixel_frame = tk.Frame(scrollable_frame, borderwidth=2, relief="groove")
pixel_frame.pack(pady=5, fill=tk.X, padx=5, expand=True)

# Строка с цветом и информацией
color_display = tk.Label(pixel_frame, width=6, height=2, bg="lightgray", relief="solid")
color_display.pack(side=tk.LEFT, padx=5, pady=5)

pixel_info = tk.Label(pixel_frame, text="X: -, Y: -\nRGB: (-, -, -)", justify=tk.LEFT)
pixel_info.pack(side=tk.LEFT, padx=5)

reset_button = ttk.Button(pixel_frame, text="Сбросить", command=reset_pixel_selection)
reset_button.pack(side=tk.RIGHT, padx=5, pady=5)

# Блок цветовых преобразований
convert_frame = tk.Frame(scrollable_frame, borderwidth=2, relief="groove")
convert_frame.pack(pady=5, fill=tk.X, padx=5)

tk.Label(convert_frame, text="Цветовые преобразования", font=('Arial', 10, 'bold')).pack(pady=5, fill=tk.X)
model_var = tk.StringVar(value=COLOR_MODELS[0])
model_menu = ttk.Combobox(convert_frame, textvariable=model_var, values=COLOR_MODELS, state="readonly")
model_menu.pack(pady=5, padx=5, fill=tk.X)
result_label = tk.Label(convert_frame, text="Результат: ", anchor='w')
result_label.pack(pady=5, padx=5, fill=tk.X)
# Привязываем событие изменения модели
model_var.trace("w", on_model_change)

# Блок настроек изображения
adjust_frame = tk.Frame(scrollable_frame, borderwidth=2, relief="groove")
adjust_frame.pack(pady=5, fill=tk.X, padx=5)

tk.Label(adjust_frame, text="Коррекция изображения", font=('Arial', 10, 'bold')).pack(pady=5)

# Ползунки
controls = [
    ("Яркость", update_brightness),
    ("Контраст", update_contrast),
    ("Насыщенность", update_color),
    ("Резкость", update_sharpness)
]
i = 0
for text, callback in controls:
    frame = tk.Frame(adjust_frame)
    frame.pack(pady=2, fill=tk.X)
    tk.Label(frame, text=text, width=12, anchor='w').grid(row=i, column=0, sticky='ws')
    scale = ttk.Scale(frame, from_=0, to=2.0, orient=tk.HORIZONTAL, length=200)
    scale.set(1.0)
    scale.bind("<ButtonRelease-1>", lambda e, v=scale, cb=callback: cb(v.get()))
    scale.grid(row=i, column=1)
    i+=1

grayscale_button = ttk.Button(adjust_frame, text="Градации серого", command=apply_grayscale)
grayscale_button.pack(pady=2, fill=tk.X)

# Морфологические операции
morph_frame = tk.Frame(scrollable_frame, borderwidth=2, relief="groove")
morph_frame.pack(pady=10, fill=tk.X, padx=5)
tk.Label(morph_frame, text="Морфологические операции", font=('Arial', 10, 'bold')).pack(pady=5)

# Выбор операции
operation_var = tk.StringVar(value="Erosion")
operations = ["Erosion", "Dilation", "Opening", "Closing", "Gradient"]
ttk.Label(morph_frame, text="Операция:").pack(anchor='w')
op_menu = ttk.Combobox(morph_frame, textvariable=operation_var, values=operations, state="readonly")
op_menu.pack(fill=tk.X, padx=5, pady=2)

# Графический редактор ядра
kernel_editor_frame = tk.Frame(morph_frame)
kernel_editor_frame.pack(pady=5)

# Панель управления размером
size_frame = tk.Frame(morph_frame)
size_frame.pack(fill=tk.X, padx=5, pady=2)

ttk.Label(size_frame, text="Размер ядра:").pack(side=tk.LEFT)
kernel_size_var = tk.IntVar(value=3)
size_spin = ttk.Spinbox(
    size_frame, 
    from_=3, 
    to=11, 
    increment=2, 
    textvariable=kernel_size_var, 
    width=5,
    command=update_kernel_size
)
size_spin.pack(side=tk.LEFT, padx=5)

# Отдельный фрейм для кнопки
btn_frame = tk.Frame(morph_frame)
btn_frame.pack(fill=tk.X, pady=5)

apply_btn = ttk.Button(btn_frame, text="Применить", command=apply_morphology)
apply_btn.pack(anchor='center')  # Центрирование кнопки

# Инициализация сетки
create_kernel_grid(3)


# Гистограмма и информация
info_frame = tk.Frame(scrollable_frame, borderwidth=2, relief="groove")
info_frame.pack(pady=10, fill=tk.X, padx=5)
tk.Label(info_frame, text="Информация об изображении", font=('Arial', 10, 'bold')).pack(pady=5, padx=5)
info_text = (
        f"Размер: \n"
        f"Размер файла: \n"
        f"Формат: \n"
        f"Глубина цвета: \n"
        f"Цветовая модель: "
    )
info_label = tk.Label(info_frame, text=info_text, justify=tk.LEFT)
info_label.pack(pady=10, padx=5, anchor='w')

# Блок гистограммы
hist_frame = tk.Frame(scrollable_frame, borderwidth=2, relief="groove")
hist_frame.pack(pady=5, fill=tk.BOTH, expand=True, padx=5)

hist_header = tk.Frame(hist_frame)
hist_header.pack(fill=tk.X)
tk.Label(hist_header, text="Гистограмма", font=('Arial', 10, 'bold')).pack(pady=5)


histogram_frame = tk.Frame(hist_frame)
histogram_frame.pack(fill=tk.BOTH, expand=True)

hist_button = ttk.Button(hist_frame, text="Обновить", command=lambda: plot_histogram(canvas_manager.img))
hist_button.pack(pady=5)

plot_histogram(None)

# Инициализация менеджера
canvas_manager = CanvasManager(canvas)
canvas.bind("<Button-1>", select_pixel)

root.mainloop()