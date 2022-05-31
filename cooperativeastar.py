from queue import PriorityQueue

import heuristics
from agent import Agent
from world import Position, World

Node = tuple[Position, int]
Path = list[tuple[int, Position]]


class CooperativeAStar():
    world: World
    agents: list[Agent]
    reservations: dict[tuple[Position, int], bool]  # a space-time map

    def __init__(self, world: World, agents: list[Agent]):
        self.world = world
        self.reservations = {}
        self.agents = agents

        for agent in self.agents:
            self.reserve(agent.position, 0)

    def reserved(self, position: Position, time: int) -> bool:
        # check to see if a position in the reservation table is reserved
        return self.reservations.get((position, time), False)

    def reserve(self, position: Position, time: int, *_) -> None:
        # Reserve a position in the space-time map
        self.reservations[(position, time)] = True

    def reserve_path(self, path: Path) -> None:
        # For each time step reserve agents planned position and next position after action
        for p in path:
            self.reserve(p[1], p[0])
            self.reserve(p[1], p[0] - 1)
        self.reserve(path[-1][1], path[-1][0] + 1)

    def astar(self, start: Position, goal: Position, t: int = 0) -> Path:
        # perform A* search
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

                if self.reserved(neighbour, n_time):
                    continue

                g = closed[current_node][1] + 1

                if (neighbour, n_time) not in closed or g < closed[(neighbour, n_time)][1]:
                    f = g + heuristics.heuristic_fudge(neighbour, goal, start)
                    open.put((f, (neighbour, n_time)))
                    closed[(neighbour, n_time)] = (current_node, g)

        raise Exception('Path not found')

    def construct_path(self, closed: dict[Node, tuple[Node, int]], end_node: Node, start_node: Node) -> Path:
        # backtrack to form path
        current = end_node
        path: Path = []
        while current != start_node:
            path.append((current[1], current[0]))
            current = closed[current][0]
        path.reverse()
        return path

    def calculate_path(self, agent: Agent, t: int = 0):
        # Calculate and return a path for the given agent, reserving the path
        if agent.goal is None:
            raise Exception('Cannot path find without goal')
        if agent.position == agent.goal:
            return [(t + 1, agent.position)]
        path = self.astar(agent.position, agent.goal, t)
        self.reserve_path([(t, agent.position)] + path)
        return path


class Solver():
    world: World
    agents: list[Agent]

    def __init__(self, world: World, agents: list[Agent]):
        self.world = world
        self.agents = agents

    def calculate_path(self, agent: Agent, time: int = 0):
        pass
