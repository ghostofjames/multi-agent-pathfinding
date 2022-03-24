from world import Position


class Task():
    id: int
    start: Position
    end: Position
    complete: bool

    def __init__(self, id: int, start: Position, end: Position) -> None:
        self.id = id
        self.start = start
        self.end = end
        self.complete = False
        self.picked_up = False

    def __repr__(self) -> str:
        return f"Task({self.id=}, {self.start=}, {self.end=})"

    def pick_up(self):
        self.picked_up = True

    def put_down(self):
        self.complete = True
