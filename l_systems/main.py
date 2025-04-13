from io import StringIO
import math
import tkinter as tk
from tkinter import ttk
import turtle

SAVED_AXIOMS = [
    ("F+F+F+F", {"F":"F+F-F-FF+F+F-F"}, 90),
    ("F++F++F", {"F":"F+F--F+F"}, 60),
    ("F", {"F":"F[+F]F[-F]F"}, math.degrees(math.pi/7)),
    ("F", {"F":"FF+[+F-F-F]-[-F+F+F]"}, math.degrees(math.pi/8))
]

def compute_system(axiom, rules: dict, iterations):
    builder = StringIO()
    for _ in range(iterations):
        for char in axiom:
            if char in rules:
                builder.write(rules[char])
            else:
                builder.write(char)
        axiom = builder.getvalue()
        builder.truncate(0)
        builder.seek(0)
    return axiom

def draw_l_system(result, angle, start_x, start_y, canvas, line_width=1, line_length=5):
    screen = turtle.TurtleScreen(canvas)
    screen.tracer(0)
    t = turtle.RawTurtle(screen)
    t.hideturtle()
    t.speed(0)
    t.pensize(line_width)
    t.penup()
    t.setpos(start_x, start_y)
    t.pendown()
    stack = []
    
    for i, char in enumerate(result):
        if char == 'F':
            t.forward(line_length)
        elif char =='b':
            t.penup()
            t.forward(line_length)
            t.pendown()
        elif char == '+':
            t.right(angle)
        elif char == '-':
            t.left(angle)
        elif char == '[':
            stack.append((t.position(), t.heading()))
        elif char == ']':
            pos, heading = stack.pop()
            t.penup()
            t.setposition(pos)
            t.setheading(heading)
            t.pendown()
        i += 1
        if i % 10_000 == 0:
            screen.update()
            print(f"Drawing {i}/{len(result)}")
    
    screen.update()
    print("Drawing complete")

class LSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("L-System Visualizer")
        
        # Configure root grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create main frame
        main_frame = ttk.Frame(root)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Create canvas with scrollbars
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.grid(row=0, column=0, columnspan=4, sticky="nsew")
        
        self.canvas = tk.Canvas(canvas_frame, width=600, height=400, bg='white')
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient="horizontal", command=self.canvas.xview)
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        
        self.canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        
        # Grid layout for scrollable canvas
        self.canvas.grid(row=0, column=0, sticky="nsew")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)
        
        # Bind resize event
        self.root.bind('<Configure>', self.on_resize)
        
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=1, column=0, columnspan=4)
        
        # Starting position inputs
        tk.Label(controls_frame, text="Start X:").grid(row=0, column=0)
        self.start_x = tk.Entry(controls_frame)
        self.start_x.grid(row=0, column=1)
        self.start_x.insert(0, "0")
        
        tk.Label(controls_frame, text="Start Y:").grid(row=1, column=0)
        self.start_y = tk.Entry(controls_frame)
        self.start_y.grid(row=1, column=1)
        self.start_y.insert(0, "0")
        
        tk.Label(controls_frame, text="Iterations:").grid(row=2, column=0)
        self.iterations = tk.Entry(controls_frame)
        self.iterations.grid(row=2, column=1)
        self.iterations.insert(0, "3")

        tk.Label(controls_frame, text="Line Width:").grid(row=8, column=0)
        self.line_width = ttk.Scale(controls_frame, from_=1, to=10, orient="horizontal")
        self.line_width.set(1)
        self.line_width.grid(row=8, column=1)
        
        tk.Label(controls_frame, text="Line Length:").grid(row=9, column=0)
        self.line_length = ttk.Scale(controls_frame, from_=1, to=50, orient="horizontal")
        self.line_length.set(5)
        self.line_length.grid(row=9, column=1)
        
        for i, (axiom, rules, angle) in enumerate(SAVED_AXIOMS):
            btn = tk.Button(controls_frame, text=f"Preset {i+1}", 
                          command=lambda a=axiom, r=rules, ang=angle: self.draw_preset(a, r, ang))
            btn.grid(row=3, column=i)
        
        tk.Label(controls_frame, text="Custom Axiom:").grid(row=4, column=0)
        self.custom_axiom = tk.Entry(controls_frame)
        self.custom_axiom.grid(row=4, column=1)
        
        tk.Label(controls_frame, text="Custom Rules {\"F\":\"F+F\"} :").grid(row=5, column=0)
        self.custom_rules = tk.Entry(controls_frame)
        self.custom_rules.grid(row=5, column=1)
        
        tk.Label(controls_frame, text="Custom Angle:").grid(row=6, column=0)
        self.custom_angle = tk.Entry(controls_frame)
        self.custom_angle.grid(row=6, column=1)
        
        tk.Button(controls_frame, text="Draw Custom", command=self.draw_custom).grid(row=7, column=0)
        tk.Button(controls_frame, text="Clear", command=self.clear_canvas).grid(row=7, column=1)

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_resize(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def clear_canvas(self):
        self.canvas.delete("all")
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def draw_preset(self, axiom, rules, angle):
        self.clear_canvas()
        result = compute_system(axiom, rules, int(self.iterations.get()))
        draw_l_system(
            result, 
            angle, 
            float(self.start_x.get()), 
            float(self.start_y.get()), 
            self.canvas,
            line_width=self.line_width.get(),
            line_length=self.line_length.get()
        )
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def draw_custom(self):
        try:
            self.clear_canvas()
            axiom = self.custom_axiom.get()
            rules = eval(self.custom_rules.get())
            angle = float(self.custom_angle.get())
            result = compute_system(axiom, rules, int(self.iterations.get()))
            draw_l_system(
                result, 
                angle, 
                float(self.start_x.get()), 
                float(self.start_y.get()), 
                self.canvas,
                line_width=self.line_width.get(),
                line_length=self.line_length.get()
            )
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = LSystemGUI(root)
    root.mainloop()

