import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

EMPTY = 0
TREE = 1
BURNING = 2
BURNED = 3

class ForestFireSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Forest Fire Simulator")
        
        # Default parameters
        self.forest_density = 0.5
        self.ignition_probability = 0.001
        self.replacement_probability = 0.05
        self.burnout_probability = 0.2
        self.update_interval = 50
        self.running = False
        self.use_moore = False
        
        self.setup_gui()
        self.setup_plot()
        self.data = self.generate_forest_fire_data((100, 100), self.forest_density)
        self.update_plot()
        
    def setup_gui(self):
        # Control frame
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Sliders
        tk.Label(control_frame, text="Forest Density:").pack()
        self.density_slider = tk.Scale(control_frame, from_=0.0, to=1.0, resolution=0.01,
                                     orient=tk.HORIZONTAL, command=self.update_density)
        self.density_slider.set(self.forest_density)
        self.density_slider.pack()
        
        tk.Label(control_frame, text="Ignition Probability:").pack()
        self.ignition_slider = tk.Scale(control_frame, from_=0.0, to=0.01, resolution=0.001,
                                      orient=tk.HORIZONTAL, command=self.update_ignition)
        self.ignition_slider.set(self.ignition_probability)
        self.ignition_slider.pack()
        
        tk.Label(control_frame, text="Replacement Probability:").pack()
        self.replacement_slider = tk.Scale(control_frame, from_=0.0, to=0.2, resolution=0.01,
                                         orient=tk.HORIZONTAL, command=self.update_replacement)
        self.replacement_slider.set(self.replacement_probability)
        self.replacement_slider.pack()
        
        tk.Label(control_frame, text="Burnout Probability:").pack()
        self.burnout_slider = tk.Scale(control_frame, from_=0.0, to=1.0, resolution=0.01,
                                     orient=tk.HORIZONTAL, command=self.update_burnout)
        self.burnout_slider.set(self.burnout_probability)
        self.burnout_slider.pack()

        tk.Label(control_frame, text="Simulation Speed (ms):").pack()
        self.speed_slider = tk.Scale(
            control_frame, 
            from_=10, 
            to=500, 
            resolution=10,
            orient=tk.HORIZONTAL, 
            command=self.update_speed_value
        )
        self.speed_slider.set(self.update_interval)
        self.speed_slider.pack()

        self.moore_var = tk.BooleanVar()
        self.moore_checkbox = tk.Checkbutton(
            control_frame, 
            text="Use Moore Neighborhood", 
            variable=self.moore_var,
            command=self.toggle_moore
        )
        self.moore_checkbox.pack(pady=5)
        
        # Buttons
        tk.Button(control_frame, text="Reset", command=self.reset_simulation).pack(pady=5)
        self.start_stop_button = tk.Button(control_frame, text="Start", command=self.toggle_simulation)
        self.start_stop_button.pack(pady=5)

    def setup_plot(self):
        self.fig = Figure(figsize=(6, 6))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
    def generate_forest_fire_data(self, dimensions, density):
        rows, cols = dimensions
        data = np.random.rand(rows, cols) < density
        return data.astype(int)
    
    def update_plot(self):
        self.ax.clear()
        cmap = plt.cm.colors.ListedColormap(['#3b2507', 'green', 'orange', 'black'])
        self.ax.imshow(self.data, cmap=cmap, interpolation='nearest', vmin=0, vmax=3)
        self.canvas.draw()
    
    def apply_rules(self):
        data_copy = np.copy(self.data)
        for i in range(self.data.shape[0]):
            for j in range(self.data.shape[1]):
                if self.data[i, j] == TREE:
                    has_burning_neighbor = False
                    if (i > 0 and self.data[i-1, j] == BURNING) or \
                       (i < self.data.shape[0]-1 and self.data[i+1, j] == BURNING) or \
                       (j > 0 and self.data[i, j-1] == BURNING) or \
                       (j < self.data.shape[1]-1 and self.data[i, j+1] == BURNING):
                        has_burning_neighbor = True
                    if self.use_moore:
                        if (i > 0 and j > 0 and self.data[i-1, j-1] == BURNING) or \
                           (i > 0 and j < self.data.shape[1]-1 and self.data[i-1, j+1] == BURNING) or \
                           (i < self.data.shape[0]-1 and j > 0 and self.data[i+1, j-1] == BURNING) or \
                           (i < self.data.shape[0]-1 and j < self.data.shape[1]-1 and self.data[i+1, j+1] == BURNING):
                            has_burning_neighbor = True
                    if has_burning_neighbor or np.random.rand() < self.ignition_probability:
                        data_copy[i, j] = BURNING
                elif self.data[i, j] == EMPTY or self.data[i, j] == BURNED:
                    if np.random.rand() < self.replacement_probability:
                        data_copy[i, j] = TREE
                    else:
                        data_copy[i, j] = EMPTY
                elif self.data[i, j] == BURNING and np.random.rand() < self.burnout_probability:
                    data_copy[i, j] = BURNED
        self.data = data_copy
    
    def update(self):
        if self.running:
            self.apply_rules()
            self.update_plot()
            self.root.after(self.update_interval, self.update)
    
    def toggle_simulation(self):
        self.running = not self.running
        if self.running:
            self.start_stop_button.config(text="Stop")
            self.update()
        else:
            self.start_stop_button.config(text="Start")
    
    def toggle_moore(self):
        self.use_moore = self.moore_var.get()
    
    def reset_simulation(self):
        self.data = self.generate_forest_fire_data((100, 100), self.forest_density)
        self.update_plot()
    
    def update_density(self, value):
        self.forest_density = float(value)
    
    def update_ignition(self, value):
        self.ignition_probability = float(value)
    
    def update_replacement(self, value):
        self.replacement_probability = float(value)
    
    def update_burnout(self, value):
        self.burnout_probability = float(value)
    
    def update_speed_value(self, value):
        self.update_interval = int(value)

def main():
    root = tk.Tk()
    app = ForestFireSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()