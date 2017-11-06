import sys
from bullet import Bullet
import pygame
from time import sleep
from zombie import Zombie


def check_events(settings, screen, stats, play_button, sb, survivor, zombies, bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, survivor, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, survivor)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, screen, stats, play_button, sb, survivor, zombies, bullets, mouse_x, mouse_y)


def check_play_button(settings, screen, stats, play_button, sb, survivor, zombies, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        settings.init_dynamic_set()

        pygame.mouse.set_visible(False)

        stats.reset_stats()
        sb.prep_score()
        sb.show_score()

        stats.game_active = True

        zombies.empty()
        bullets.empty()

        create_horde(settings, screen, zombies, survivor)
        survivor.center_surv()


def get_number_zombies_x(settings, zombies_width):
    available_space = settings.width - (2 * zombies_width)
    num_zombie_x = int(available_space / (2 * zombies_width))
    return num_zombie_x


def get_number_rows(settings, survivor_height, zombies_height):
    available_space_y = settings.height - (3 * zombies_height) - survivor_height
    number_rows = int(available_space_y / (4 * zombies_height))
    return number_rows


def create_zombie(settings, screen, zombies, zombie_number, row_number):
    zombie = Zombie(settings, screen)
    zombie_width = zombie.rect.width
    zombie.x = zombie_width + 2 * zombie_width * zombie_number
    zombie.rect.x = zombie.x
    zombie.rect.y = zombie.rect.height + 2 * zombie.rect.height * row_number
    zombies.add(zombie)


def create_horde(settings, screen, zombies, survivor):
    zombie = Zombie(settings, screen)
    number_zombies_x = get_number_zombies_x(settings, zombie.rect.width)
    for row_number in range(get_number_rows(settings, survivor.rect.height, zombie.rect.height)):
        for zombie_number in range(number_zombies_x):
            create_zombie(settings, screen, zombies, zombie_number, row_number)


def check_horde_edges(settings, zombies):
    for zombie in zombies.sprites():
        if zombie.check_edges():
            change_horde_direction(settings, zombies)
            break


def change_horde_direction(settings, zombies):
    for zombie in zombies.sprites():
        zombie.rect.y += settings.drop_speed
    settings.horde_direction *= - 1


def survivor_hit(settings, stats, screen, survivor, zombies, bullets):
    # Decrement the life of the survivor
    if stats.surv_left > 0:
        stats.surv_left -= 1
        zombies.empty()
        bullets.empty()
        create_horde(settings, screen, zombies, survivor)
        survivor.center_surv()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_zombies_bottom(settings, stats, screen, survivor, zombies, bullets):
    screen_rect = screen.get_rect()
    for zombie in zombies.sprites():
        if zombie.rect.bottom > screen_rect.bottom:
            survivor_hit(settings, stats, screen, survivor, zombies, bullets)
            break


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_screen(screen, settings, sb, survivor, stats, bullets, zombies, play_button):
        """Update images on the screen and flip to the new screen."""
        # Redraw the screen during each pass through the loop.
        screen.fill(settings.bg_color)
        screen.blit(settings.background, settings.background_rect)
        survivor.blitme()
        # Make the most recently drawn screen visible.
        zombies.draw(screen)
        for bullet in bullets:
            bullet.draw_bullet()
        sb.show_score()

        if not stats.game_active:
            play_button.draw_button()

        pygame.display.flip()


def check_keydown_events(event, settings, screen, survivor, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_d:
        survivor.moving_right = True
    elif event.key == pygame.K_a:
        survivor.moving_left = True
    elif event.key == pygame.K_w:
        survivor.moving_down = True
    elif event.key == pygame.K_s:
        survivor.moving_up = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, survivor, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, survivor):
    """Respond to key releases."""
    if event.key == pygame.K_d:
        survivor.moving_right = False
    elif event.key == pygame.K_a:
        survivor.moving_left = False
    elif event.key == pygame.K_w:
        survivor.moving_down = False
    elif event.key == pygame.K_s:
        survivor.moving_up = False


def update_bullets(settings, screen, stats, sb, survivor, bullets, zombies):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_zombies_collisions(settings, screen, stats, sb, survivor, zombies, bullets)


def check_bullet_zombies_collisions(settings, screen, stats, sb, survivor, zombies, bullets):
    collision = pygame.sprite.groupcollide(bullets, zombies, True, True)

    if collision:
        for zombies in collision.values():
            stats.score += settings.zombie_points * len(zombies)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(zombies) == 0:
        bullets.empty()
        settings.increase_speed()
        create_horde(settings, screen, zombies, survivor)


def fire_bullet(settings, screen, survivor, bullets):
    """Fire a bullet if limit not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < settings.bullets_allowed:
        new_bullet = Bullet(settings, screen, survivor)
        bullets.add(new_bullet)


def update_zombie(settings, stats, screen, survivor, zombies, bullets):
    check_horde_edges(settings, zombies)
    zombies.update()
    check_zombies_bottom(settings, stats, screen, survivor, zombies, bullets)

    if pygame.sprite.spritecollideany(survivor, zombies):
        survivor_hit(settings, stats, screen, survivor, zombies, bullets)

