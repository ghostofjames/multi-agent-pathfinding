from typing import Iterator

from simulation.agent import Agent
from simulation.task import Task
from simulation.world import Position, distance


class TaskManager():
    tasks: list[Task]

    def __init__(self, tasks: list[Task]) -> None:
        self.tasks = tasks

    @property
    def incomplete(self) -> Iterator[Task]:
        return filter(lambda task: not task.complete, self.tasks)

    @property
    def unassigned(self) -> Iterator[Task]:
        return filter(lambda task: not task.assigned, self.tasks)

    @property
    def assigned(self) -> Iterator[Task]:
        return filter(lambda task: task.assigned, self.tasks)

    @property
    def all_complete(self) -> bool:
        return all(task.complete for task in self.tasks)

    def assign_task(self, agent: Agent) -> Task | None:
        try:
            task = self.get_closest_task(agent.position)
            task.assigned = True
            return task
        except:
            return None

    def get_closest_task(self, pos: Position) -> Task:
        return min(self.unassigned, key=lambda task: distance(pos, task.start))
