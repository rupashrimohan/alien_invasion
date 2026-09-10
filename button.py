import pygame.font


class Button:
    """A class to build buttons for the game."""

    def __init__(self, ai_game, msg):
        """Initializing the button attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of a button
        self.but_width = 200
        self.but_height = 50
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # center the button
        self.rect = pygame.Rect(0, 0, self.but_width, self.but_height)
        self.rect.center = self.screen_rect.center

        # Preparing button message
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn the message into an image and fix it at the center if the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw balnk button and then draw the msg image."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
