from typing import Iterator, NamedTuple
import json


class Position(NamedTuple):
    x: int
    y: int

    def __repr__(self) -> str:
        return f'({self.x}, {self.y})'


class World():
    size: tuple[int, int]
    obstacles: list[Position]
    movements = [(1,  0),
                 (0,  1),
                 (-1, 0),
                 (0, -1),
                 (0,  0)]

    def __init__(self, size, obstacles) -> None:
        self.size = size
        self.obstacles = obstacles

    @classmethod
    def from_file(cls, file='warehouse-empty.json'):
        with open(file) as f:
            d = json.load(f)
            size = tuple(d['size'])
            obstacles = [Position(*pos) for pos in d['obstacles']]
            return cls(size, obstacles)

    def in_bounds(self, pos: Position) -> bool:
        return 0 <= pos.x <= self.size[0] and 0 <= pos.y <= self.size[1]

    def passable(self, pos: Position) -> bool:
        return pos not in self.obstacles

    def neighbours(self, pos: Position) -> Iterator[Position]:
        pos = Position(*pos)

        neighbours = (Position(pos.x + move[0], pos.y + move[1]) for move in self.movements)

        return filter(self.passable, filter(self.in_bounds, neighbours))


def distance(a: Position, b: Position) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)
