import torch
from Model_torch import DNN, Trainer
import numpy as np
import random
from utils import game2state
import tensorflow as tf
from collections import deque

max_memory = 10000
batch_size = 1024


class Agent:

    def __init__(self, state_size):
        self.epochs = 0
        self.epsilon = 0
        self.gamma = 0.9  # discount rates
        self.alpha = 0.1
        self.state_size = state_size
        # self.memory = np.zeros((max_memory, self.state_size * 2 + 2))
        self. memory = deque(maxlen=max_memory)
        # self.memory_counter = 0
        # self.learn_step_counter = 0
        # self.replace_target_iter = 50
        self.dnn = DNN(state_size=state_size, hidden_size=64*3, action_size=3)
        self.trainer = Trainer(self.dnn)

    @staticmethod
    def get_state(game):
        state = game2state(game)
        return np.array(state, dtype=int)

    def store_in_memory(self, state, action, reward, next_state, done):
        # transition = np.hstack((state, action, reward, next_state))
        # index = self.memory_counter % max_memory
        # self.memory[index, :] = transition
        # self.memory_counter += 1

        self.memory.append(
            (state, action, reward, next_state, done)
        )

    def train_long_memory(self):
        if len(self.memory) > batch_size:
            sample_memory = random.sample(self.memory, batch_size)
        else:
            sample_memory = self.memory

        states, actions, rewards, next_states, dones = zip(*sample_memory)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

        # if self.learn_step_counter > self.replace_target_iter == 0:
        #     self.learn_step_counter = 0
        #     self.dnn.target_replace_op()
        #
        # if self.memory_counter > max_memory:
        #     sample_index = np.random.choice(max_memory, size=batch_size)
        # else:
        #     sample_index = np.random.choice(self.memory_counter, size=batch_size)
        # batch_memory = self.memory[sample_index, :]
        #
        # q_next = self.dnn.model_targ.predict(batch_memory[:, -self.state_size:])  # use next state to predict next Q
        # q_eval = self.dnn.model_eval.predict(batch_memory[:, :self.state_size])  # use state to predict evaluation Q
        # q_targ = q_eval.copy()
        #
        # batch_index = np.arange(batch_size, dtype=np.int32)
        # eval_action_index = batch_memory[:, self.state_size].astype(int)
        # reward = batch_memory[:, self.state_size+1]
        # q = q_targ[batch_index, eval_action_index]
        # q_targ[batch_index, eval_action_index] = q + self.alpha * (reward + self.gamma * np.max(q_next, axis=1) - q)
        #
        # self.dnn.model_eval.fit(
        #     x=batch_memory[:, :self.state_size], y=q_targ, epochs=10, verbose=0
        # )
        # self.learn_step_counter += 1

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

        # state = tf.expand_dims(state, axis=0)
        # next_state = tf.expand_dims(next_state, axis=0)
        # q_next = self.dnn.model_targ.predict(next_state)
        # q_eval = self.dnn.model_targ.predict(state)
        # q_targ = q_eval.copy()
        # q_targ[0, action] = reward + self.gamma * np.max(q_next, axis=1)
        #
        # self.dnn.model_eval.fit(
        #     x=state, y=q_targ, epochs=5, verbose=0
        # )
        # self.learn_step_counter += 1

    def get_action(self, state):
        # state = np.array(state)
        # state = tf.expand_dims(state, axis=0)
        if self.epochs <= 70:
            self.epsilon = (100 - self.epochs) / 200
        else:
            self.epsilon = 0.1
        if random.random() > self.epsilon:
            # action_value = self.dnn.model_targ.predict(state)
            state = torch.tensor(state, dtype=torch.float)
            predict_action = self.dnn(state)
            action = torch.argmax(predict_action).item()  # [0, 2]
        else:
            action = random.randint(0, 2)
        return action
