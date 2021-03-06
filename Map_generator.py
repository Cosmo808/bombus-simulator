import pygame
import sys
from math import sqrt
import random
from utils import inside_map


def screen_map_set(rows=21, columns=21, length=40):
    rows -= 1
    columns -= 1
    screen = pygame.display.set_mode(((rows + 1) * length, (columns + 1) * length), 0, 32)  # 界面大小
    pygame.display.set_caption("Bombus Simulator")  # 修改名称
    map = [(rows / 4 * length, 0), (rows / 4 * 3 * length, 0), (rows * length, columns / 4 * length * sqrt(3)),
           (rows / 4 * 3 * length, columns / 2 * length * sqrt(3)),
           (rows / 4 * length, columns / 2 * length * sqrt(3)), (0, columns / 4 * length * sqrt(3))]
    return screen, map


def points_set(rows=21, columns=21, length=40):
    points = []
    bias = [
        [0, 0.5 * length], [-0.5 * length, 0]
    ]
    if rows % 4 == 1:
        bias = bias[0]
    elif rows % 4 == 3:
        bias = bias[1]

    try:
        for row in range(rows):
            if row % 2 == 0:
                b = bias[0]
            else:
                b = bias[1]
            for col in range(columns):
                x = col * length + b
                y = row * 0.5 * length * sqrt(3)
                points.append((x, y))
        return points
    except TypeError:
        print("\n", "Wrong Input...")
        sys.exit(0)


def obstacles_set(points, rows=21, columns=21, length=40, P_obs=0.12):
    obs_pos = []
    obs_cache = []
    for row in range(rows):
        for col in range(columns):
            if col == columns - 1:
                break
            index_0 = row * rows + col
            index_1 = (row + 1) * rows + col + (row % 2)
            if row == rows - 1:
                break
            if random.random() < P_obs:
                r = random.randint(0, 2)
                index = [(index_0, index_0 + 1), (index_0, index_1), (index_0, index_1 + 1)]
                index = index[r]
                try:
                    s_pos = points[index[0]]
                    e_pos = points[index[1]]
                    midpoint_x = (s_pos[0] + e_pos[0]) / 2
                    midpoint_y = (s_pos[1] + e_pos[1]) / 2
                    midpoint_x_str = '%.3f' % ((s_pos[0] + e_pos[0]) / 2)
                    midpoint_y_str = '%.3f' % ((s_pos[1] + e_pos[1]) / 2)
                    if not inside_map(midpoint_x, midpoint_y, rows, columns, length):
                        continue
                    midpoint = [midpoint_x_str, midpoint_y_str]
                    obs_cache.append(midpoint)
                    pos = [midpoint_x - 6, midpoint_y - 6]
                    obs_pos.append(pos)
                except IndexError:
                    pass
    return obs_pos, obs_cache


def prizes_set(points, prize_pos=None, prize_ind=None, bombus_pos=None,
               rows=21, columns=21, length=40, num_prize=10):
    # initialize the position
    num_points = columns * rows
    if prize_pos is None:
        counts = 0
        prize_pos = []
        index = []
        while True:
            ind = random.randint(0, num_points - 1)  # [0, num_points-1]
            p = points[ind]
            if inside_map(p[0], p[1], rows, columns, length):
                if ind not in index:
                    index.append(ind)
                    prize_x = p[0] - 20
                    prize_y = p[1] - 20
                    prize_pos.append((prize_x, prize_y))
                    counts = counts + 1
            if counts == num_prize:
                return prize_pos, index

    # update prize
    flag = False
    for i, p in enumerate(prize_pos):
        p_x = '%.3f' % (p[0] + 20)
        p_y = '%.3f' % (p[1] + 20)
        p_orig = (p_x, p_y)
        if bombus_pos == p_orig:
            flag = True  # success
            break
    if not flag:
        # bombus do not reach prize
        return prize_pos, prize_ind, flag
    # bombus reach the prize i
    while True:
        ind = random.randint(0, num_points - 1)
        p = points[ind]
        if inside_map(p[0], p[1], rows, columns, length):
            if ind not in prize_ind:
                break
    prize_x = p[0] - 20
    prize_y = p[1] - 20
    prize_ind[i] = ind
    prize_pos[i] = (prize_x, prize_y)
    return prize_pos, prize_ind, flag


def bombus_init_pos(points, rows=21, columns=21, length=40):
    while True:
        rand = random.randint(0, rows * columns - 1)
        bom_pos = points[rand]
        x = bom_pos[0]
        y = bom_pos[1]
        bom_pos = [x - 18, y - 18]
        if inside_map(x, y, rows, columns, length):
            break
    return bom_pos
