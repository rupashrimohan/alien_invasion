class GameStats:
    """Track statistics for Alien invasion game."""

    def __init__(self, ai_game):
        """Initializing the attributes"""
        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """Initialize the statistics that can change during the game"""
        self.ship_left = self.settings.ship_limit
