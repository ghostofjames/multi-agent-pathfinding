import json

from agent import Agent
from task import Task
from world import Position, distance


class TaskManager():
    queue: list[Task]

    def __init__(self) -> None:
        self.tasks = []
        self.queue = []

    def add(self, task):
        if task not in self.tasks:
            self.tasks.append(task)
            self.queue.append(task)

    def load(self, file='task-list.json') -> None:
        with open(file) as f:
            for task in json.load(f):
                self.add(Task(id=task['id'],
                              start=Position(*task['start']),
                              end=Position(*task['end'])))

    def assign_task(self, agent: Agent) -> Task | None:
        try:
            task = self.get_closest_task(agent.position)
            self.queue.remove(task)
            return task
        except:
            return None

    def get_closest_task(self, pos: Position) -> Task:
        return min(self.queue, key=lambda task: distance(Position(*pos), Position(*task.start)))

    def all_complete(self) -> bool:
        return all(task.complete for task in self.tasks)
