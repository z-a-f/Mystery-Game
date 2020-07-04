from mystery_game.world import World
from mystery_game.color import Color
from mystery_game.agent import Agent
from mystery_game.direction import Direction
from mystery_game.movement import attach_UDLR_to_tags

world = World(10, 10)

# Order matters => must be Box->Diamond->Circle
red_box = world.add_box((0, 0), Color.R)
green_box = world.add_box((4, 4), Color.G)
circle = world.add_circle((6, 6), Color.R, offset_in=20)

world.mainloop()
