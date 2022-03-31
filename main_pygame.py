import pygame
from pygame.locals import *
from sys import exit
import time
from tkinter import messagebox
import Map_generator
from Bombus_move_utils import move, next_dir_change


# set screen and map
pygame.init()  # 初始化py_game模块
screen, map = Map_generator.screen_map_set()


# load img
obstacle = pygame.image.load('Pic/obstacle.png').convert()
obstacle = pygame.transform.scale(obstacle, (15, 15))
bombus = pygame.image.load('Pic/bombus.png').convert()
bombus = pygame.transform.scale(bombus, (30, 35))
prize = pygame.image.load('Pic/prize.png').convert()
prize = pygame.transform.scale(prize, (40, 40))

# color
BLACK = 0, 0, 0
BLUE = 70, 130, 180
WHITE = 255, 255, 255

# param
rows = 21
columns = 21
length = 40
P_obs = 0.12
num_prize = 1
delay = 300
bom_present_dir = 0
bom_next_dir = 0

# set points
points = Map_generator.points_set()

# set init prize position
prize_pos, prize_ind = Map_generator.prizes_set(points)

# set obstacles
obs_pos, obs_cache = Map_generator.obstacles_set(points)

# set init bombus position
bom_pos = Map_generator.bombus_init_pos(points)

# run pygame
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
            if col == columns - 1:
                break
            index_0 = row * 21 + col
            index_1 = (row + 1) * 21 + col + (row % 2)
            start_pos = points[index_0]
            end_pos_0 = points[index_0 + 1]
            pygame.draw.line(screen, WHITE, start_pos, end_pos_0, 1)
            if row == rows - 1:
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

    # bombus move
    times = 0
    while True:
        times = times + 1
        if times > 30:
            messagebox.showerror('Error', 'OVERTIMES!')
            exit()

        # change the next direction
        bom_next_dir = next_dir_change(bom_pos, bom_present_dir, prize_pos)

        bombus_pos, next_dir, flag = move(bom_pos, bom_present_dir, bom_next_dir, obs_cache)
        if flag:  # successfully move
            bom_pos = bombus_pos  # update the position
            bom_present_dir = next_dir  # update the direction
            break

    # update the prize
    for p in prize_pos:
        screen.blit(prize, p)
    b_x = '%.3f' % (bom_pos[0] + 18)
    b_y = '%.3f' % (bom_pos[1] + 18)
    b_pos = (b_x, b_y)
    prize_pos, prize_ind = Map_generator.prizes_set(points, prize_pos, prize_ind, b_pos)

    # display on screen
    pygame.display.update()
    pygame.time.delay(delay)

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
