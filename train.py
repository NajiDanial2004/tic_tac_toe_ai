import torch
import torch.optim as optim
import torch.nn as nn
from model.dqn import DQN
from model.replay_buffer import ReplayBuffer
from env.tic_tac_toe import TicTacToeEnv


def train_dqn_model(episodes=5000, batch_size=64):
    env = TicTacToeEnv()
    model = DQN()
    target_model = DQN()
    target_model.load_state_dict(model.state_dict())
    target_model.eval()

    buffer = ReplayBuffer()
    optimizer = optim.Adam(model.parameters(), lr=0.0005)
    criterion = nn.MSELoss()
    gamma = 0.99
    epsilon = 1.0
    update_target_every = 500

    for ep in range(episodes):
        state = env.reset()
        done = False

        while not done:
            flat_actions = [r * 3 + c for r, c in env.available_actions()]
            if torch.rand(1).item() < epsilon:
                action_idx = torch.tensor([random.choice(flat_actions)]).item()
            else:
                with torch.no_grad():
                    q_vals = model(torch.FloatTensor(state).unsqueeze(0))[0]
                q_vals_invalid = q_vals.clone()
                invalid = list(set(range(9)) - set(flat_actions))
                q_vals_invalid[invalid] = -float('inf')
                action_idx = torch.argmax(q_vals_invalid).item()

            action = divmod(action_idx, 3)
            next_state, reward, done, _ = env.step(action)
            buffer.push(state, action_idx, reward, next_state, float(done))
            state = next_state

            if len(buffer) >= batch_size:
                states, actions, rewards, next_states, dones = buffer.sample(batch_size)
                q_values = model(states)
                q_value = q_values.gather(1, actions.unsqueeze(1)).squeeze(1)
                with torch.no_grad():
                    next_q_values = target_model(next_states)
                    max_next_q = next_q_values.max(1)[0]
                    target = rewards + gamma * max_next_q * (1 - dones)
                loss = criterion(q_value, target)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

        epsilon = max(0.1, epsilon * 0.995)
        if ep % update_target_every == 0:
            target_model.load_state_dict(model.state_dict())
            print(f"Episode {ep} | Epsilon {epsilon:.3f}")

    return model

