import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class FractalVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Fraktálová vizualizace - Mandelbrot & Julia")
        self.root.resizable(False, False)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=3)

        self.center_re_var = tk.StringVar(value="-0.5")
        self.center_im_var = tk.StringVar(value="0.0")
        self.zoom_var = tk.StringVar(value="1.5")
        self.iter_var = tk.StringVar(value="50")
        self.set_type_var = tk.StringVar(value="mandelbrot")
        self.julia_re_var = tk.StringVar(value="-0.7")
        self.julia_im_var = tk.StringVar(value="0.27015")

        self.xmin = -2.0
        self.xmax = 1.0
        self.ymin = -1.0
        self.ymax = 1.0

        self.update_job = [None]

        self._create_widgets()

        self.fig = Figure()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        self.canvas_widget.bind("<Configure>", self.on_resize)
        self.canvas_widget.bind("<Button-1>", self.on_click_zoom)
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.toggle_julia_fields()
        self.root.update_idletasks()
        self.root.after(100, self.update_plot)


    def _create_widgets(self):
        control_frame = ttk.Frame(self.root, padding="10 10 10 10")
        control_frame.grid(row=0, column=0, sticky="nswe")

        ttk.Label(control_frame, text="Parameters", font='TkDefaultFont 10 bold').grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))

        ttk.Label(control_frame, text="Re(center):").grid(row=1, column=0, sticky="w", pady=2)
        ttk.Entry(control_frame, textvariable=self.center_re_var, width=15).grid(row=1, column=1, pady=2)

        ttk.Label(control_frame, text="Im(center):").grid(row=2, column=0, sticky="w", pady=2)
        ttk.Entry(control_frame, textvariable=self.center_im_var, width=15).grid(row=2, column=1, pady=2)

        ttk.Label(control_frame, text="Zoom:").grid(row=3, column=0, sticky="w", pady=2)
        ttk.Entry(control_frame, textvariable=self.zoom_var, width=15).grid(row=3, column=1, pady=2)

        ttk.Label(control_frame, text="Iterations:").grid(row=4, column=0, sticky="w", pady=2)
        ttk.Entry(control_frame, textvariable=self.iter_var, width=15).grid(row=4, column=1, pady=2)

        ttk.Label(control_frame, text="Set Type:", font='TkDefaultFont 10 bold').grid(row=5, column=0, columnspan=2, sticky="w", pady=(10, 5))
        ttk.Radiobutton(control_frame, text="Mandelbrot", variable=self.set_type_var, value="mandelbrot", command=self.toggle_julia_fields).grid(row=6, column=0, columnspan=2, sticky="w")
        ttk.Radiobutton(control_frame, text="Julia", variable=self.set_type_var, value="julia", command=self.toggle_julia_fields).grid(row=7, column=0, columnspan=2, sticky="w")

        ttk.Label(control_frame, text="Julia 'c' Parameter", font='TkDefaultFont 10 bold').grid(row=8, column=0, columnspan=2, sticky="w", pady=(10, 5))

        ttk.Label(control_frame, text="Re(c):").grid(row=9, column=0, sticky="w", pady=2)
        self.julia_re_entry = ttk.Entry(control_frame, textvariable=self.julia_re_var, width=15)
        self.julia_re_entry.grid(row=9, column=1, pady=2)

        ttk.Label(control_frame, text="Im(c):").grid(row=10, column=0, sticky="w", pady=2)
        self.julia_im_entry = ttk.Entry(control_frame, textvariable=self.julia_im_var, width=15)
        self.julia_im_entry.grid(row=10, column=1, pady=2)

        ttk.Button(control_frame, text="Draw Fractal", command=self.update_plot).grid(row=11, column=0, columnspan=2, pady=15)

        self.canvas_frame = ttk.Frame(self.root, padding="0 0 0 0")
        self.canvas_frame.grid(row=0, column=1, sticky="nsew")
        self.canvas_frame.rowconfigure(0, weight=1)
        self.canvas_frame.columnconfigure(0, weight=1)

    def mandelbrot(self, c, max_iter):
        z = 0
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = z*z + c
        return max_iter

    def julia(self, z, c, max_iter):
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = z*z + c
        return max_iter

    def compute_set(self, xmin, xmax, ymin, ymax, width, height, max_iter, set_type):
        r1 = np.linspace(xmin, xmax, width)
        r2 = np.linspace(ymin, ymax, height)

        if set_type == "mandelbrot":
            return np.array([[self.mandelbrot(complex(r, i), max_iter) for r in r1] for i in r2])
        else:
            try:
                c_julia = complex(float(self.julia_re_var.get()), float(self.julia_im_var.get()))
            except ValueError:
                print("Invalid Julia parameter value. Using default c = -0.7 + 0.27015i")
                c_julia = complex(-0.7, 0.27015)

            return np.array([[self.julia(complex(r, i), c_julia, max_iter) for r in r1] for i in r2])


    def update_plot(self):
        try:
            center_re = float(self.center_re_var.get())
            center_im = float(self.center_im_var.get())
            zoom_x = float(self.zoom_var.get())
            max_iter = int(self.iter_var.get())
        except ValueError:
            print("Invalid input value. Please enter valid numbers.")
            return

        width = self.canvas_frame.winfo_width()
        height = self.canvas_frame.winfo_height()

        if width <= 1 or height <= 1:
            self.root.after(100, self.update_plot)
            return

        aspect_ratio = height / width
        zoom_y = zoom_x * aspect_ratio

        self.xmin = center_re - zoom_x
        self.xmax = center_re + zoom_x
        self.ymin = center_im - zoom_y
        self.ymax = center_im + zoom_y

        img = self.compute_set(self.xmin, self.xmax, self.ymin, self.ymax, width, height, max_iter, self.set_type_var.get())

        self.fig.clf()

        ax = self.fig.add_subplot(111)
        ax.set_position([0, 0, 1, 1])
        ax.set_axis_off()

        title = "Mandelbrot Set" if self.set_type_var.get() == "mandelbrot" else f"Julia Set (c = {self.julia_re_var.get()} + {self.julia_im_var.get()}i)"

        ax.imshow(img, extent=(self.xmin, self.xmax, self.ymin, self.ymax), cmap="twilight_shifted", origin='lower', aspect='auto')

        ax.text(0.5, 0.95, title, transform=ax.transAxes, ha='center', color='white', fontsize=10)

        ax.text(0.02, 0.02, f"Re: [{self.xmin:.4f}, {self.xmax:.4f}]", transform=ax.transAxes, ha='left', va='bottom', color='white', fontsize=7)
        ax.text(0.98, 0.02, f"Im: [{self.ymin:.4f}, {self.ymax:.4f}]", transform=ax.transAxes, ha='right', va='bottom', color='white', fontsize=7)

        self.canvas.draw()

    def on_resize(self, event):
        if event.width > 1 and event.height > 1:
            if self.update_job[0]:
                self.root.after_cancel(self.update_job[0])

            self.update_job[0] = self.root.after(100, self.update_plot)

    def on_click_zoom(self, event):
        if self.canvas_frame.winfo_width() <= 1 or self.canvas_frame.winfo_height() <= 1:
            return

        width = self.canvas_frame.winfo_width()
        height = self.canvas_frame.winfo_height()

        click_x_norm = event.x / width
        click_y_norm = 1 - (event.y / height)

        new_re = self.xmin + click_x_norm * (self.xmax - self.xmin)
        new_im = self.ymin + click_y_norm * (self.ymax - self.ymin)

        self.center_re_var.set(f"{new_re:.6f}")
        self.center_im_var.set(f"{new_im:.6f}")

        try:
            current_zoom = float(self.zoom_var.get())
            self.zoom_var.set(f"{current_zoom * 0.5}")
        except ValueError:
             print("Invalid zoom value. Cannot zoom.")
             return

        self.update_plot()

    def on_exit(self):
        self.root.quit()
        self.root.destroy()

    def toggle_julia_fields(self):
        state = tk.NORMAL if self.set_type_var.get() == "julia" else tk.DISABLED
        self.julia_re_entry.configure(state=state)
        self.julia_im_entry.configure(state=state)
        self.update_plot()

if __name__ == "__main__":
    root = tk.Tk()
    app = FractalVisualizer(root)
    root.mainloop()