import numpy as np
import tkinter as tk

class HopfieldNetwork:
    def __init__(self, size):
        self.size = size
        self.weights = np.zeros((size, size))
        self.trained_patterns = []
    
    def train(self, pattern: np.ndarray):
        self.trained_patterns.append(pattern.copy())
        print(pattern)
        p = np.array([pattern.copy()])
        dot = np.dot(p.T,p)
        self.weights += dot
        np.fill_diagonal(self.weights, 0)
        #print(self.weights)
    
    def recall(self, pattern, use_async = False, max_iters = 100):
        if use_async:
            for index in range(self.size):
                neuron = self.weights[:,index]
                pattern[index] = np.sign(np.dot(neuron, pattern))
        else:
            last_pattern = None
            i = 0
            while not np.array_equal(last_pattern, pattern) and i < max_iters:
                last_pattern = np.copy(pattern)
                pattern = np.sign(self.weights @ pattern)
                i += 1
        return pattern

    def reset(self):
        self.weights = np.zeros((self.size, self.size))
        self.trained_patterns = []

class GUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Hopfield Network GUI")
        
        self.cell_size = 50
        self.grid_size = 5
        self.dimension = self.grid_size ** 2
        print(self.dimension / (2* np.log2(self.dimension)))
        self.pattern = np.ones((self.grid_size, self.grid_size)) * -1
        self.network = HopfieldNetwork(self.dimension)
        
        self.canvas = tk.Canvas(root, width=300, height=300)
        self.canvas.pack()
        self.cells = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x0, y0 = j * self.cell_size, i * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                self.cells[i][j] = self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black", tags=f"cell_{i}_{j}")
        
        self.canvas.bind("<Button-1>", self.toggle_cell)
        
        self.train_btn = tk.Button(root, text="Train", command=self.train)
        self.train_btn.pack()
        
        self.recall_btn = tk.Button(root, text="Recall", command=self.recall)
        self.recall_btn.pack()

        self.recall_async_btn = tk.Button(root, text="Recall Async", command=self.recall_async)
        self.recall_async_btn.pack()
        
        self.show_patterns_btn = tk.Button(root, text="Show Trained Patterns", command=self.show_trained_patterns)
        self.show_patterns_btn.pack()
        
        self.reset_btn = tk.Button(root, text="Reset everything", command=self.reset)
        self.reset_btn.pack()
    
    def toggle_cell(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            if self.pattern[row, col] == -1:
                self.pattern[row, col] = 1
                self.canvas.itemconfig(self.cells[row][col], fill="black")
            else:
                self.pattern[row, col] = -1
                self.canvas.itemconfig(self.cells[row][col], fill="white")
    
    def train(self):
        self.network.train(self.pattern.flatten())
    
    def recall(self):
        recalled_pattern = self.network.recall(self.pattern.flatten())
        print(recalled_pattern)
        recalled_pattern = recalled_pattern.reshape(self.grid_size, self.grid_size)
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                color = "black" if recalled_pattern[i, j] == 1 else "white"
                self.canvas.itemconfig(self.cells[i][j], fill=color)

    def recall_async(self):
        recalled_pattern = self.network.recall(self.pattern.flatten(), use_async=True)
        print(recalled_pattern)
        recalled_pattern = recalled_pattern.reshape(self.grid_size, self.grid_size)
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                color = "black" if recalled_pattern[i, j] == 1 else "white"
                self.canvas.itemconfig(self.cells[i][j], fill=color)
    
    def show_trained_patterns(self):
        for idx, pattern in enumerate(self.network.trained_patterns):
            top = tk.Toplevel(self.root)
            top.title("Trained Patterns")
            frame = tk.Frame(top)
            frame.pack()
            label = tk.Label(frame, text=f"Pattern {idx+1}")
            label.pack()
            canvas = tk.Canvas(frame, width=300, height=300)
            canvas.pack()
            reshaped_pattern = pattern.reshape(self.grid_size, self.grid_size)  # Oprava
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    x0, y0 = j * self.cell_size, i * self.cell_size
                    x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                    color = "black" if reshaped_pattern[i, j] == 1 else "white"
                    canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")
    
    def reset(self):
        self.pattern = np.ones((self.grid_size, self.grid_size)) * -1
        self.network.reset()
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.canvas.itemconfig(self.cells[i][j], fill="white")

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
