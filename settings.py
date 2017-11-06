import pygame


class Settings():
    def __init__(self):
        # screen settings
        self.bg_color = (255, 255, 255)

        # GAME DIMENSIONS
        self.TILESIZE = 30
        self.MAPWIDTH = 40
        self.MAPHEIGHT = 30

        # true dimensions
        self.width = self.TILESIZE*self.MAPWIDTH
        self.height = self.TILESIZE*self.MAPHEIGHT


        # surv set
        self.surv_limit = 3

        # bullet set
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 6

        # how fast the game will speed up
        self.speedup_scale = 1.2

        #
        self.drop_speed = 10

        # Zombie value increase
        self.score_scale = 1.5

        # Zombie movement speed
        self.zombie_move_speed = 10

        # Background
        self.background = pygame.image.load('tileset.png')
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.background_rect = self.background.get_rect()

        self.init_dynamic_set()

    def init_dynamic_set(self):
        # Settings that change throughout the game
        self.surv_speed = 3
        self.bullet_speed_factor= 4
        self.zombie_speed = 3
        self.horde_direction = 1

        # scoring
        self.zombie_points = 50

    def increase_speed(self):
        # increase speed settings and zombie point values
        self.surv_speed *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.zombie_speed *= self.speedup_scale

        self.zombie_points = int(self.zombie_points * self.score_scale)
