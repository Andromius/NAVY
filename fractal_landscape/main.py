import tkinter as tk
from tkinter import Frame, Button, Scale, HORIZONTAL, Label
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

class FractalLandscape:
    def __init__(self, master):
        self.master = master
        master.title("3D Fractal Landscape Generator")
        master.protocol("WM_DELETE_WINDOW", self.on_exit)
        
        # Configuration
        self.fig_width = 8
        self.fig_height = 6
        self.dpi = 100
        
        # Parameters
        self.roughness = 0.5
        self.iterations = 6
        self.elevation_levels = 5
        
        # View angles
        self.elev = 30
        self.azim = 45
        
        # Store the height map
        self.height_map = None
        self.grid_width = 0
        self.grid_height = 0
        
        self.colormap = cm.terrain
        
        # Create the UI and Matplotlib figure
        self.create_widgets()
        
        # Initial generation
        self.generate_landscape()
    
    def create_widgets(self):
        # Main content frame
        content_frame = Frame(self.master)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left frame for controls
        controls_frame = Frame(content_frame)
        controls_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Parameter controls
        Label(controls_frame, text="Parameters", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        # Roughness slider
        roughness_label = Label(controls_frame, text="Roughness:")
        roughness_label.pack(anchor="w", padx=5)
        self.roughness_slider = Scale(controls_frame, from_=0.1, to=1.0, 
                                     resolution=0.1, orient=HORIZONTAL, 
                                     command=self.update_roughness,
                                     length=150)
        self.roughness_slider.set(self.roughness)
        self.roughness_slider.pack(padx=5, pady=(0, 10))
        
        # Iterations slider
        iterations_label = Label(controls_frame, text="Detail Level:")
        iterations_label.pack(anchor="w", padx=5)
        self.iterations_slider = Scale(controls_frame, from_=0, to=8, 
                                      resolution=1, orient=HORIZONTAL, 
                                      command=self.update_iterations,
                                      length=150)
        self.iterations_slider.set(self.iterations)
        self.iterations_slider.pack(padx=5, pady=(0, 10))
        
        # Generate button
        self.generate_button = Button(controls_frame, text="Generate New Landscape", 
                                     command=self.generate_landscape)
        self.generate_button.pack(padx=5, pady=10)
        
        # Right frame for matplotlib plot
        plot_frame = Frame(content_frame)
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create matplotlib figure and canvas
        self.fig = plt.figure(figsize=(self.fig_width, self.fig_height), dpi=self.dpi)
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Status label
        self.status_label = Label(self.master, text="Ready")
        self.status_label.pack(side=tk.BOTTOM, pady=5)
    
    def on_exit(self):
        self.master.quit()
        self.master.destroy()
    
    def update_roughness(self, value):
        self.roughness = float(value)
    
    def update_iterations(self, value):
        self.iterations = int(value)
    
    def update_colormap(self):
        self.colormap = self.colormap_var.get()
        if self.height_map is not None:
            self.redraw_landscape()
    
    def update_view_angle(self, _=None):
        self.elev = self.elev_slider.get()
        self.azim = self.azim_slider.get()
        if self.height_map is not None:
            self.redraw_landscape()

    def generate_landscape(self):
        """Generate a new fractal landscape using spatial subdivision."""
        self.status_label.config(text="Generating landscape...")
        self.master.update()
        
        # Create grid based on iterations (2^n + 1)
        size = 2 ** self.iterations
        self.grid_width = size + 1
        self.grid_height = self.grid_width
        
        # Create height map using NumPy
        self.height_map = np.zeros((self.grid_height, self.grid_width))
        
        # Perform spatial subdivision algorithm
        self.spatial_subdivision()
        
        # Draw the 3D landscape
        self.redraw_landscape()
        self.status_label.config(text="Landscape generated")
    
    def spatial_subdivision(self):
        """
        Implement spatial subdivision algorithm for terrain generation:
        1. Start with a square
        2. Split into 2x2 grid
        3. Perturb heights at vertices
        4. Recursively subdivide each subsquare
        """

        size = self.grid_width - 1  # Grid size (2^n)
        
        corner_height = 0
        self.height_map[0, 0] = corner_height
        self.height_map[0, size] = corner_height
        self.height_map[size, 0] = corner_height
        self.height_map[size, size] = corner_height
        
        self._subdivide(0, 0, size, self.roughness)
        self.height_map[self.height_map < 0] = 0
    
    def _subdivide(self, x, y, size, roughness):
        """
        Recursively subdivide a square and perturb the new vertices.
        
        Args:
            x, y: Top-left corner coordinates of the square
            size: Size of the square
            roughness: Current roughness factor
        """
        # Base case: smallest subdivision reached (1x1 grid)
        if size <= 1:
            return
        
        half_size = size // 2
        
        # Calculate coordinates of the center point
        mid_x = x + half_size
        mid_y = y + half_size
        
        # Calculate midpoints of the sides
        mid_top = (x + half_size, y)
        mid_right = (x + size, y + half_size)
        mid_bottom = (x + half_size, y + size)
        mid_left = (x, y + half_size)
        
        # If the center point hasn't been set, calculate it as average of corners + perturbation
        if self.height_map[mid_y, mid_x] == 0:
            # Average the four corners
            avg = (self.height_map[y, x] + 
                   self.height_map[y, x+size] + 
                   self.height_map[y+size, x] + 
                   self.height_map[y+size, x+size]) / 4.0
            
            # Add random displacement
            perturbation = random.uniform(-roughness, roughness)
            self.height_map[mid_y, mid_x] = avg + perturbation
        
        # If midpoints haven't been set, calculate them as average of endpoints + perturbation
        # Top midpoint
        if self.height_map[mid_top[1], mid_top[0]] == 0:
            avg = (self.height_map[y, x] + self.height_map[y, x+size]) / 2.0
            perturbation = random.uniform(-roughness, roughness)
            self.height_map[mid_top[1], mid_top[0]] = avg + perturbation
        
        # Right midpoint
        if self.height_map[mid_right[1], mid_right[0]] == 0:
            avg = (self.height_map[y, x+size] + self.height_map[y+size, x+size]) / 2.0
            perturbation = random.uniform(-roughness, roughness)
            self.height_map[mid_right[1], mid_right[0]] = avg + perturbation
        
        # Bottom midpoint
        if self.height_map[mid_bottom[1], mid_bottom[0]] == 0:
            avg = (self.height_map[y+size, x] + self.height_map[y+size, x+size]) / 2.0
            perturbation = random.uniform(-roughness, roughness)
            self.height_map[mid_bottom[1], mid_bottom[0]] = avg + perturbation
        
        # Left midpoint
        if self.height_map[mid_left[1], mid_left[0]] == 0:
            avg = (self.height_map[y, x] + self.height_map[y+size, x]) / 2.0
            perturbation = random.uniform(-roughness, roughness)
            self.height_map[mid_left[1], mid_left[0]] = avg + perturbation
        
        # Recursively subdivide the four new squares with reduced roughness
        new_roughness = roughness * 0.5
        
        self._subdivide(x, y, half_size, new_roughness)                   # Top-left
        self._subdivide(x + half_size, y, half_size, new_roughness)       # Top-right
        self._subdivide(x, y + half_size, half_size, new_roughness)       # Bottom-left
        self._subdivide(x + half_size, y + half_size, half_size, new_roughness)  # Bottom-right
    
    def redraw_landscape(self):
        """Draw the landscape using matplotlib's 3D plotting."""
        if self.height_map is None:
            return
        
        # Clear previous plot
        self.ax.clear()
        
        # Create X and Y coordinate matrices
        x = np.linspace(0, 1, self.grid_width)
        y = np.linspace(0, 1, self.grid_height)
        X, Y = np.meshgrid(x, y)
        
        # Plot surface with the selected colormap
        surf = self.ax.plot_surface(X, Y, self.height_map, 
                                   cmap=self.colormap,
                                   linewidth=0, antialiased=True)
        
        # Set labels and title
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Height')
        self.ax.set_title('3D Fractal Landscape')
        
        # Set viewing angle
        self.ax.view_init(elev=self.elev, azim=self.azim)
        
        # Set z axis limits to be consistent between generations
        self.ax.set_zlim(0, 1)
        
        # Refresh canvas
        self.canvas.draw()
        self.canvas.get_tk_widget().update_idletasks()
        self.canvas.get_tk_widget().update()

if __name__ == "__main__":
    root = tk.Tk()
    app = FractalLandscape(root)
    root.geometry("1000x700")  # Larger window to accommodate both controls and plot
    root.mainloop()