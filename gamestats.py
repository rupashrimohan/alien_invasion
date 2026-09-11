from pathlib import Path


class GameStats:
    """Track statistics for Alien invasion game."""

    def __init__(self, ai_game):
        """Initializing the attributes"""
        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """Initialize the statistics that can change during the game"""
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        self.high_score = self._read_highscore_fromfile()

    def _read_highscore_fromfile(self):
        """Read high score from the file"""
        path = Path("files/highscore.txt")
        try:
            contents = path.read_text().strip()
        except FileNotFoundError:
            return 0
        else:
            if contents:
                return int(contents)
            else:
                return 0
