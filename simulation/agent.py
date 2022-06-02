from simulation.task import Task
from simulation.world import Position


class Agent():
    id: int
    position: Position
    task: Task | None
    path: list[tuple[int, Position]]

    def __init__(self, id: int, position: Position) -> None:
        self.id = id
        self.position = position
        self.path = []
        self.task = None

    @property
    def goal(self) -> Position | None:
        if self.task:
            return self.task.start if not self.task.picked_up else self.task.end
        else:  # If agent doesnt have a task, its goal should be to remain stationary
            return self.position

    def goal_reached(self) -> bool:
        return self.goal == self.position

    def move(self) -> None:
        if self.path:
            next = self.path.pop(0)
            self.position = next[1]
        else:
            pass

    def __repr__(self) -> str:
        return f"Agent(id={self.id}, position={self.position}, goal={self.goal or None})"

    def to_json(self):
        return {k: self.__dict__[k] for k in ('id', 'position')}
