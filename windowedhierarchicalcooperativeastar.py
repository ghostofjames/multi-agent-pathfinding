from queue import PriorityQueue
from hierarchicalcooperativeastar import HierarchicalCooperativeAstar, Node, Path
from world import Position, World


class WindowedHierarchicalCooperativeAStar(HierarchicalCooperativeAstar):
    d: int  # d depth

    def __init__(self, world: World):
        super().__init__(world)

    def astar(self, start: Position, goal: Position, t: int = 0) -> Path:
        open: PriorityQueue[tuple[int, Node]] = PriorityQueue()
        closed: dict[Node, tuple[Node, int]] = {(start, t): ((start, t), 0)}

        open.put((0, (start, t)))

        start_node: Node = (start, t)
        nodes_expanded: int = 0

        heuristic = self.ReverseResumableAstar(start, goal, self.world)

        reached_depth = 0

        while not open.empty():
            current_node: Node = open.get()[1]

            nodes_expanded += 1

            # if current_node[0] == goal:
            #     print(f'Nodes Expanded: {nodes_expanded}')
            #     return self.construct_path(closed, current_node, start_node)

            n_time = current_node[1] + 1
            for neighbour in self.world.neighbours(current_node[0]):

                if self.reserved(neighbour, n_time) or self.occupied(neighbour):
                    continue

                g = closed[current_node][1] + 1

                if (neighbour, n_time) not in closed or g < closed[(neighbour, n_time)][1]:
                    f = g + heuristic.abstractDist(neighbour)
                    open.put((f, (neighbour, n_time)))
                    closed[(neighbour, n_time)] = (current_node, g)
