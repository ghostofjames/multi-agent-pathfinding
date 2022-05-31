from simulation import Simulation

MAP = 'configs/small-15x13-narrow.json'

# 'configs/small-14x14.json'
# 'configs/medium-26x14.json'
# 'configs/large-38x20.json'
# 'configs/small-15x13-narrow.json'
# 'configs/medium-27x13-narrow.json'
# 'configs/large-51x25-narrow.json'

print("4 agents")

a = Simulation(config=MAP, algorithm='CA*', nagents=4, thread=False)
a.run()

a = Simulation(config=MAP, algorithm='HCA*', nagents=4, thread=False)
a.run()

print("8 agents")

a = Simulation(config=MAP, algorithm='CA*', nagents=8, thread=False)
a.run()

a = Simulation(config=MAP, algorithm='HCA*', nagents=8, thread=False)
a.run()

print("12 agents")

a = Simulation(config=MAP, algorithm='CA*', nagents=12, thread=False)
a.run()

a = Simulation(config=MAP, algorithm='HCA*', nagents=12, thread=False)
a.run()


# # Large Warehouse

# print("16 agents")

# a = Simulation(config='configs/large-38x20.json', algorithm='CA*', nagents=16, thread=False)
# a.run()

# a = Simulation(config='configs/large-38x20.json', algorithm='HCA*', nagents=16, thread=False)
# a.run()

# print("20 agents")

# a = Simulation(config='configs/large-38x20.json', algorithm='CA*', nagents=20, thread=False)
# a.run()

# a = Simulation(config='configs/large-38x20.json', algorithm='HCA*', nagents=20, thread=False)
# a.run()

# print("24 agents")

# a = Simulation(config='configs/large-38x20.json', algorithm='CA*', nagents=24, thread=False)
# a.run()

# a = Simulation(config='configs/large-38x20.json', algorithm='HCA*', nagents=24, thread=False)
# a.run()
