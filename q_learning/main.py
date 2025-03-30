import numpy as np
import tkinter as tk
import random
import time

# Parametry prostředí
size = 10  # Velikost hrací plochy (size x size)
cheese_pos = (4, 4)  # Pozice sýra
obstacles = [(2, 2), (1, 3), (3, 1)]  # Překážky

actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Nahoru, dolů, vlevo, vpravo
q_table = np.zeros((size, size, len(actions)))  # Q-tabule

# Parametry učení
alpha = 0.1  # Learning rate
gamma = 0.9  # Discount factor
epsilon = 0.9  # Prozkoumávání

class QLearningVisualizer:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.canvas = tk.Canvas(root, width=1000, height=1000)
        self.canvas.pack(side='left')
        self.cell_size = 100
        self.episodes = 100
        self.draw_grid()
        self.draw_elements()
        self.agent = self.canvas.create_oval(10, 10, 90, 90, fill='blue')
        self.movement_reward = -1
        self.obstacle_reward = -10
        self.cheese_reward = 100
        
        self.demo_running = False

        self.train_button = tk.Button(root, text="Spustit trénování", command=self.train_agent)
        self.train_button.pack()
        
        self.demo_button = tk.Button(root, text="Spustit demonstraci", command=self.demo_optimal_path)
        self.demo_button.pack()

        self.qtable_button = tk.Button(root, text="Zobrazit Q-Table", command=self.show_qtable)
        self.qtable_button.pack()

        self.env_button = tk.Button(root, text="Zobrazit matici prostředí", command=self.show_environment)
        self.env_button.pack()

        self.start_pos = (0, 0)  # Initial position variable
        
        # Add edit mode buttons and state variables
        self.edit_frame = tk.Frame(root)
        self.edit_frame.pack()
        
        self.edit_mode = "none"  # Current edit mode
        self.obstacle_button = tk.Button(self.edit_frame, text="Překážky", command=lambda: self.set_edit_mode("obstacles"))
        self.cheese_button = tk.Button(self.edit_frame, text="Sýr", command=lambda: self.set_edit_mode("cheese"))
        self.start_button = tk.Button(self.edit_frame, text="Start", command=lambda: self.set_edit_mode("start"))
        
        self.obstacle_button.pack(side=tk.LEFT)
        self.cheese_button.pack(side=tk.LEFT)
        self.start_button.pack(side=tk.LEFT)

        # Add parameters frame
        self.params_frame = tk.LabelFrame(root, text="Learning Parameters", padx=5, pady=5)
        self.params_frame.pack(pady=10)

        # Alpha slider
        tk.Label(self.params_frame, text="Alpha (learning rate):").grid(row=0, column=0, sticky='w')
        self.alpha_var = tk.DoubleVar(value=alpha)
        self.alpha_slider = tk.Scale(self.params_frame, from_=0.0, to=1.0, resolution=0.01,
                                    orient=tk.HORIZONTAL, length=200, variable=self.alpha_var)
        self.alpha_slider.grid(row=0, column=1)

        # Gamma slider
        tk.Label(self.params_frame, text="Gamma (discount):").grid(row=1, column=0, sticky='w')
        self.gamma_var = tk.DoubleVar(value=gamma)
        self.gamma_slider = tk.Scale(self.params_frame, from_=0.0, to=1.0, resolution=0.01,
                                    orient=tk.HORIZONTAL, length=200, variable=self.gamma_var)
        self.gamma_slider.grid(row=1, column=1)

        # Epsilon slider
        tk.Label(self.params_frame, text="Epsilon (exploration):").grid(row=2, column=0, sticky='w')
        self.epsilon_var = tk.DoubleVar(value=epsilon)
        self.epsilon_slider = tk.Scale(self.params_frame, from_=0.0, to=1.0, resolution=0.01,
                                    orient=tk.HORIZONTAL, length=200, variable=self.epsilon_var)
        self.epsilon_slider.grid(row=2, column=1)

        tk.Label(self.params_frame, text="Number of episodes:").grid(row=3, column=0, sticky='w')
        self.episodes_var = tk.IntVar(value=100)
        self.episodes_entry = tk.Entry(self.params_frame, textvariable=self.episodes_var, width=10)
        self.episodes_entry.grid(row=3, column=1, sticky='w', padx=5)

        self.reset_button = tk.Button(self.params_frame, text="Reset", command=self.reset_training)
        self.reset_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Add stats frame
        self.stats_frame = tk.LabelFrame(root, text="Training Statistics", padx=5, pady=5)
        self.stats_frame.pack(pady=10)
        
        # Add text widget for iterations
        self.stats_text = tk.Text(self.stats_frame, height=10, width=40)
        self.stats_text.pack()

        self.canvas.bind("<Button-1>", self.canvas_clicked)

    def redraw_board(self):
        self.canvas.delete("all")
        self.draw_grid()
        self.draw_elements()
        self.agent = self.canvas.create_oval(10, 10, 90, 90, fill='blue')
        self.update_agent_position(self.start_pos)

    def canvas_clicked(self, event):
        global cheese_pos
        i = event.y // self.cell_size
        j = event.x // self.cell_size
        
        if i >= size or j >= size:
            return
            
        position = (i, j)
        
        if self.edit_mode == "obstacles":
            if position in obstacles:
                obstacles.remove(position)
            else:
                if position != cheese_pos and position != self.start_pos:
                    obstacles.append(position)
        
        elif self.edit_mode == "cheese":
            if position != self.start_pos and position not in obstacles:
                cheese_pos = position
        
        elif self.edit_mode == "start":
            if position != cheese_pos and position not in obstacles:
                self.start_pos = position
        
        self.redraw_board()

    def set_edit_mode(self, mode):
        self.edit_mode = mode
        for btn in [self.obstacle_button, self.cheese_button, self.start_button]:
            btn.configure(bg='#f0f0f0')
        
        if mode == "obstacles":
            self.obstacle_button.configure(bg='lightblue')
        elif mode == "cheese":
            self.cheese_button.configure(bg='lightblue')
        elif mode == "start":
            self.start_button.configure(bg='lightblue')
    
    def draw_grid(self):
        for i in range(size + 1):
            self.canvas.create_line(i * self.cell_size, 0, i * self.cell_size, size * self.cell_size)
            self.canvas.create_line(0, i * self.cell_size, size * self.cell_size, i * self.cell_size)
    
    def draw_elements(self):
        for (i, j) in obstacles:
            self.canvas.create_rectangle(j * self.cell_size, i * self.cell_size, (j + 1) * self.cell_size, (i + 1) * self.cell_size, fill='red')
        self.canvas.create_rectangle(cheese_pos[1] * self.cell_size, cheese_pos[0] * self.cell_size, (cheese_pos[1] + 1) * self.cell_size, (cheese_pos[0] + 1) * self.cell_size, fill='yellow')
        
    def reset_training(self):
        q_table.fill(0)
        self.demo_running = False
        self.alpha_var.set(0.1)
        self.gamma_var.set(0.9)
        self.epsilon_var.set(0.9)
        self.episodes_var.set(100)
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, "Training reset. Ready for new training.\n")
        
        self.alpha_slider.configure(state='normal')
        self.gamma_slider.configure(state='normal')
        self.epsilon_slider.configure(state='normal')
        self.episodes_entry.configure(state='normal')
        
        self.update_agent_position(self.start_pos)
        self.root.update()


    def train_agent(self):
        try:
            self.episodes = self.episodes_var.get()
            if self.episodes <= 0:
                raise ValueError
        except tk.TclError:
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(tk.END, "Error: Invalid number setting 100 episodes")
            self.episodes = 100
            self.episodes_var.set(self.episodes)

        current_alpha = self.alpha_var.get()
        current_gamma = self.gamma_var.get()
        starting_epsilon = self.epsilon_var.get()

        total_iterations = 0

        current_epsilon = starting_epsilon

        self.stats_text.insert(tk.END, "Training progress:\n")

        self.alpha_slider.configure(state='disabled')
        self.gamma_slider.configure(state='disabled')
        self.epsilon_slider.configure(state='disabled')

        for episode in range(self.episodes):
            state = self.start_pos
            if episode % 5 == 0 and episode != 0:
                current_epsilon *= 0.95
            self.epsilon_var.set(current_epsilon)
            episode_iterations = 0
            while state != cheese_pos:
                self.update_agent_position(state)
                self.root.update()

                if random.uniform(0, 1) < current_epsilon:
                    action = random.randint(0, len(actions) - 1)
                else:
                    action = np.argmax(q_table[state[0], state[1]])
                
                new_state = (state[0] + actions[action][0], state[1] + actions[action][1])
                if new_state[0] < 0 or new_state[0] >= size or new_state[1] < 0 or new_state[1] >= size or new_state in obstacles:
                    reward = self.obstacle_reward
                    new_state = state
                elif new_state == cheese_pos:
                    reward = self.cheese_reward
                else:
                    reward = self.movement_reward
                
                best_future_q = np.max(q_table[new_state[0], new_state[1]])
                q_table[state[0], state[1], action] += current_alpha * (
                    reward + current_gamma * best_future_q - q_table[state[0], state[1], action]
                )
                state = new_state
                episode_iterations += 1
                total_iterations += 1
            self.stats_text.insert(tk.END, f"Episode {episode + 1}: {episode_iterations} steps\n")
            self.stats_text.see(tk.END) 
        self.epsilon_var.set(current_epsilon)
        self.alpha_slider.configure(state='normal')
        self.gamma_slider.configure(state='normal')
        self.epsilon_slider.configure(state='normal')
        
        self.stats_text.insert(tk.END, f"\nTraining completed.\nTotal iterations: {total_iterations}\n")
        self.stats_text.see(tk.END)
    
    def demo_optimal_path(self):
        self.stats_text.insert(tk.END, "Visualizing learned path")
        self.demo_running = True
        state = self.start_pos
        self.update_agent_position(state)
        self.root.update()
        time.sleep(0.5)
        while state != cheese_pos and self.demo_running:
            action = np.argmax(q_table[state[0], state[1]])
            state = (state[0] + actions[action][0], state[1] + actions[action][1])
            self.update_agent_position(state)
            self.root.update()
            time.sleep(0.5)
        self.demo_running = False
    
    def update_agent_position(self, state):
        x, y = state
        self.canvas.coords(self.agent, y * self.cell_size + 10, x * self.cell_size + 10, y * self.cell_size + 90, x * self.cell_size + 90)

    def show_qtable(self):
        qtable_window = tk.Toplevel(self.root)
        qtable_window.title("Q-Table Visualization")
        
        main_frame = tk.Frame(qtable_window)
        main_frame.pack(fill=tk.BOTH, expand=1)
        
        canvas = tk.Canvas(main_frame)
        v_scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        h_scrollbar = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=canvas.xview)
        
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        content_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=content_frame, anchor='nw')
        
        action_labels = ['↑', '↓', '←', '→']
        for j, label in enumerate(action_labels):
            tk.Label(content_frame, text=label, width=10).grid(row=0, column=j+1)
        
        for i in range(size):
            for j in range(size):
                tk.Label(content_frame, text=f"({i},{j})").grid(row=i*size + j + 1, column=0)
                
                for action in range(len(actions)):
                    value = q_table[i, j, action]
                    tk.Label(content_frame, text=f"{value:.2f}", width=10).grid(
                        row=i*size + j + 1, column=action + 1)
        
        content_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        
        qtable_window.geometry("500x400")
    
    def show_environment(self):
        env_window = tk.Toplevel(self.root)
        env_window.title("Environment Matrix - Rewards")
        reward_matrix = np.ones((size, size)) * self.movement_reward
        
        reward_matrix[cheese_pos] = self.cheese_reward
        for obs in obstacles:
            reward_matrix[obs] = self.obstacle_reward
        
        for i in range(size):
            for j in range(size):
                value = reward_matrix[i, j]
                if value == self.cheese_reward:
                    bg_color = 'yellow'
                elif value == self.obstacle_reward:
                    bg_color = 'red'
                else:
                    bg_color = 'white'
                    
                tk.Label(env_window, 
                        text=f"{int(value)}", 
                        width=5,
                        font=('TkDefaultFont', 12),
                        bg=bg_color).grid(row=i, column=j, padx=5, pady=5)

root = tk.Tk()
root.title("Q-Learning: Učení agenta")
app = QLearningVisualizer(root)
root.mainloop()
