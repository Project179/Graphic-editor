import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, simpledialog
from PIL import Image, ImageTk, ImageGrab
import random
#создание холста для рисования
class GraphicsEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Графический редактор")

        self.create_menu()

        self.tool_frame = ttk.Frame(self.root)
        self.tool_frame.pack(side="top", fill="x")

        self.canvas = tk.Canvas(self.root, width=600, height=400, bg="white")
        self.canvas.pack(side="top", fill="both", expand=True)

        self.current_tool = "pen"
        self.current_color = "black"
        self.line_width = 1
        self.current_font = ("Arial", 12)

        self.color_indicator = ttk.Label(self.tool_frame, width=8, background=self.current_color)
        self.color_indicator.pack(side="left", padx=5)

        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_drawing)
        self.canvas.bind("<MouseWheel>", self.zoom)

        self.create_tool_panel()

    # меню
    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Открыть", command=self.open_file)
        file_menu.add_command(label="Сохранить", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Очистить", command=self.clear_canvas)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        menu_bar.add_cascade(label="Файл", menu=file_menu)

    # кнопки функций
    def create_tool_panel(self):
        pen_button = ttk.Button(self.tool_frame, text="Карандаш", command=lambda: self.set_tool("pen"))
        pen_button.pack(side="left")

        spray_button = ttk.Button(self.tool_frame, text="Распыление", command=lambda: self.set_tool("spray"))
        spray_button.pack(side="left")

        line_button = ttk.Button(self.tool_frame, text="Линия", command=lambda: self.set_tool("line"))
        line_button.pack(side="left")

        oval_button = ttk.Button(self.tool_frame, text="Овал", command=lambda: self.set_tool("oval"))
        oval_button.pack(side="left")

        rectangle_button = ttk.Button(self.tool_frame, text="Прямоугольник", command=lambda: self.set_tool("rectangle"))
        rectangle_button.pack(side="left")

        triangle_button = ttk.Button(self.tool_frame, text="Треугольник", command=lambda: self.set_tool("triangle"))
        triangle_button.pack(side="left")

        dashed_line_button = ttk.Button(self.tool_frame, text="Прерывистая линия", command=lambda: self.set_tool("dashed_line"))
        dashed_line_button.pack(side="left")

        eraser_button = ttk.Button(self.tool_frame, text="Ластик", command=lambda: self.set_tool("eraser"))
        eraser_button.pack(side="left")

        color_button = ttk.Button(self.tool_frame, text="Выбрать цвет", command=self.select_color)
        color_button.pack(side="left")

        fill_button = ttk.Button(self.tool_frame, text="Заливка", command=lambda: self.set_tool("fill"))
        fill_button.pack(side="left")

        width_label = ttk.Label(self.tool_frame, text="Толщина:")
        width_label.pack(side="left")
        width_entry = ttk.Entry(self.tool_frame, width=4)
        width_entry.pack(side="left")
        width_entry.insert(0, str(self.line_width))
        width_entry.bind("<Return>", self.set_line_width)

        text_button = ttk.Button(self.tool_frame, text="Текст", command=lambda: self.set_tool("text"))
        text_button.pack(side="left")

        font_label = ttk.Label(self.tool_frame, text="Шрифт:")
        font_label.pack(side="left")
        self.font_combobox = ttk.Combobox(self.tool_frame, state="readonly")
        self.font_combobox.pack(side="left")
        self.font_combobox["values"] = ("Arial", "Times New Roman", "Courier New")
        self.font_combobox.current(0)

        size_label = ttk.Label(self.tool_frame, text="Размер:")
        size_label.pack(side="left")
        self.size_entry = ttk.Entry(self.tool_frame, width=4)
        self.size_entry.pack(side="left")
        self.size_entry.insert(0, str(self.current_font[1]))
        self.size_entry.bind("<Return>", self.set_font_size)

        scale_label = ttk.Label(self.root, text="Масштаб:")
        scale_label.pack(side="bottom")
        self.scale_var = tk.DoubleVar()
        scale_entry = ttk.Scale(self.root, from_=0.1, to=2.0, length=100, variable=self.scale_var, command=self.change_scale)
        scale_entry.pack(side="bottom")
        scale_entry.set(1.0)

    def zoom(self, event):
        if event.delta > 0:
            self.scale_var.set(self.scale_var.get() + 0.1)
        elif event.delta < 0:
            self.scale_var.set(self.scale_var.get() - 0.1)

    def set_tool(self, tool):
        self.current_tool = tool
        if self.current_tool == "fill":
            self.canvas.bind("<Button-1>", self.fill_canvas)
        elif self.current_tool == "text":
            self.canvas.bind("<Button-1>", self.place_text)
        else:
            self.canvas.bind("<Button-1>", self.start_drawing)

    def set_font_size(self, event):
        size = event.widget.get()
        try:
            size = int(size)
            self.current_font = (self.current_font[0], size)
        except ValueError:
            pass

    def place_text(self, event):
        x = event.x
        y = event.y
        text = simpledialog.askstring("Ввод текста", "Введите текст:")
        if text:
            self.canvas.create_text(x, y, text=text, fill=self.current_color, font=self.current_font)

    def select_color(self):
        color = colorchooser.askcolor()
        if color:
            self.current_color = color[1]
            self.color_indicator.configure(background=self.current_color)

    def set_line_width(self, event):
        width = event.widget.get()
        try:
            self.line_width = int(width)
        except ValueError:
            pass

    def change_scale(self, value):
        self.canvas.scale("all", 0, 0, value, value)

    def start_drawing(self, event):
        self.start_x = event.x
        self.start_y = event.y

    # сами функции
    def draw(self, event):
        if self.current_tool == "pen":
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.current_color,
                                    width=self.line_width)
            self.start_x = event.x
            self.start_y = event.y
        elif self.current_tool == "spray":
            for _ in range(30):
                x = event.x + random.randint(-15, 15)
                y = event.y + random.randint(-15, 15)
                self.canvas.create_oval(x, y, x + self.line_width, y + self.line_width, fill=self.current_color,
                                        outline=self.current_color)
        elif self.current_tool == "line":
            self.canvas.delete("temp")
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.current_color,
                                    width=self.line_width, tags="temp")
        elif self.current_tool == "oval":
            self.canvas.delete("temp")
            self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, outline=self.current_color,
                                    width=self.line_width, tags="temp")
        elif self.current_tool == "rectangle":
            self.canvas.delete("temp")
            self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=self.current_color,
                                         width=self.line_width, tags="temp")
        elif self.current_tool == "triangle":
            self.canvas.delete("temp")
            x1 = (self.start_x + event.x) / 2
            y1 = self.start_y
            x2 = event.x
            y2 = event.y
            x3 = self.start_x
            y3 = event.y
            self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, outline=self.current_color, width=self.line_width,
                                       fill="", tags="temp")
        elif self.current_tool == "dashed_line":
            self.canvas.delete("temp")
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.current_color,
                                    width=self.line_width, dash=(5, 5), tags="temp")
        elif self.current_tool == "eraser":
            self.canvas.create_rectangle(event.x - self.line_width, event.y - self.line_width,
                                         event.x + self.line_width, event.y + self.line_width,
                                         fill="white", outline="white")

        elif self.current_tool == "fill":
            self.fill_canvas()

    def end_drawing(self, event):
        if self.current_tool == "line":
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.current_color,
                                    width=self.line_width)
        elif self.current_tool == "oval":
            self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, outline=self.current_color,
                                    width=self.line_width)
        elif self.current_tool == "rectangle":
            self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=self.current_color,
                                         width=self.line_width)
        elif self.current_tool == "triangle":
            x1 = (self.start_x + event.x) / 2
            y1 = self.start_y
            x2 = event.x
            y2 = event.y
            x3 = self.start_x
            y3 = event.y
            self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, outline=self.current_color, width=self.line_width,
                                       fill="")
        elif self.current_tool == "dashed_line":
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.current_color,
                                    width=self.line_width, dash=(5, 5))

    def fill_canvas(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        if not item:
            self.canvas.config(bg=self.current_color)
        else:
            item = item[0]
            self.canvas.itemconfig(item, fill=self.current_color)

    # открыть файл
    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            image = Image.open(file_path)
            self.canvas.delete("all")
            self.canvas.image = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.canvas.image)

    # сохранить файл
    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path:
            x = self.root.winfo_rootx() + self.canvas.winfo_x()
            y = self.root.winfo_rooty() + self.canvas.winfo_y()
            x1 = x + self.canvas.winfo_width()
            y1 = y + self.canvas.winfo_height()
            ImageGrab.grab().crop((x, y, x1, y1)).save(file_path)

    def clear_canvas(self):
        self.canvas.delete("all")


root = tk.Tk()
editor = GraphicsEditor(root)
root.mainloop()