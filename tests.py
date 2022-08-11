# Script for running simulation tests

from simulation import Simulation

MAP = 'configs/small-15x13-narrow.json'

# 'configs/small-14x14.json'
# 'configs/medium-26x14.json'
# 'configs/large-38x20.json'
# 'configs/small-15x13-narrow.json'
# 'configs/medium-27x13-narrow.json'
# 'configs/large-51x25-narrow.json'


a = Simulation(config=MAP, algorithm='CA*', nagents=4, thread=False)
a.run()

a = Simulation(config=MAP, algorithm='HCA*', nagents=4, thread=False)
a.run()

a = Simulation(config=MAP, algorithm='CA*', nagents=4, thread=False)
a.run()

a = Simulation(config=MAP, algorithm='HCA*', nagents=4, thread=False)
a.run()
