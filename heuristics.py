from queue import PriorityQueue
from typing import NamedTuple
from world import Position, World


def manhattan_distance(current, goal, *args):
    """ Manhattan distance between current and goal """
    x1, y1 = current
    x2, y2 = goal

    return abs(x1 - x2) + abs(y1 - y2)


def manhattan_distance_scaled(current, goal, *args):
    """ Manhattan distance between current and goal scaling heursitic slightly upwards in order to
    avoid ties, this slightly breaks admissibility of the heuristic.
    see http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html#breaking-ties"""
    heuristic = manhattan_distance(current, goal)
    heuristic *= (1 + 0.1)

    return heuristic


def heuristic_fudge(current, goal, start):
    """ Prefer positions that are along the straight line from the starting point to the goal by 
    multipying the manhattan distance by the vector cross product between the start and goal 
    vector and the current point to goal vector.
    Taken from http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html#breaking-ties"""
    x1, y1 = current
    x2, y2 = goal
    x3, y3 = start

    heuristic = manhattan_distance(current, goal)

    dx1 = x1 - x2
    dy1 = y1 - y2
    dx2 = x3 - x2
    dy2 = y3 - y2
    cross = abs(dx1 * dy2 - dx2 * dy1)
    heuristic += cross * 0.001
    return heuristic



