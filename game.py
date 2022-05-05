import pygame
import Map_generator
from utils import move


# color
BLUE = 70, 130, 180
WHITE = 255, 255, 255

# params
delay = 0
P_obstacle = 0.08
number_prize = 1


class BombusGame:

    def __init__(self, P_obs=P_obstacle, num_prize=number_prize):
        self.rows = 9
        self.columns = 9
        self.length = 40
        self.P_obs = P_obs  # distribution probability of obstacles
        self.num_prize = num_prize  # prize number
        self.font = None
        self.bom_present_dir = None  # bombus present direction
        self.points = None  # points in map
        self.prize_pos = None  # prize position
        self.prize_ind = None  # prize index
        self.obs_pos = None  # obstacle position
        self.obs_cache = None  # obstacle position cache
        self.bom_pos = None  # bombus position
        self.scores = None
        self.iteration = None
        self.screen = None
        self.map = None
        self.obstacle = None
        self.bombus = None
        self.prize = None
        self._load_img()
        self.reset()
        
    def _load_img(self):
        # init pygame
        pygame.init()
        self.screen, self.map = Map_generator.screen_map_set(self.rows, self.columns, self.length)
        self.font = pygame.font.Font('./Font/arial.ttf', 18)

        # load img
        self.obstacle = pygame.image.load('Pic/obstacle.png').convert()
        self.obstacle = pygame.transform.scale(self.obstacle, (15, 15))
        self.bombus = pygame.image.load('Pic/bombus.png').convert()
        self.bombus = pygame.transform.scale(self.bombus, (30, 35))
        self.prize = pygame.image.load('Pic/prize.png').convert()
        self.prize = pygame.transform.scale(self.prize, (40, 40))
        
    def reset(self):
        self.bom_present_dir = 0
        self.points = Map_generator.points_set(self.rows, self.columns, self.length)
        self.prize_pos, self.prize_ind = Map_generator.prizes_set(
            self.points, rows=self.rows, columns=self.columns, length=self.length, num_prize=self.num_prize
        )  # set init prize position
        self.obs_pos, self.obs_cache = Map_generator.obstacles_set(
            self.points, self.rows, self.columns, self.length, P_obs=self.P_obs
        )  # set obstacles
        self.bom_pos = Map_generator.bombus_init_pos(
            self.points, self.rows, self.columns, self.length
        )  # set init bombus position
        self.scores = 0  # reset score
        self.iteration = 0  # reset iteration
        # self.bom_pos_cache = []  # reset bombus position
        # self.bom_dir_cache = []  # reset bombus direction

    def draw_map(self):
        # refresh the self.screen
        self.screen.fill(WHITE)

        # draw the polygon
        pygame.draw.polygon(self.screen, BLUE, self.map)

        # draw the point
        for point in self.points:
            pygame.draw.circle(self.screen, WHITE, point, 4)

        # draw the line
        for row in range(self.rows):
            for col in range(self.columns):
                if col == self.columns - 1:
                    break
                index_0 = row * self.rows + col
                index_1 = (row + 1) * self.rows + col + (row % 2)
                start_pos = self.points[index_0]
                end_pos_0 = self.points[index_0 + 1]
                pygame.draw.line(self.screen, WHITE, start_pos, end_pos_0, 1)
                if row == self.rows - 1:
                    break
                end_pos_1 = self.points[index_1]
                end_pos_2 = self.points[index_1 - 1]
                pygame.draw.line(self.screen, WHITE, start_pos, end_pos_1, 1)
                pygame.draw.line(self.screen, WHITE, start_pos, end_pos_2, 1)

        # draw the obstacles
        for obs in self.obs_pos:
            self.screen.blit(self.obstacle, obs)

        # draw the bombus
        self.screen.blit(self.bombus, self.bom_pos)

    def play_step(self, next_dir):  # next_dir: [-1, 0, 1]
        self.iteration += 1

        # 0. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 1. draw map
        self.draw_map()

        # 2. bombus move
        bom_next_dir = next_dir  # change the next direction
        bombus_pos, next_dir, flag, punish = move(self.bom_pos, self.bom_present_dir, bom_next_dir, self.obs_cache,
                                                  self.rows, self.columns, self.length)
        self.bom_pos = bombus_pos  # update the position
        self.bom_present_dir = next_dir  # update the direction
        # self.bom_pos_cache.append(self.bom_pos)
        # self.bom_dir_cache.append(self.bom_present_dir)

        # 3. check if game over
        if flag:  # successfully move
            reward = 0
            done = False
        else:  # game over
            reward = punish
            done = True

        # 4. update the prize
        for p in self.prize_pos:
            self.screen.blit(self.prize, p)
        b_x = '%.3f' % (self.bom_pos[0] + 18)
        b_y = '%.3f' % (self.bom_pos[1] + 18)
        b_pos = (b_x, b_y)
        self.prize_pos, self.prize_ind, flag = Map_generator.prizes_set(
            self.points, self.prize_pos, self.prize_ind, b_pos,
            self.rows, self.columns, self.length, num_prize=number_prize)
        if flag:  # successfully reach the prize
            self.scores += 1
            reward = 10

        # 5. display the score
        text = self.font.render("Score: " + str(self.scores), True, BLUE)
        self.screen.blit(text, [0, 0])

        # 6. display on screen
        pygame.display.update()
        pygame.time.delay(delay)

        return self.scores, done, reward
