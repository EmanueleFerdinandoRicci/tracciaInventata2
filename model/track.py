from dataclasses import dataclass


@dataclass
class Track:
    TrackId: int
    Name: str
    AlbumId: int
    MediaTypeId: int
    GenreId: int
    Composer: str
    Milliseconds: int
    Bytes: int
    UnitPrice: float

    def __hash__(self):
        return hash(self.TrackId)

    def __eq__(self, other):
        return self.TrackId == other.TrackId

    def __str__(self):
        return f"{self.Name}"