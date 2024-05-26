import tkinter as tk
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
        self.brush_size = 5

        self.setup_ui()

    def setup_ui(self):
        # Панель инструментов
        toolbar = tk.Frame(self.root)
        toolbar.pack()

        # Выпадающий список для изменения размера кисти
        brush_sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.brush_size_var = tk.IntVar(value=self.brush_size)
        brush_size_menu = tk.OptionMenu(toolbar, self.brush_size_var, *brush_sizes, command=self.change_brush_size)
        brush_size_menu.pack(side=tk.LEFT)

    def change_brush_size(self, size):
        self.brush_size = size


    def reset(self):
        pass

    def clear_canvas(self):
        pass

    def choose_color(self):
        pass

    def save_image(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
