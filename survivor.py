import pygame
import math


class Survivor():
    def __init__(self, settings, screen):
        self.screen = screen
        self.moving_right = False
        self.moving_left = False
        self.moving_down = False
        self.moving_up = False
        self.settings = settings

        self.image = pygame.image.load('Shooter (2).png')

        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        self.centerx = float(self.screen_rect.centerx)
        self.centery = float(self.screen_rect.centery)

        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.settings.surv_speed
        if self.moving_left and self.rect.left > 0:
            self.centerx -= self.settings.surv_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery -= self.settings.surv_speed
        if self.moving_up and self.rect.top > 0:
            self.centery += self.settings.surv_speed
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def blitme(self):
        """Draw the survivor at its current location."""
        (pos) = pygame.mouse.get_pos()

        surv = self.image

        angle = 360-math.atan2(pos[1]-300, pos[0]-400)*180/math.pi
        rotimage = pygame.transform.rotate(surv, angle)
        rect = rotimage.get_rect(center=(self.centerx, self.centery))
        self.screen.blit(rotimage, rect)

    def center_surv(self):
        self.centerx = self.screen_rect.centerx
        self.centery = self.screen_rect.centery

