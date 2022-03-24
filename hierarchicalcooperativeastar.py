from queue import PriorityQueue
from cooperativeastar import CooperativeAStar, Node, Path
import heuristics
from world import Position, World


class HierarchicalCooperativeAstar(CooperativeAStar):
    def __init__(self, world: World):
        self.world = world
        self.reservations = {}
        self.agents = []

    def astar(self, start: Position, goal: Position, t: int = 0) -> Path:
        open: PriorityQueue[tuple[int, Node]] = PriorityQueue()
        closed: dict[Node, tuple[Node, int]] = {(start, t): ((start, t), 0)}

        open.put((0, (start, t)))

        start_node: Node = (start, t)
        nodes_expanded: int = 0

        heuristic = self.ReverseResumableAstar(start, goal, self.world)

        while not open.empty():
            current_node: Node = open.get()[1]

            nodes_expanded += 1

            if current_node[0] == goal:
                print(f'Nodes Expanded: {nodes_expanded}')
                return self.construct_path(closed, current_node, start_node)

            n_time = current_node[1] + 1
            for neighbour in self.world.neighbours(current_node[0]):

                if self.reserved(neighbour, n_time) or self.occupied(neighbour):
                    continue

                g = closed[current_node][1] + 1

                if (neighbour, n_time) not in closed or g < closed[(neighbour, n_time)][1]:
                    f = g + heuristic.abstractDist(neighbour)
                    open.put((f, (neighbour, n_time)))
                    closed[(neighbour, n_time)] = (current_node, g)

        raise Exception('Path not found')

    class ReverseResumableAstar():
        def __init__(self, initial: Position, goal: Position, w: World) -> None:
            self.w = w
            self.initial = initial
            self.goal = goal

            self.open: PriorityQueue[tuple[int, tuple[Position, int]]] = PriorityQueue()
            self.closed: dict[Position, int] = {}

            self.open.put((heuristics.manhattan_distance(initial, goal), (goal, 0)))

            self.resume(initial)

        def resume(self, N: Position):
            while open:
                p = self.open.get()[1]
                self.closed[p[0]] = p[1]

                if p[0] == N:
                    return True

                for neighbour in reversed(list(self.w.neighbours(p[0]))):
                    g = p[1] + 1
                    h = heuristics.manhattan_distance(neighbour, self.initial)
                    if neighbour not in self.closed or g < self.closed[neighbour]:
                        # self.closed[neighbour] = g
                        self.open.put((h, (neighbour, g)))

            return False

        def abstractDist(self, N):
            if N in self.closed:
                return self.closed[N]
            elif self.resume(N) == True:
                return self.closed[N]
            raise Exception('Not Found')
