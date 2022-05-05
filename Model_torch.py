import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os


class DNN(nn.Module):
    def __init__(self, state_size, hidden_size, action_size):
        super().__init__()
        self.linear1 = nn.Linear(state_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, action_size)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name):
        model_folder_path = './Model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)
        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


class Trainer:
    def __init__(self, dnn):
        self.lr = 1e-3
        self.gamma = 0.9
        self.alpha = 1
        self.dnn = dnn
        self.optimizer = optim.Adam(self.dnn.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.int)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        predict_q = self.dnn(state)  # predict
        target_q = predict_q.clone()

        for index in range(len(done)):
            if not done[index]:
                q = reward[index] + self.gamma * torch.max(self.dnn(next_state[index]))
            else:
                q = reward[index]
            q_old = target_q[index][action[index].item()]
            target_q[index][action[index]] = q_old + self.alpha * (q - q_old)

        self.optimizer.zero_grad()
        loss = self.criterion(target_q, predict_q)
        loss.backward()
        self.optimizer.step()
