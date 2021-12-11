import pygame
import math
from pygame.locals import *
from sys import exit
import random
import numpy as np
import time

BLACK = 0, 0, 0
BLUE = 70, 130, 180
WHITE = 255, 255, 255

len = 40
P_obs = 0.12
num_prize = 10
delay = 150

pygame.init()  # 初始化py_game模块
screen = pygame.display.set_mode((1000, 800), 0, 32)  # 界面大小
pygame.display.set_caption("熊蜂模拟环境")  # 修改名称

obstacle = pygame.image.load('Pic/obstacle.png').convert()
obstacle = pygame.transform.scale(obstacle, (15, 15))
bombus = pygame.image.load('Pic/bombus.png').convert()
bombus = pygame.transform.scale(bombus, (30, 35))
prize = pygame.image.load('Pic/prize.png').convert()
prize = pygame.transform.scale(prize, (40, 40))

map = [(5 * len, 0), (15 * len, 0), (20 * len, 5 * len * math.sqrt(3)),
       (15 * len, 10 * len * math.sqrt(3)), (5 * len, 10 * len * math.sqrt(3)), (0, 5 * len * math.sqrt(3))]
# map = [(0, 0), (20 * len, 0), (20 * len, 10 * len * math.sqrt(3)), (0, 10 * len * math.sqrt(3))]
rows = 21
columns = 21

# the direction of the bombus standing for its head orienting
bom_dir = [1, 0, 0, 0, 0, 0]

# set points
points = []
bias = 0
for row in range(rows):
    if (row % 2 == 0):
        bias = 0
    else:
        bias = 0.5 * len
    for col in range(columns):
        x = col * len + bias
        y = row * 0.5 * len * math.sqrt(3)
        points.append((x, y))


def inside_map(x, y):
    flag = True
    if (x / (5 * len) + y / (5 * len * math.sqrt(3)) < 1):
        flag = False
    elif (x / (25 * len) + y / (25 * len * math.sqrt(3)) > 1):
        flag = False
    elif (x / (-5 * len) + y / (5 * len * math.sqrt(3)) > 1):
        flag = False
    elif (x / (15 * len) + y / (-15 * len * math.sqrt(3)) > 1):
        flag = False
    elif (y > 10 * len * math.sqrt(3) or y < 0):
        flag = False

    return flag


# set obstacle
obs_pos = []
obs_cache = []
for row in range(rows):
    for col in range(columns):
        if (col == columns - 1):
            break
        index_0 = row * rows + col
        index_1 = (row + 1) * rows + col + (row % 2)
        if (row == rows - 1):
            break
        if (random.random() < P_obs):
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
                if (inside_map(midpoint_x, midpoint_y) == False):
                    continue
                midpoint = (midpoint_x_str, midpoint_y_str)
                obs_cache.append(midpoint)
                pos = [midpoint_x - 6, midpoint_y - 6]
                obs_pos.append(pos)
            except IndexError:
                pass

# set bombus initial position
while True:
    rand = random.randint(0, rows * columns - 1)
    bom_pos = points[rand]
    x = bom_pos[0]
    y = bom_pos[1]
    bom_pos = [x - 18, y - 18]
    if (inside_map(x, y) == True):
        break


# bombus move
def bom_mov(pos, b_dir):
    x = pos[0] + 18
    y = pos[1] + 18
    x_orig = x
    y_orig = y
    dir = np.nonzero(b_dir)[0][0]

    # choose the heading direction
    rand = random.randint(0, 2)
    if (rand == 0):
        pass
    elif (rand == 1):
        if (dir == 5):
            dir = 0
            b_dir = [1, 0, 0, 0, 0, 0]
        else:
            dir = dir + 1
            b_dir = b_dir[0: -1]
            b_dir.insert(0, 0)
    elif (rand == 2):
        if (dir == 0):
            dir = 5
            b_dir = [0, 0, 0, 0, 0, 1]
        else:
            dir = dir - 1
            b_dir = b_dir[1:]
            b_dir.append(0)

    # determine the next position
    if (dir == 0):
        x = x + len
    elif (dir == 1):
        x = x + 0.5 * len
        y = y + 0.5 * len * math.sqrt(3)
    elif (dir == 2):
        x = x - 0.5 * len
        y = y + 0.5 * len * math.sqrt(3)
    elif (dir == 3):
        x = x - len
    elif (dir == 4):
        x = x - 0.5 * len
        y = y - 0.5 * len * math.sqrt(3)
    elif (dir == 5):
        x = x + 0.5 * len
        y = y - 0.5 * len * math.sqrt(3)

    # obstacle
    mid_x = '%.3f' % ((x_orig + x) / 2)
    mid_y = '%.3f' % ((y_orig + y) / 2)
    mid = (mid_x, mid_y)
    next_pos = (x - 18, y - 18)
    if (mid in obs_cache):
        return False

    # inside map
    if (inside_map(x, y) == False):
        return False

    return next_pos, b_dir


