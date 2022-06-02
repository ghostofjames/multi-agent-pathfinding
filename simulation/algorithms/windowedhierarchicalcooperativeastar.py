from queue import PriorityQueue

from simulation.agent import Agent
from simulation.world import Position, World

from . import heuristics
from .hierarchicalcooperativeastar import HierarchicalCooperativeAstar, Node,Path

Node = tuple[Position, int]


class WindowedHierarchicalCooperativeAStar(HierarchicalCooperativeAstar):
    reservations: dict[tuple[Position, int], int | None]  # a space-time map

    def __init__(self, world: World, agents: list[Agent]):
        self.world = world
        self.reservations = {}
        self.agents = agents

        for agent in self.agents:
            self.reserve(agent.position, 0, agent.id)

        self.depth = 10
        self.max_depth = 14

        self.heuristics = {}

    def reserved(self, position: Position, time: int, id: int) -> bool:
        # check to see if a position in the reservation table is reserved
        r = self.reservations.get((position, time), None)
        if r == id or r == None:
            return False
        return True

    def reserve(self, position: Position, time: int, id: int) -> None:
        # Reserve a position in the space-time map
        self.reservations[(position, time)] = id

    def reserve_path(self, path: Path, id: int) -> None:
        # For each time step reserve agents planned position and next position after action
        for p in path:
            self.reserve(p[1], p[0], id)
            self.reserve(p[1], p[0] - 1, id)
        self.reserve(path[-1][1], path[-1][0] + 1, id)

    def astar(self, start: Position, goal: Position, heuristic, t: int, id: int) -> Path:
        # perform A* search
        open: PriorityQueue[tuple[int, tuple[Position, int, int]]] = PriorityQueue()
        closed: dict[Node, tuple[Node, int, int]] = {(start, t): ((start, t), 0, 0)}

        open.put((0, (start, t, 0)))

        start_node: Node = (start, t)

        while not open.empty():
            current_node = open.get()[1]
            c_pos, c_time, c_depth = current_node

            if c_depth == self.max_depth:
                return self.construct_path(closed, (c_pos, c_time), start_node)

            for neighbour in self.world.neighbours(c_pos):
                cost = 0 if neighbour == goal else 1

                g = closed[(c_pos, c_time)][1] + cost

                n_time = c_time + 1
                n_depth = c_depth + 1

                if self.reserved(neighbour, n_time, id):
                    continue

                if (neighbour, n_time) not in closed or g < closed[(neighbour, n_time)][1]:
                    f = g + heuristic.abstractDist(neighbour)
                    open.put((f, (neighbour, n_time, n_depth)))
                    closed[(neighbour, n_time)] = ((c_pos, c_time), g, n_depth)

        raise Exception('Path not found')

    def construct_path(self, closed: dict[Node, tuple[Node, int, int]], end_node: Node, start_node: Node) -> Path:
        # backtrack to form path
        current = end_node
        path: Path = []
        while current[1] != start_node[1]:
            path.append((current[1], current[0]))
            current = closed[current][0]
        path.reverse()
        return path

    def calculate_path(self, agent: Agent, t: int = 0) -> Path:
        # Calculate and return a path for the given agent, reserving the path
        if agent.goal is None:
            raise Exception('Cannot path find without goal')

        # get RRA* instance for agent and goal
        if (agent.id, agent.goal) not in self.heuristics:
            self.heuristics[(agent.id, agent.goal)] = self.ReverseResumableAstar(
                agent.position, agent.goal, self.world)

        path = self.astar(agent.position, agent.goal,
                          self.heuristics[(agent.id, agent.goal)], t, agent.id)
        self.reserve_path(path, agent.id)
        partial_path = path[:self.depth]
        return partial_path

    class ReverseResumableAstar():
        def __init__(self, initial: Position, goal: Position, w: World) -> None:
            self.w = w
            self.initial = initial
            self.goal = goal

            self.open: PriorityQueue[tuple[int, tuple[Position, int]]] = PriorityQueue()
            self.closed: dict[Position, int] = {}

            self.open.put((heuristics.manhattan_distance(initial, goal), (goal, 0)))

            self.resume(initial)

        def resume(self, N: Position) -> bool:
            while not self.open.empty():
                p = self.open.get()[1]
                self.closed[p[0]] = p[1]

                if p[0] == N:
                    if self.open.empty():
                        self.open.put((0, p))
                    return True

                for neighbour in reversed(list(self.w.neighbours(p[0]))):
                    g = p[1] + 1
                    h = heuristics.manhattan_distance(neighbour, self.initial)
                    if neighbour not in self.closed or g < self.closed[neighbour]:
                        self.open.put((h, (neighbour, g)))

            return False

        def abstractDist(self, N: Position):
            if N in self.closed:
                return self.closed[N]
            elif self.resume(N) == True:
                return self.closed[N]
            raise Exception('Not Found')
