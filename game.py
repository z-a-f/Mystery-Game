from mystery_game.agent import Agent
from mystery_game.world import World
from mystery_game.color import Color
from mystery_game.movement import Direction, attach_UDLR_to_tags

# world = World(6, 6)
# world.add_vwall(1, 0, 3)
# world.add_hwall(4, 5, -2)

world = World(4, 4)

agent_name = 'agent'
target_name = 'target'

world.randomize(4, agent_name, target_name)
agent = Agent(world)

world.mainloop()
