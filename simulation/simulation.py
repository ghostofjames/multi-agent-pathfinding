import json
import time
from itertools import combinations

from simulation.agent import Agent
from simulation.algorithms import CooperativeAStar, HierarchicalCooperativeAstar, WindowedCooperativeAStar, WindowedHierarchicalCooperativeAStar
from simulation.task import Task
from simulation.taskmanager import TaskManager
from simulation.world import Position, World

NUM_AGENTS = 8
NUM_TASKS = 30
DEFAULT_CONFIG = 'configs/small-14x14.json'
# DEFAULT_CONFIG = 'configs/medium-26x14.json'
# DEFAULT_CONFIG = 'configs/large-38x20.json'
# DEFAULT_CONFIG = 'configs/small-15x13-narrow.json'
# DEFAULT_CONFIG = 'configs/medium-27x13-narrow.json'
# DEFAULT_CONFIG = 'configs/large-39x19-narrow.json'

DEFAULT_SPEED = 5
DEFAULT_ALGORITHM = 'CA*'
ALGORITHMS = {'CA*': CooperativeAStar, 'HCA*': HierarchicalCooperativeAstar,
              'WHCA*': WindowedHierarchicalCooperativeAStar, 'WCA*': WindowedCooperativeAStar}


class Simulation():
    world: World
    agents: list[Agent]
    taskmanager: TaskManager

    time: int
    speed: int
    paused: bool
    complete: bool

    def __init__(self, speed=DEFAULT_SPEED, config=DEFAULT_CONFIG, algorithm=DEFAULT_ALGORITHM, nagents=NUM_AGENTS, ntasks=NUM_TASKS, thread=True):
        self.speed = speed
        self.time = 0
        self.paused = thread
        self.complete = False

        self.algorithm = algorithm
        self.config = config

        with open(config) as f:
            data = json.load(f)

            self.world = World((data['size'][0] - 1, data['size'][1] - 1),
                               [Position(*obstacle) for obstacle in data['obstacles']])

            self.agents = [Agent(agent['id'], Position(*agent['position']))
                           for agent in data['agents'][:nagents]]
            # shuffle(self.agents)

            self.solver = ALGORITHMS[algorithm](self.world, self.agents)

            tasks = [Task(task['id'], Position(*task['start']), Position(*task['end']))
                     for task in data['tasks'][:ntasks]]
            self.taskmanager = TaskManager(tasks)

        self.costs = {agent.id: 0 for agent in self.agents}
        self.processing_time = 0

    def step(self) -> None:
        ts = time.time()

        for agent in self.agents:
            # Task completion
            if agent.task and agent.goal_reached():
                if agent.task.picked_up == False:
                    agent.task.pick_up()
                    # print(f'{agent} has reached goal {agent.goal} and picked up item')
                else:
                    agent.task.deliver()
                    # print(f'{agent} has reached goal {agent.goal} and delivered item. {agent.task} is complete.')
                    agent.task = None

                agent.path = []

                continue  # Picking up or delivering an item takes a time step

            # Task assignment
            elif agent.task == None:
                agent.task = self.taskmanager.assign_task(agent)
                # print(f'{agent} has been assigned {agent.task}')

                if agent.task == None:
                    self.solver.reserve(agent.position, self.time, agent.id)

            # Path finding and movement
            if agent.path:

                agent.move()

                self.costs[agent.id] += 1

                if self.algorithm == 'WHCA*' and agent.path == []:
                    print(f'Finding continued path for {agent}')
                    path = self.solver.calculate_path(agent, self.time)
                    agent.path = path

            elif agent.path == []:
                print(f'Finding path for {agent}')
                path = self.solver.calculate_path(agent, self.time)
                agent.path = path

        # self.collision_test()

        self.time += 1

        te = time.time()

        self.processing_time += te-ts

        if self.taskmanager.all_complete:
            self.complete = True
            # print(f"all tasks have been complete, time taken was {self.time}")

            print('-' * 20)
            print(f'Map = {self.config}, Algorithm = {self.algorithm}, N.Agents = {len(self.agents)}')
            print(f'Time = {self.time}')
            print(f'Processing time = {self.processing_time}')
            print(f'Makespan = {max(self.costs.values())}')
            print(f'Sum of Costs = {sum(self.costs.values())}')
            print('-' * 20)

    def run(self) -> None:
        # run simulation until all tasks are complete
        while not self.taskmanager.all_complete:
            time.sleep(1 / self.speed)
            if not self.paused:
                self.step()

    def collision_test(self) -> None:
        for (a, b) in combinations(self.agents, 2):
            if a.position == b.position:
                raise Exception(
                    f'Agents {a.id} and {b.id} collided at {a.position} at {self.time}')
