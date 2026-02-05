from dataclasses import dataclass
from model.artist import Artist

@dataclass
class Connection:
    artist1: Artist
    artist2: Artist
    n_genres: int

    def __str__(self):
        return f"{self.artist1} - {self.artist2} - {self.n_genres}"
