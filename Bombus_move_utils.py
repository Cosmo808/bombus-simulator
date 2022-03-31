import math


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


def move(bom_pos, bom_present_dir, bom_next_dir, obs_cache, length=40):
    flag = True
    present_x = bom_pos[0] + 18
    present_y = bom_pos[1] + 18
    
    next_dir = bom_present_dir + bom_next_dir  # present:[0, 5]; next:[-1, 1]
    if next_dir == -1:
        next_dir = 5
    elif next_dir == 6:
        next_dir = 0
    
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
        present_x - length
        next_y = present_y
    elif next_dir == 4:
        next_x = present_x - 0.5 * length
        next_y = present_y - 0.5 * length * math.sqrt(3)
    elif next_dir == 5:
        next_x = present_x + 0.5 * length
        next_y = present_y - 0.5 * length * math.sqrt(3)

    # if not inside map
    if not inside_map(next_x, next_y):
        flag = False

    # if hit obstacle
    midpoint_x = '%.3f' % ((present_x + next_x) / 2)
    midpoint_y = '%.3f' % ((present_y + next_y) / 2)
    midpoint = [midpoint_x, midpoint_y]
    if midpoint in obs_cache:
        flag = False

    bombus_pos = [next_x - 18, next_y - 18]
    return bombus_pos, next_dir, flag


def next_dir_change(bom_pos, bom_present_dir, prize_pos):
    