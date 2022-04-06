import math
from IPython import display
import matplotlib.pyplot as plt


def inside_map(x, y, length=40):
    flag = True
    if x / (5 * length) + y / (5 * length * math.sqrt(3)) < 1:
        flag = False
    elif x / (25 * length) + y / (25 * length * math.sqrt(3)) > 1:
        flag = False
    elif x / (-5 * length) + y / (5 * length * math.sqrt(3)) > 1:
        flag = False
    elif x / (15 * length) + y / (-15 * length * math.sqrt(3)) > 1:
        flag = False
    elif y > 10 * length * math.sqrt(3) or y < 0:
        flag = False
    return flag


def get_nextxy(present_x, present_y, next_dir, length=40.0):
    next_x = None
    next_y = None
    if next_dir == 0:
        next_x = present_x + length
        next_y = present_y
    elif next_dir == 1:
        next_x = present_x + 0.5 * length
        next_y = present_y + 0.5 * length * math.sqrt(3)
    elif next_dir == 2:
        next_x = present_x - 0.5 * length
        next_y = present_y + 0.5 * length * math.sqrt(3)
    elif next_dir == 3:
        next_x = present_x - length
        next_y = present_y
    elif next_dir == 4:
        next_x = present_x - 0.5 * length
        next_y = present_y - 0.5 * length * math.sqrt(3)
    elif next_dir == 5:
        next_x = present_x + 0.5 * length
        next_y = present_y - 0.5 * length * math.sqrt(3)
    return next_x, next_y


def move(bom_pos, bom_present_dir, bom_next_dir, obs_cache, length=40.0):
    flag = True
    punish = 0
    present_x = bom_pos[0] + 18
    present_y = bom_pos[1] + 18

    next_dir = bom_present_dir + (bom_next_dir - 1)  # present:[0, 5]; next-1:[-1, 1]
    if next_dir == -1:
        next_dir = 5
    elif next_dir == 6:
        next_dir = 0

    next_x, next_y = get_nextxy(present_x, present_y, next_dir)

    # if not inside map
    if not inside_map(next_x, next_y):
        punish = -10
        flag = False

    # if hit obstacle
    midpoint_x = '%.3f' % ((present_x + next_x) / 2)
    midpoint_y = '%.3f' % ((present_y + next_y) / 2)
    midpoint = [midpoint_x, midpoint_y]
    if midpoint in obs_cache:
        punish = -10
        flag = False

    bombus_pos = [next_x - 18, next_y - 18]
    return bombus_pos, next_dir, flag, punish


def plot_epochs(plot_scores, plot_mean_scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.cla()
    plt.title('Training')
    plt.xlabel('Epochs')
    plt.ylabel('Scores')
    plt.plot(plot_scores)
    plt.plot(plot_mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(plot_scores) - 1, plot_scores[-1], str(plot_scores[-1]))
    plt.text(len(plot_mean_scores) - 1, plot_mean_scores[-1], str(plot_scores[-1]))
    plt.pause(0.1)


def game2state(game):
    present_dir = game.bom_present_dir
    bom_pos = game.bom_pos
    obs_cache = game.obs_cache
    prize_pos = game.prize_pos

    if_obs = [0, 0, 0]
    if_prize = [0, 0, 0, 0]

    present_x = bom_pos[0] + 18
    present_y = bom_pos[1] + 18

    # if obs or border in 3 directions
    for action in range(0, 3):
        next_dir = present_dir + (action - 1)
        if next_dir == -1:
            next_dir = 5
        elif next_dir == 6:
            next_dir = 0
        next_x, next_y = get_nextxy(present_x, present_y, next_dir)
        # if hit obstacle
        midpoint_x = '%.3f' % ((present_x + next_x) / 2)
        midpoint_y = '%.3f' % ((present_y + next_y) / 2)
        midpoint = [midpoint_x, midpoint_y]
        if midpoint in obs_cache or not inside_map(next_x, next_y):
            if_obs[action] = 1

    # if prize in 4 sectors
    for prize in prize_pos:
        p_x = prize[0] + 20.0
        p_y = prize[1] + 20.0
        relative_x = p_x - present_x
        relative_y = p_y - present_y
        distance = math.sqrt(relative_x * relative_x + relative_y * relative_y)
        if distance == 0:
            continue
        cos = relative_x / distance
        degree = math.acos(cos) / math.pi * 180
        if relative_y < 0:
            degree = 360 - degree
        degree = degree + 60 * present_dir
        while degree >= 360:
            degree -= 360  # range: [0, 360]
            
        if degree <= 30 or degree >= 330:  # if in sector 1
            if_prize[0] = 1
        elif 30 < degree <= 90:  # if in sector 2
            if_prize[1] = 1
        elif 270 <= degree < 330:
            if_prize[2] = 1
        else:
            if_prize[3] = 1

    state = [
        present_dir,  # bombus present direction, range: [0, 5]

        if_obs[0],  # if obstacle in direction -1, default 0
        if_obs[1],  # if obstacle in direction 0, default 0
        if_obs[2],  # if obstacle in direction 1, default 0

        if_prize[0],  # if prize in sector 1, default 0
        if_prize[1],  # if prize in sector 2, default 0
        if_prize[2],  # if prize in sector 3, default 0
        if_prize[3],  # if prize in sector 4, default 0
    ]

    return state
