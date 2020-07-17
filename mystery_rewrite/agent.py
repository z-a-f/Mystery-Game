
class Agent(object):
  """Agent to interact with the world"""
  def __init__(self, world, start_row, start_col):
    self.world = world
    self.row = start_row
    self.col = start_col

    self.holding = None

  def move(self, row, col):
    # if row < 0 or row >= self.world.rows or col < 0 or col >= self.world.cols:
    #   raise ValueError(f'Cannot move to coordinates ({row}, {col})')
    if row < 0:
      row += self.world.rows
    if col < 0:
      col += self.world.cols
    self.row = row % self.world.rows
    self.col = col % self.world.cols

    self.row = row
    self.col = col

  def step(self, direction):
    if not self.world[self.row, self.col].can_move(direction):
      return False
    row = self.row + direction.value[0]
    col = self.col + direction.value[1]
    self.move(row, col)

    return True

  def look(self, distance=0):
    """Looks at the cells around itself, and returns the contents.

    The contents are represented as a list:
    [C, N1, E1, S1, W1, N2, E2, S2, W2, ...]
    where C represents the currently occupied cell.
    The N*, E*, S*, and W* are the cells of an appropriate direction, and the
    * represents the distance.

    If a wall is preventing, it will be a None

    Args:
      distance: Distance to look around

    Returns:
      movable: List of movable objects
      immovable: List of immovable objects
    """
    seen_cells = [self.world[self.row, self.col]]
    can_move_to = set(Direction.N, Direction.S, Direction.E, Direction.W)
    for idx in range(distance):
      for d in [Distance.N, Distance.E, Distance.S, Distance.W]:
        row, col = d.value
        row += self.row + row * d
        col += self.col + col * d
        adjacent_cell = self.world[row, col]
        if adjacent_cell.can_move(-d) and (d in can_move_to):
          seen_cells.append(adjacent_cell)
        else:
          seen_cells.append(None)
          can_move_to.remove(d)

    movable = []
    immovable = []
    for cell in seen_cells:
      if cell is None:
        movable.append(cell)
        immovable.append(cell)
      else:
        movable.append(cell.targets)
        immovable.append(cell.objects)

    return movable, immovable

  def grab(self, *obj):
    if self.holding is not None:
      return False

    if len(obj) == 0:
      self.holding = self.world.pop_targets(self.row, self.col)
    else:
      changed = False
      for o in obj:
        if self.world.has_target(self.row, self.col, o):
          if self.holding is None:
            self.holding = []
          self.holding.append(o)
          self.world.remove_target(o)
          changed = True
    return changed

