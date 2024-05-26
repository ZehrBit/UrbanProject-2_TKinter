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
        self.canvas.bind("<Button-3>", self.pick_color)  # Привязка события для пипетки

        # Привязка горячих клавиш
        self.root.bind('<Control-s>', self.save_image)
        self.root.bind('<Control-c>', self.choose_color)

    def setup_ui(self):
        # Панель инструментов
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        # Кнопка "Выбрать цвет"
        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        # Кнопка "Кисть"
        eraser_button = tk.Button(control_frame, text="Кисть", command=self.brush)
        eraser_button.pack(side=tk.LEFT)

        # Кнопка "Ластик"
        eraser_button = tk.Button(control_frame, text="Ластик", command=self.use_eraser)
        eraser_button.pack(side=tk.LEFT)

        # Кнопка "Очистить"
        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        # Кнопка "Сохранить"
        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        self.brush_size_scale = tk.Scale(control_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        self.brush_size_scale.pack(side=tk.LEFT)

    def paint(self, event):
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size_scale.get(), fill=self.brush_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.brush_color,
                           width=self.brush_size_scale.get())

        self.last_x = event.x
        self.last_y = event.y

    def pick_color(self, event):
        x, y = event.x, event.y
        # Получаем цвет пикселя в позиции (x, y)
        color = self.image.getpixel((x, y))
        # Преобразуем цвет в формат HEX
        self.brush_color = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'
        self.previous_color = self.brush_color  # Обновляем предыдущий цвет кисти

    def brush(self):
        self.brush_color = self.previous_color

    def change_brush_size(self, size):
        self.brush_size = size

    def reset(self, event):
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self, event=None):
        color = colorchooser.askcolor(color=self.brush_color)[1]
        if color:
            self.brush_color = color
            self.previous_color = color  # Обновляем предыдущий цвет кисти

    def use_eraser(self):
        self.brush_color = "white"

    def save_image(self, event=None):
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")


if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
