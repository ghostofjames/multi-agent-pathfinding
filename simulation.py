from itertools import combinations
import time

from agent import Agent
from hierarchicalcooperativeastar import HierarchicalCooperativeAstar
from world import Position, World
from taskmanager import TaskManager
from cooperativeastar import CooperativeAStar, heuristics


from functools import wraps


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()
        print(f'func: {f.__name__} took: {te-ts} sec')
        return result
    return wrap


class Simulation():
    world: World
    agents: list[Agent]
    taskmanager: TaskManager

    time: int
    speed: float
    paused: bool
    complete: bool

    def __init__(self, world='warehouse.json', speed=1):
        self.speed = speed
        self.world = World(world)

        self.time = -1

        # self.agents = [Agent(0, Position(1, 1)),
        #                Agent(1, Position(0, 0)),
        #                Agent(2, Position(0, 2)),
        #                Agent(3, Position(0, 1))]

        self.agents = [Agent(0, Position(0,  0)),
                       Agent(1, Position(10, 0)),
                       Agent(2, Position(0,  10)),
                       Agent(3, Position(10, 10))]

        # self.agents = [Agent(0, Position(0,  0)),
        #                Agent(1, Position(10, 0)),
        #                Agent(2, Position(0,  10)),
        #                Agent(3, Position(10, 10)),
        #                Agent(4, Position(0,   2)),
        #                Agent(5, Position(10,  2)),
        #                Agent(6, Position(0,   8)),
        #                Agent(7, Position(10, 8))]

        self.taskmanager = TaskManager()
        self.taskmanager.load('task-list.json')

        # self.taskmanager.assign_tasks(self.agents)

        # self.solver = CooperativeAStar(self.world, heuristic=heuristics.heuristic_fudge)
        self.solver = HierarchicalCooperativeAstar(self.world)

        for agent in self.agents:
            self.solver.add_agent(agent)

        self.paused = True
        self.complete = False

    @timing
    def step(self):
        self.time += 1

        for agent in self.agents:
            if agent.task == None:
                agent.task = self.taskmanager.assign_task(agent)
                # print(f'{agent} has been assigned {agent.task}')

            elif agent.goal_reached():
                # print(f'{agent} has reached goal {agent.goal}')
                if agent.task.picked_up == False:
                    agent.task.pick_up()
                    # print(f'Agent has picked up item and is moving to destination.')
                else:
                    agent.task.put_down()
                    # print(f'Agent has delivered item and {agent.task} is complete.')
                    agent.task = None

            elif agent.path == [] or (len(agent.path) == 1 and agent.path[0][1] == agent.position):
                # print(f'Finding path for {agent} to goal {agent.goal}')
                path = self.solver.calculate_path(agent, self.time)
                agent.path = path

            else:
                agent.move()

        self.collision_test()

        if self.taskmanager.all_complete():
            print(f"all tasks have been complete, time taken was {self.time}")
            self.complete = True

    def run(self):
        # run simulation until all agents reach goal
        # while not all(agent.goal_reached() for agent in self.agents):
        while True:
            time.sleep(self.speed)
            if self.paused:
                continue
            elif self.complete:
                continue
            else:
                self.step()

    def collision_test(self):
        for (a, b) in combinations(self.agents, 2):
            if a.position == b.position:
                raise Exception(
                    f'Agents {a.id} and {b.id} collided at {a.position} at {self.time}')
