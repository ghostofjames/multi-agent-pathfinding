from world import Position


class Task():
    id: int
    start: Position
    end: Position
    assigned: bool
    picked_up: bool
    complete: bool

    def __init__(self, id: int, start: Position, end: Position) -> None:
        self.id = id
        self.start = start
        self.end = end
        self.assigned = False
        self.picked_up = False
        self.complete = False

    def __repr__(self) -> str:
        return f"Task({self.id=}, {self.start=}, {self.end=})"

    def pick_up(self):
        self.picked_up = True

    def deliver(self):
        self.complete = True

    def to_json(self):
        return {k: self.__dict__[k] for k in ('id', 'start', 'end')}
