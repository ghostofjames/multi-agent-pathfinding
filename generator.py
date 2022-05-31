# Script for generating random tasks within a world

import json
import random
from agent import Agent
from task import Task

from world import Position, World, distance

with open('configs/large-39x19-narrow.json') as f:
    data = json.load(f)
    world = World((data['size'][0] - 1, data['size'][1] - 1),
                  [Position(*obstacle) for obstacle in data['obstacles']])

# Generate Random Tasks
ntasks = 30
tasks = []
id = 0

pickuppositions = [Position(x, y)
                   for x in range(1, world.size[0])
                   for y in range(1, world.size[1])
                   if (Position(x, y) not in world.obstacles and (y != 6 or y != 12))]

deliverpositions = [Position(x, y)
                    for x in [0, world.size[0]]
                    for y in range(0, world.size[1] + 1)]

while len(tasks) < ntasks:
    pos1 = random.choice(pickuppositions)
    pos2 = random.choice(deliverpositions)

    dist = distance(pos1, pos2)

    if dist > 2:
        # print(pos1, pos2, dist)

        pickuppositions.remove(pos1)
        deliverpositions.remove(pos2)

        tasks.append(Task(id, pos1, pos2))
        id += 1


# Generate random agents
nagents = 30
agents = []
id = 0

startpositions = [Position(x, y)
                  for x in [0, world.size[0]]
                  for y in range(0, world.size[1] + 1)]

while len(agents) < nagents:
    start = random.choice(startpositions)
    startpositions.remove(start)
    agents.append(Agent(id, start))
    id += 1

json.dumps({"agents": [agent.to_json() for agent in agents],
            "tasks": [task.to_json() for task in tasks]})
