from typing import Iterator, NamedTuple
import json


# Position = NamedTuple('Position', [('x', int), ('y', int)])

class Position(NamedTuple):
    x: int
    y: int

    def __repr__(self) -> str:
        return f'({self.x}, {self.y})'


class World():
    size: tuple[int, int]
    obstacles: list[Position]
    movement = [(1,  0),
                (0,  1),
                (-1, 0),
                (0, -1),
                (0,  0)]

    def __init__(self, file='warehouse-empty.json') -> None:
        with open(file) as f:
            d = json.load(f)
            self.size = tuple(d['size'])
            self.obstacles = [Position(*pos) for pos in d['obstacles']]

    def in_bounds(self, pos: Position) -> bool:
        return 0 <= pos.x <= self.size[0] and 0 <= pos.y <= self.size[1]

    def passable(self, pos: Position) -> bool:
        return pos not in self.obstacles

    def neighbours(self, pos: Position) -> Iterator[Position]:
        pos = Position(*pos)
        # neighbours = (Position(pos.x + 1, pos.y),      # up
        #               Position(pos.x,     pos.y - 1),  # right
        #               Position(pos.x - 1, pos.y),      # down
        #               Position(pos.x,     pos.y + 1),  # left
        #               Position(pos.x,     pos.y))      # wait

        neighbours = (Position(pos.x + m[0], pos.y + m[1]) for m in self.movement)

        return filter(self.passable, filter(self.in_bounds, neighbours))


def distance(a: Position, b: Position) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)
