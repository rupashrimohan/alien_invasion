import pygame
from pygame.sprite import Sprite


class Star(Sprite):
    """A class to manage a grid of stars."""

    def __init__(self, ai_game):
        """Initilaize the star class attributes."""

        super().__init__()
        self.screen = ai_game.screen

        # Let's just make a tiny white 2 x 2 pixel square for now
        self.image = pygame.Surface((2, 2))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()

        # start each start near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
