# python 3.12

import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, simpledialog
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Программа для рисования")

        # Инициализация размеров холста
        self.canvas_width = 600
        self.canvas_height = 400

        # Создаем изображение и объект для рисования
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)

        # Создаем холст TKinter
        self.canvas = tk.Canvas(root, bg="white", width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        # Инициализация атрибутов кисти
        self.last_x, self.last_y = None, None
        self.brush_color = "black"
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

        # Кнопка "Изменить фон"
        bg_button = tk.Button(control_frame, text="Изменить фон", command=self.change_background)
        bg_button.pack(side=tk.LEFT)

        # Лейбл для предварительного просмотра цвета кисти
        self.color_preview = tk.Label(control_frame, text="     ", bg=self.brush_color)
        self.color_preview.pack(side=tk.LEFT, padx=5)

        # Кнопка "Кисть"
        eraser_button = tk.Button(control_frame, text="Кисть", command=self.brush)
        eraser_button.pack(side=tk.LEFT)

        # Кнопка "Ластик"
        eraser_button = tk.Button(control_frame, text="Ластик", command=self.use_eraser)
        eraser_button.pack(side=tk.LEFT)

        # Кнопка "Текст"
        text_button = tk.Button(control_frame, text="Текст", command=self.add_text)
        text_button.pack(side=tk.LEFT)

        # Кнопка "Очистить"
        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        # Кнопка "Сохранить"
        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        # Кнопка "Изменить размер холста"
        resize_button = tk.Button(control_frame, text="Изменить размер холста", command=self.resize_canvas)
        resize_button.pack(side=tk.LEFT)

        # Изменить размер кисти
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
        self.color_preview.config(bg=self.brush_color)  # Обновляем цвет предварительного просмотра

    def brush(self):
        self.brush_color = self.previous_color
        self.color_preview.config(bg=self.brush_color)  # Обновляем цвет предварительного просмотра

    # def change_brush_size(self, size):
    #     self.brush_size = size

    def reset(self, event):
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self, event=None):
        color = colorchooser.askcolor(color=self.brush_color)[1]
        if color:
            self.brush_color = color
            self.previous_color = color  # Обновляем предыдущий цвет кисти
            self.color_preview.config(bg=self.brush_color)  # Обновляем цвет предварительного просмотра

    def resize_canvas(self):
        new_width = simpledialog.askinteger("Изменить размер холста", "Введите новую ширину:\t\t\t",
                                            initialvalue=self.canvas_width)
        new_height = simpledialog.askinteger("Изменить размер холста", "Введите новую высоту:\t\t\t",
                                             initialvalue=self.canvas_height)

        if new_width and new_height:
            # Обновляем размеры холста
            self.canvas_width, self.canvas_height = new_width, new_height
            self.canvas.config(width=self.canvas_width, height=self.canvas_height)

            # Создаем новое изображение с новыми размерами
            self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
            self.draw = ImageDraw.Draw(self.image)
            self.clear_canvas()

    def add_text(self):
        text = simpledialog.askstring("Ввод текста", "Введите текст\t\t\t:")
        if text:
            self.canvas.bind("<Button-1>", lambda event: self.draw_text(event, text))

    def draw_text(self, event, text):
        x, y = event.x, event.y
        self.canvas.create_text(x, y, text=text, fill=self.brush_color, font=f"Arial {self.brush_size_scale.get()}")
        self.draw.text((x, y), text, fill=self.brush_color)
        self.canvas.unbind("<Button-1>")

    def change_background(self):
        color = colorchooser.askcolor(color=self.canvas["bg"])[1]
        if color:
            self.canvas.config(bg=color)
            self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), color)
            self.draw = ImageDraw.Draw(self.image)

    def use_eraser(self):
        self.brush_color = "white"
        self.color_preview.config(bg=self.brush_color)  # Обновляем цвет предварительного просмотра

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
