import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Программа для рисования")

        # Создаем изображение и объект для рисования
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        # Создаем холст TKinter
        self.canvas = tk.Canvas(root, bg="white", width=600, height=400)
        self.canvas.pack()

        # Инициализация атрибутов кисти
        self.last_x, self.last_y = None, None
        self.brush_color = "black"
        self.brush_size = 5
        self.previous_color = self.brush_color  # Сохраняем предыдущий цвет кисти

        self.setup_ui()

        # Привязка событий
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

    def setup_ui(self):
        # Панель инструментов
        toolbar = tk.Frame(self.root)
        toolbar.pack()

        # Кнопка "Выбрать цвет"
        color_button = tk.Button(toolbar, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        # Кнопка "Кисть"
        eraser_button = tk.Button(toolbar, text="Кисть", command=self.brush)
        eraser_button.pack(side=tk.LEFT)

        # Кнопка "Ластик"
        eraser_button = tk.Button(toolbar, text="Ластик", command=self.use_eraser)
        eraser_button.pack(side=tk.LEFT)

        # Выпадающий список для изменения размера кисти
        brush_sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.brush_size_var = tk.IntVar(value=self.brush_size)
        brush_size_menu = tk.OptionMenu(toolbar, self.brush_size_var, *brush_sizes, command=self.change_brush_size)
        brush_size_menu.pack(side=tk.LEFT)

        # Кнопка "Очистить"
        clear_button = tk.Button(toolbar, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        # Кнопка "Сохранить"
        save_button = tk.Button(toolbar, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

    def brush(self):
        self.brush_color = self.previous_color

    def change_brush_size(self, size):
        self.brush_size = size

    def paint(self, event):
        if self.last_x and self.last_y is not None:
            x, y = event.x, event.y
            self.canvas.create_line(self.last_x, self.last_y, x, y, fill=self.brush_color, width=self.brush_size)
            self.draw.line((self.last_x, self.last_y, x, y), fill=self.brush_color, width=self.brush_size)
        self.last_x, self.last_y = event.x, event.y

    def reset(self, event):
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        pass

    def choose_color(self):
        color = colorchooser.askcolor(color=self.brush_color)[1]
        if color:
            self.brush_color = color
            self.previous_color = color  # Обновляем предыдущий цвет кисти

    def use_eraser(self):
        self.brush_color = "white"

    def save_image(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
