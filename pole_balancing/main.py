import gymnasium as gym
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from collections import deque

CONFIG = {
    'gamma': 0.99,
    'epsilon_start': 1.0,
    'epsilon_min': 0.01,
    'epsilon_decay': 0.995,
    'learning_rate': 0.001,
    'batch_size': 64,
    'memory_capacity': 10000,
    'episodes': 500
}

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Approximator(nn.Module):
    def __init__(self, input_dim, output_dim):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim + output_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, 1)
        )

    def forward(self, state_vec, action_vec):
        one_hot = torch.nn.functional.one_hot(action_vec, num_classes=2).float().squeeze(1)
        combined = torch.cat((state_vec, one_hot), dim=1)
        return self.model(combined).squeeze(1)

env = gym.make("CartPole-v1", render_mode="human")
obs_dim = env.observation_space.shape[0]
act_dim = env.action_space.n

policy = Approximator(obs_dim, act_dim).to(device)
opt = optim.Adam(policy.parameters(), lr=CONFIG['learning_rate'])
experience = deque(maxlen=CONFIG['memory_capacity'])
epsilon = CONFIG['epsilon_start']

def decide_action(obs, eps):
    if np.random.rand() < eps:
        return random.randrange(act_dim)
    obs_tensor = torch.tensor(obs, dtype=torch.float32).unsqueeze(0).to(device)
    scores = [policy(obs_tensor, torch.tensor([[i]]).to(device)).item() for i in range(act_dim)]
    return int(np.argmax(scores))

def train_on_batch():
    if len(experience) < CONFIG['batch_size']:
        return
    samples = random.sample(experience, CONFIG['batch_size'])
    obs_list, act_list, rew_list, next_obs_list, terminal_flags = zip(*samples)

    obs_batch = torch.tensor(obs_list, dtype=torch.float32).to(device)
    act_batch = torch.tensor(act_list, dtype=torch.long).unsqueeze(1).to(device)
    rew_batch = torch.tensor(rew_list, dtype=torch.float32).to(device)
    next_obs_batch = torch.tensor(next_obs_list, dtype=torch.float32).to(device)
    done_mask = torch.tensor(terminal_flags, dtype=torch.bool).to(device)

    with torch.no_grad():
        q_targets = torch.stack([
            policy(next_obs_batch, torch.full((CONFIG['batch_size'], 1), a, dtype=torch.long).to(device))
            for a in range(act_dim)
        ], dim=1)
        max_q_vals = q_targets.max(1)[0]
        expected = rew_batch + CONFIG['gamma'] * max_q_vals * (~done_mask)

    current_q_vals = policy(obs_batch, act_batch)
    loss = nn.MSELoss()(current_q_vals, expected)

    opt.zero_grad()
    loss.backward()
    opt.step()

for ep in range(CONFIG['episodes']):
    obs, _ = env.reset()
    episode_reward = 0
    is_done = False

    while not is_done:
        chosen_action = decide_action(obs, epsilon)
        next_obs, reward, terminated, truncated, _ = env.step(chosen_action)
        is_done = terminated or truncated

        experience.append((obs, chosen_action, reward, next_obs, is_done))
        obs = next_obs
        episode_reward += reward

        train_on_batch()

    epsilon = max(CONFIG['epsilon_min'], epsilon * CONFIG['epsilon_decay'])
    print(f"[Episode {ep}] Reward: {episode_reward:.1f} | Epsilon: {epsilon:.3f}")

env.close()
