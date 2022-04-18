from queue import PriorityQueue
from turtle import position
from hierarchicalcooperativeastar import HierarchicalCooperativeAstar, Node, Path
from world import Position, World


Node = tuple[Position, int]


class WindowedHierarchicalCooperativeAStar(HierarchicalCooperativeAstar):
    max_depth: int  # max depth d

    def __init__(self, world: World, depth: int):
        super().__init__(world)
        self.max_depth = depth

    def astar(self, start: Position, goal: Position, t: int = 0) -> Path:
        open: PriorityQueue[tuple[int, tuple[Position, int, int]]] = PriorityQueue()
        closed: dict[Node, tuple[Node, int, int]] = {(start, t): ((start, t), 0, 0)}

        open.put((0, (start, t, 0)))

        start_node: Node = (start, t)

        heuristic = self.ReverseResumableAstar(start, goal, self.world)

        while not open.empty():
            current_node = open.get()[1]
            c_pos, c_time, c_depth = current_node

            if c_depth == self.max_depth:
                from pprint import pprint
                # pprint(closed)
                return self.construct_path(closed, (c_pos, c_time), start_node)

            for neighbour in self.world.neighbours(c_pos):
                g = closed[(c_pos, c_time)][1] + 1
                n_time = c_time + 1
                n_depth = c_depth + 1

                if self.reserved(neighbour, n_time) or self.occupied(neighbour):
                    continue

                if (neighbour, n_time) not in closed or g < closed[(neighbour, n_time)][1]:
                    f = g + heuristic.abstractDist(neighbour)
                    open.put((f, (neighbour, n_time, n_depth)))
                    closed[(neighbour, n_time)] = ((c_pos, c_time), g, n_depth)

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


s = WindowedHierarchicalCooperativeAStar(World(), 4)
# p = s.astar(Position(0, 0), Position(10, 0))
# print(p)
# p = s.astar(p[-1][1], Position(10, 0))
# print(p)
# p = s.astar(p[-1][1], Position(10, 0))
# print(p)
# p = s.astar(p[-1][1], Position(10, 0))
# print(p)
p = s.astar(Position(10, 0), Position(10, 0))
print(p)
