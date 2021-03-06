import matplotlib.pyplot as plt
from RL import Agent
from game import BombusGame
from utils import plot_epochs
# from ICP import ICPapi


plot_scores = []
plot_mean_scores = []
total_score = 0
record = 0
game = BombusGame()
agent = Agent(state_size=15)
# icp = ICPapi()
plt.ion()

practice_flag = 0

while True:
    # get old state
    state_old = agent.get_state(game)

    # get action
    action = agent.get_action(state_old)
    # if practice_flag:
        # send command to light stream screen
        # icp.dir2light(action)
        # get actual action
        # icp.get_actual_action()

    # perform the action and get new state
    scores, done, reward = game.play_step(next_dir=action)
    state_new = agent.get_state(game)

    # train short memory
    agent.train_short_memory(state_old, action, reward, state_new, done)

    # remember
    agent.store_in_memory(state_old, action, reward, state_new, done)

    if done:  # game over
        # train long memory
        game.reset()
        agent.epochs += 1
        agent.train_long_memory()

        if scores > record:
            record = scores
            agent.dnn.save(file_name=str(record)+'.pth')

        # print result every epoch
        print('Epoch #{}  Score {}  Record {}'.format(agent.epochs, scores, record))

        # plot
        plot_scores.append(scores)
        total_score += scores
        mean_scores = total_score / agent.epochs
        plot_mean_scores.append(mean_scores)
        plot_epochs(plot_scores, plot_mean_scores)
