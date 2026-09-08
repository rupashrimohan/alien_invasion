import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


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
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
            self._check_events()
            self.ship.update()
            # update the bullets
            self._update_bullets()
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

    # Helper method _update_screen
    def _update_screen(self):
        """Update images on the screena nd flip to the new screen"""
        self.screen.fill(self.settings.bg_color)
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
