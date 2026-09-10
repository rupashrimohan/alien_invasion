import sys

import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star
from random import randint
from gamestats import GameStats


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")
        # Create an instance of the game stats
        self.gamestats = GameStats(self)
        self.stars = pygame.sprite.Group()
        self._create_stars()
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        # start the game in an active state
        self.game_active = True

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
            self._check_events()
            if self.game_active == True:
                self.ship.update()
                # update the bullets
                self._update_bullets()
                # update the aliens fleet (moving to the right)
                self._update_aliens()
            # Update the screen
            self._update_screen()
            self.clock.tick(60)

    # Helper Methos _check_events
    def _check_events(self):
        """Repsond to events like keyboard presses and mouse."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    # Helper method _check_keydown_events
    def _check_keydown_events(self, event):
        """Check the keydown event and set the flag value"""
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Move the ship to the left
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    # Helper method _check_keyup_events
    def _check_keyup_events(self, event):
        """Check the keydup event and set the flag value"""
        if event.key == pygame.K_RIGHT:
            # stop moving the ship to the right
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            # stop moving the ship to the left
            self.ship.moving_left = False

    # Helper method to fire the bullet
    def _fire_bullet(self):
        """Create a new bullet and add to the bullet group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    # Helper methods to create alien fleet
    def _create_fleet(self):
        """Create a fleet of aliens."""
        # Create an alien and keep adding until there is no room left.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (
            self.settings.screen_height - (3 * alien_height) - self.ship.rect.height
        ):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            # Fininshed a row; reset x value and increment y value
            current_x = alien_width
            current_y += 2 * alien_height

    # Helper method to create a new Alien
    def _create_alien(self, x_position, y_position):
        """Create and alien and place it in the fleet."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    # Helper method to update the bullets.
    def _update_bullets(self):
        """Update the position of the bullet and get rid of the old bullets."""
        self.bullets.update()
        # Getting rid of the bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()

    # Helper method to check collision
    def _check_bullet_alien_collision(self):
        """Check for collisions between alien and bullet and create a new fleet."""
        # Check for any bullets that have hit aliens.
        # If so, get rid of the bullet and the alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, False, True)
        if not self.aliens:
            # Destroy the bullets and create a new fleet
            self.bullets.empty()
            self._create_fleet()

    def _create_stars(self):
        """Grid of stars"""
        num_of_stars = 100

        for _ in range(num_of_stars):
            star = Star(self)
            random_x = randint(0, self.screen.width)
            random_y = randint(0, self.screen.height)

            star.rect.x = random_x
            star.rect.y = random_y

            self.stars.add(star)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Chnage fleet direction by dropping the entire fleet."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    # Helper methos to update tha liens position
    def _update_aliens(self):
        """Check if the fleet is at the edge and then update its position"""
        self._check_fleet_edges()
        self.aliens.update()
        # Look for alien ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Cehck if the aliens hit the bottom of the screen
        self._check_aliens_bottom()

    # Ship hit helper method
    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.gamestats.ship_left > 0:
            # Decrement the ships by 1
            self.gamestats.ship_left -= 1

            # Get rid of remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship's position
            self._create_fleet()
            self.ship.center_ship()

            # pause the game
            sleep(0.5)
        else:
            self.game_active = False

    def _check_aliens_bottom(self):
        """Check if aliens hits the bottom of the screen and respond."""
        for alien in self.aliens.sprites():
            if alien.check_bottom_edge():
                self._ship_hit()
                break

    # Helper method _update_screen
    def _update_screen(self):
        """Update images on the screen and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)
        # Draw the stars first
        self.stars.draw(self.screen)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Make the most recently drawn screen visible.
        pygame.display.flip()


if __name__ == "__main__":
    # Make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()
