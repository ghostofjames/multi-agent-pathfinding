from typing import Optional
from task import Task
from world import Position


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
        else:
            return None

    def __repr__(self) -> str:
        return f"Agent(id={self.id}, position={self.position}, goal={self.goal or None})"

    def goal_reached(self):
        return self.goal == self.position

    def move(self) -> None:
        if self.path and len(self.path) > 1:
            next = self.path.pop(0)
            self.position = next[1]
        elif self.path and len(self.path) == 1:
            # stay stationary
            self.position = self.path[0][1]
