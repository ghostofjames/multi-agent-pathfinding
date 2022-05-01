from queue import PriorityQueue
from typing import NamedTuple

from world import World, Position
from agent import Agent
import heuristics

Node = tuple[Position, int]
Path = list[tuple[int, Position]]


class CooperativeAStar():
    world: World
    agents: list[Agent]
    reservations: dict[tuple[Position, int], bool]  # a space-time map

    def __init__(self, world: World, heuristic=heuristics.manhattan_distance):
        self.world = world
        self.heuristic = heuristic
        self.reservations = {}
        self.agents = []

    def reserve(self, position: Position, time: int) -> None:
        print(position)
        self.reservations[(position, time)] = True

    def reserve_path(self, path: Path) -> None:
        """ For each time step reserve agents planned position and next position after action """
        for p in path:
            self.reserve(p[1], p[0])
            self.reserve(p[1], p[0] - 1)

    def reserved(self, position: Position, time: int) -> bool:
        return self.reservations.get((position, time), False)

    def occupied(self, position: Position) -> bool:
        for agent in self.agents:
            if agent.path and position == agent.path[-1][1]:
                # print(f'{position} is occupied')
                return True
        return False

    def add_agent(self, agent: Agent) -> None:
        self.agents.append(agent)
        self.reserve(agent.position, 0)

    def astar(self, start: Position, goal: Position, t: int = 0) -> Path:
        open: PriorityQueue[tuple[int, Node]] = PriorityQueue()
        closed: dict[Node, tuple[Node, int]] = {(start, t): ((start, t), 0)}

        open.put((0, (start, t)))

        start_node: Node = (start, t)

        while not open.empty():
            current_node: Node = open.get()[1]

            if current_node[0] == goal:
                return self.construct_path(closed, current_node, start_node)

            n_time = current_node[1] + 1
            for neighbour in self.world.neighbours(current_node[0]):

                if self.reserved(neighbour, n_time) or self.occupied(neighbour):
                    continue

                g = closed[current_node][1] + 1

                if (neighbour, n_time) not in closed or g < closed[(neighbour, n_time)][1]:
                    f = g + self.heuristic(neighbour, goal, start)
                    open.put((f, (neighbour, n_time)))
                    closed[(neighbour, n_time)] = (current_node, g)

        raise Exception('Path not found')

    def construct_path(self, closed, end_node, start_node) -> Path:
        # backtrack to form path
        current = end_node
        path: Path = []
        while current != start_node:
            path.append((current[1], current[0]))
            current = closed[current][0]
        path.reverse()
        return path

    def calculate_path(self, agent, t=0):
        path = self.astar(agent.position, agent.goal, t)
        self.reserve_path(path)
        return path

    def calculate_paths(self, t=0) -> None:
        for agent in self.agents:
            path = self.calculate_path(agent, t)
            agent.path = path
            print(path)
