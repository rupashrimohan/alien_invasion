import pygame.font
from ship import Ship

from pygame.sprite import Group
from pathlib import Path


class ScoreBoard:
    """A class to report scoring information"""

    def __init__(self, ai_game):
        """Initialize the attributes"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = self.screen.get_rect()
        self.stats = ai_game.gamestats

        # Font setting for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # prepare the scoe image
        self.prep_score()
        # prepare high score
        self.prep_high_score()
        # prepare the level
        self.prep_level()
        # prepare the ships
        self.prep_ship()

    def prep_score(self):
        """Turn the score into an image"""
        rounded_score = round(self.stats.score, -1)
        score_str = f"Score: {rounded_score:,}"
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color
        )
        # Display the score at the top right corner
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into the rendered image"""
        rounded_high_score = round(self.stats.high_score, -1)
        high_score_str = f"HighScore: {rounded_high_score:,}"
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.settings.bg_color
        )

        # center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Turn the level into an image"""
        level_str = f"Level: {self.stats.level}"
        self.level_img = self.font.render(
            level_str, True, self.text_color, self.settings.bg_color
        )

        # Adjust it to the top left
        self.level_rect = self.level_img.get_rect()
        self.level_rect.left = self.screen_rect.left + 20
        self.level_rect.top = 20

    def prep_ship(self):
        """Display the number of ships left for the player."""
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ai_game)
            # Scale the ship image to be smaller (e.g., 30x30 pixels)
            ship.image = pygame.transform.scale(ship.image, (30, 30))
            ship.rect = ship.image.get_rect()

            # Position them neatly in the top-left after the level
            ship.rect.x = (
                self.level_rect.right + 20 + ship_number * (ship.rect.width + 10)
            )
            ship.rect.y = 20

            self.ships.add(ship)

    def show_score(self):
        """Draw score, ships and level to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_img, self.level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        """Check to see of there is a new high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.write_high_score_tofile()
            self.prep_high_score()

    def write_high_score_tofile(self):
        """Write the high score to file and display"""
        path = Path("files/highscore.txt")
        path.write_text(str(self.stats.high_score))
