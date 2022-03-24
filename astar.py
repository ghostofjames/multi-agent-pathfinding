from queue import PriorityQueue
from world import World, Position


def h(a, b):
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)


def astar(world: World, start: Position, goal: Position):
    open: PriorityQueue[tuple[int, Position]] = PriorityQueue()
    closed: dict[Position, tuple[Position, int]] = {start: (start, 0)}
    open.put((0, start))

    while not open.empty():
        current = open.get()[1]
        if current == goal:
            break

        for neighbour in world.neighbours(current):
            g = closed[current][1] + 1
            if neighbour not in closed or g < closed[neighbour][1]:
                f = g + h(neighbour, goal)
                open.put((f, neighbour))
                closed[neighbour] = (current, g)
                print(closed[neighbour])

    # backtrack to form path
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = closed[current][0]
    path.append(start)
    path.reverse()
    return path
