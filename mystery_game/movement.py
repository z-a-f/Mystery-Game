from enum import Enum

class Direction(Enum):
  N = (0, -1)
  S = (0, +1)
  E = (+1, 0)
  W = (-1, 0)

def attach_movement_to_tags(world, tags, movekey, direction):
  def callback(event):
    for tag in tags:
      world.move(tag, direction)
  world.bind(movekey, callback)

def attach_wasd_to_tags(world, tags):
  key_maps = [
    ('w', Direction.N),
    ('s', Direction.S),
    ('a', Direction.W),
    ('d', Direction.E)
  ]
  for key, direction in key_maps:
    attach_movement_to_tags(world, tags, key, direction)

def attach_UDLR_to_tags(world, tags, udlr_keys):
  assert len(udlr_keys) == 4
  directions = [
    Direction.N,
    Direction.S,
    Direction.W,
    Direction.E
  ]
  for idx in range(4):
    key = str(udlr_keys[idx])
    attach_movement_to_tags(world, tags, key, directions[idx])
    if len(key) == 1 and key.isnumeric():
      key = '<KP_' + key + '>'
      attach_movement_to_tags(world, tags, key, directions[idx])
