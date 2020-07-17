from mystery_rewrite.cell import Cell
from mystery_rewrite.direction import Direction

from mystery_rewrite._utils import List

class World(object):
  def __init__(self, rows, cols):
    self.rows = rows
    self.cols = cols

    self.cells = List(
      [ [ Cell() for _ in range(self.cols) ] for _ in range(self.rows) ])

    # In order to avoid costly world search, we use a dict with the locations.
    # Maps object to location.
    # Location could be the agent as well.
    self.targets = dict()
    self.objects = dict()

  def __getitem__(self, idx):
    if isinstance(idx, tuple) and len(idx) == 1:
      idx = (idx[0] // self.cols, idx[0] % self.cols)
    return self.cells[idx]

  def __repr__(self):
    s = f'World<target #: {len(self.targets)}, object #: {len(self.objects)}'
    s += f'cells:\n'
    for cell in self.cells.flat:
      s += str(cell) + '\n'
    return s

  #######
  # Walls
  def add_hwall(self, row, start_col, end_col, loc='both'):
    assert loc in ['both', Direction.N, Direction.S]
    if loc == 'both':
      self.add_hwall(row, start_col, end_col, loc=Direction.N)
      self.add_hwall(row, start_col, end_col, loc=Direction.S)
      return

    if row < 0:
      row = self.rows + row
    if start_col < 0:
      start_col = self.cols + start_col
    if end_col < 0:
      end_col = self.cols + end_col
    if start_col > end_col:
      start_col, end_col = end_col, start_col
    end_col = min(end_col, self.cols)

    for col in range(start_col, end_col + 1):
      self.cells[row, col].set_wall(loc)

  def add_vwall(self, start_row, end_row, col, loc='both'):
    assert loc in ['both', Direction.E, Direction.W]
    if loc == 'both':
      self.add_vwall(start_row, end_row, col, loc=Direction.W)
      self.add_vwall(start_row, end_row, col, loc=Direction.E)
      return

    if col < 0:
      col = self.cols + col
    if start_row < 0:
      start_row = self.rows + start_row
    if end_row < 0:
      end_row = self.rows + end_row
    if start_row > end_row:
      start_row, end_row = end_row, start_row
    end_row = min(end_row, self.rows)

    for row in range(start_row, end_row + 1):
      self.cells[row, col].set_wall(loc)

  def add_enclosure(self):
    self.add_hwall(0, 0, -1, loc=Direction.N)
    self.add_hwall(-1, 0, -1, loc=Direction.S)
    self.add_vwall(0, -1, 0, loc=Direction.E)
    self.add_vwall(0, -1, -1, loc=Direction.W)

  #################
  # Movable objects
  def add_target(self, row, col, *target):
    """Adds a target to the cell and to the targets dict"""
    self.cells[row, col].add_target(*target)
    for t in target:
      self.targets[t] = (row, col)

  def has_target(self, row, col, tgt):
    return tgt in self.cells[row, col].targets

  def remove_target(self, target):
    """Removes the target from the targets dicts and from the cell"""
    row, col = self.targets.pop(target)
    self.cells[row, col].remove_target(target)

  def pop_targets(self, row, col):
    """Takes all the targets from the cells"""
    tgts = list(self.cells[row, col].targets)
    self.cells[row, col].clear_objects()
    return tgts

  ###################
  # Immovable objects
  def add_object(self, row, col, *obj):
    """Adds an object to a cell"""
    self.cells[row, col].add_object(*obj)
    for o in obj:
      self.objects[o] = (row, col)
