class Cell(object):
  """Environment cell.

  This cell doesn't have information about its location.
  Information it contains:

  - walls: set of directions where the passage is not allowed
  - objects: set of IMMOVABLE objects that are located IN the cell.
             Note these objects SHOULD NOT be movable
  - targets: set of MOVABLE objects that are located in the cell.
             Noe these objects are movable

  Note that the agents are not in the cell, but rather in the world environment.
  That means the agents can interact with the cells by taking them as objects.
  """
  kNumDirections = 4

  def __init__(self):
    self.walls = set()
    self.objects = set()
    self.targets = set()

  def __repr__(self):
    walls = ', '.join([ f'{key.name}'  for key in self.walls ])
    s = f'Cell<walls: ({walls}), objects: {self.objects}>'
    return s

  def add_object(self, *objs):
    for o in objs:
      self.objects.add(o)

  def remove_object(self, obj):
    raise RuntimeError(f'Cannot move an immovable object {obj}!')

  def clear_objects(self):
    self.objects = set()

  def add_target(self, *tgts):
    for t in tgts:
      self.targets.add(t)

  def remove_target(self, tgt):
    self.targets.remove(tgt)

  def clear_targets(self):
    self.targets = set()

  def set_wall(self, *directions):
    for d in directions:
      self.walls.add(d)

  def can_move(self, *direction):
    if len(direction) == 0:
      return len(self.walls) != self.kNumDirections
    if len(direction) == 1:
      return direction[0] not in self.walls
    for dr in direction:
      if not self.can_move(dr):
        return False
    return True
