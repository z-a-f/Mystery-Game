from enum import Enum

class Direction(Enum):
  """Directions to move to an adjacent cell.

  Every direction is a (dx, dy) pair, where dx/dy are the deltas in column/row.
  """
  N = (0, -1)
  S = (0, +1)
  E = (+1, 0)
  W = (-1, 0)

  def __neg__(self):
    """This will only works if the directions are just negative opposites."""
    row, col = self.value
    return Direction((-row, -col))
