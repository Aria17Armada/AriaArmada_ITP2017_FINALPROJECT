import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
import game_functions as gf
from survivor import Survivor


def run_game():
    # initializing pygame, settings, screen object
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.width,
                                      settings.height))
    pygame.display.set_caption('Zombies Game')

    # initiate data on status and scoreboard
    stats = GameStats(settings)
    sb = Scoreboard(settings, screen, stats)

    # initiate the play button
    play_button = Button(settings, screen, "Play")

    # initialize the survivor,bullets,and zombies
    survivor = Survivor(settings, screen)
    bullets = Group()
    zombies = Group()

    # create the horde
    gf.create_horde(settings, screen, zombies, survivor)

    while True:
        gf.check_events(settings, screen, stats, play_button, sb, survivor, zombies, bullets)
        if stats.game_active:
            survivor.update()
            gf.update_bullets(settings, screen, stats, sb, survivor, bullets, zombies)
            gf.update_zombie(settings, stats, screen, survivor, zombies, bullets)

        gf.update_screen(screen, settings, sb, survivor, stats, bullets, zombies, play_button)

        survivor.blitme()
        survivor.update()

        pygame.display.flip()

run_game()
# Establish world
# Render zombies
# Render "hero"
# Render Bullet
