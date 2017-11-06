import pygame
from pygame.sprite import Sprite


class Zombie(Sprite):
    def __init__(self, settings, screen):
        super(Zombie, self).__init__()
        self.screen = screen
        self.settings = settings

        self.image = pygame.image.load("zombie.png")
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.x += (self.settings.zombie_speed *
                   self.settings.horde_direction)
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