# set random prize
def set_prize(p_pos = None, p_ind = None, b_pos = None):
    global num_prize

    # initialize the position
    if (p_pos is None):
        counts = 0
        prize_pos = []
        index = []
        num_points = columns * rows
        while True:
            ind = random.randint(0, num_points - 1)
            p = points[ind]
            prize_x = p[0] - 20
            prize_y = p[1] - 20
            if (inside_map(p[0], p[1]) == True):
                if (ind not in index):
                    index.append(ind)
                    prize_pos.append((prize_x, prize_y))
                    counts = counts + 1
            if (counts == num_prize):
                return prize_pos, index

    # update prize
    flag = 0
    for i, p in enumerate(p_pos):
        p_x = '%.3f' % (p[0] + 20)
        p_y = '%.3f' % (p[1] + 20)
        p_orig = (p_x, p_y)
        if (b_pos == p_orig):
            flag = -1
            break
    if (flag != -1):
        return p_pos, p_ind
    num_points = columns * rows
    while True:
        ind = random.randint(0, num_points - 1)
        p = points[ind]
        prize_x = p[0] - 20
        prize_y = p[1] - 20
        if (inside_map(p[0], p[1]) == True):
            if (ind not in p_ind):
                break

    p_ind[i] = ind
    p_pos[i] = (prize_x, prize_y)
    return p_pos, p_ind

# main function
if __name__ == '__main__':
    # set initial prize
    prize_pos, prize_ind = set_prize()

    # run the pygame
    while True:
        # refresh the screen
        screen.fill(WHITE)

        # draw the polygon
        pygame.draw.polygon(screen, BLUE, map)

        # draw the point
        for point in points:
            pygame.draw.circle(screen, WHITE, point, 4)

        # draw the line
        for row in range(rows):
            for col in range(columns):
                if (col == columns - 1):
                    break
                index_0 = row * 21 + col
                index_1 = (row + 1) * 21 + col + (row % 2)
                start_pos = points[index_0]
                end_pos_0 = points[index_0 + 1]
                pygame.draw.line(screen, WHITE, start_pos, end_pos_0, 1)
                if (row == rows - 1):
                    break
                end_pos_1 = points[index_1]
                end_pos_2 = points[index_1 - 1]
                pygame.draw.line(screen, WHITE, start_pos, end_pos_1, 1)
                pygame.draw.line(screen, WHITE, start_pos, end_pos_2, 1)

        # draw the obstacles
        for obs in obs_pos:
            screen.blit(obstacle, obs)

        # draw the bombus
        screen.blit(bombus, bom_pos)
        times = 0
        # bombus move
        while True:
            times = times + 1
            if (times > 1000):
                exit()
            results = bom_mov(bom_pos, bom_dir)
            if (results != False):
                times = 0
                bom_pos, bom_dir = results
                break

        # update the prize
        for p in prize_pos:
            screen.blit(prize, p)
        b_x = '%.3f' % (bom_pos[0] + 18)
        b_y = '%.3f' % (bom_pos[1] + 18)
        b_pos = (b_x, b_y)
        prize_pos, prize_ind = set_prize(prize_pos, prize_ind, b_pos)

        # display on screen
        pygame.display.update()
        pygame.time.delay(delay)

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                time.sleep(5)
