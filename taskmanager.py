from typing import Iterator

from agent import Agent
from task import Task
from world import Position, distance


class TaskManager():
    queue: list[Task]

    def __init__(self) -> None:
        self.tasks = []

    @property
    def assigned(self) -> Iterator:
        return filter(lambda task: task.assigned, self.tasks)

    @property
    def unassigned(self) -> Iterator:
        return filter(lambda task: not task.assigned, self.tasks)

    @property
    def all_complete(self) -> bool:
        return all(task.complete for task in self.tasks)

    def add(self, tasks: list[Task]):
        for task in tasks:
            if task not in self.tasks:
                self.tasks.append(task)

    def assign_task(self, agent: Agent) -> Task | None:
        try:
            task = self.get_closest_task(agent.position)
            task.assigned = True
            return task
        except:
            return None

    def get_closest_task(self, pos: Position) -> Task:
        return min(self.unassigned, key=lambda task: distance(Position(*pos), Position(*task.start)))
