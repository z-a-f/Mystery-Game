import tkinter as tk

from ._env_object_defs import _box, _diamond
from ._env_tag_defs import _move, _teleport
from ._env_wall_defs import _wall, _vwall, _hwall
from ._env_wall_defs import _adjacent_cells_walled
from ._env_wall_defs import _is_hwall_between, _is_vwall_between


class World(tk.Tk):
  kPointsPerGrid = 100

  def __init__(self, h, w, bg='white'):
    super(World, self).__init__()
    self.rows = w
    self.cols = h
    self.height = self.cols * self.kPointsPerGrid
    self.width = self.rows * self.kPointsPerGrid
    self.canvas = tk.Canvas(self, height=self.height, width=self.width, bg=bg)
    self.canvas.pack(fill=tk.BOTH, expand=True)
    self.canvas.bind('<Configure>', self._create_grid)
    self.resizable(0, 0)

    self.vwalls = set()
    self.hwalls = set()

    # Save map from key -> (id, object type, cell location)
    self.objects = dict()

  def _create_grid(self, event=None):
    self.canvas.delete('grid_line') # Will only remove the grid_line

    # Creates all vertical lines at intevals of 100
    for i in range(0, self.width, self.kPointsPerGrid):
        self.canvas.create_line([(i, 0), (i, self.height)], tag='grid_line')

    # Creates all horizontal lines at intevals of 100
    for i in range(0, self.height, self.kPointsPerGrid):
        self.canvas.create_line([(0, i), (self.width, i)], tag='grid_line')

  def add_wall(self, start_row, end_row, start_col, end_col):
    """Adds a wall given start and end coordinates.

    Note: The locations must be the coordinates of the walls.
    For example here are the wall coordinates

        0    1    2    3
      0 +----+----+----+
        |    |    |    |
      1 +----+----+----+
        |    |    |    |
      2 +----+----+----+
        |    |    |    |
      3 +----+----+----+
        |    |    |    |
      4 +----+----+----+
    """
    return _wall(self, start_row, end_row, start_col, end_col)

  def add_vwall(self, col, row, length):
    """Adds a vertical wall given the starting column and row, and the length.

    Note: The length can be negative
    """
    return _vwall(self, col, row, length)

  def add_hwall(self, col, row, length):
    """Adds a horizontal wall given the starting column and row, and the length.

    Note: The length can be negative
    """
    return _hwall(self, col, row, length)

  def adjacent_cells_walled(self, cell1, cell2):
    """Checks if there is a wall between two cells."""
    return _adjacent_cells_walled(self, cell1, cell2)

  def is_hwall_between(self, cell1, cell2):
    """Checks if there is a horizontal wall between two cells."""
    return _is_hwall_between(self, cell1, cell2)

  def is_vwall_between(self, cell1, cell2):
    """Checks if there is a vertical wall between two cells."""
    return _is_vwall_between(self, cell1, cell2)

  def add_box(self, cell, color_obj, offset_in=5, tag=None):
    """Adds a box into a cell."""
    return _box(self, cell, color_obj, offset_in, tag)

  def add_diamond(self, cell, color_obj, offset_in=5, tag=None):
    """Adds a diamond into a cell"""
    return _diamond(self, cell, color_obj, offset_in, tag)

  def move(self, tag, direction):
    """Moves an object given its tag by one cell in a specified direction."""
    return _move(self, tag, direction)

  def teleport(self, tag, new_cell):
    """Moves an object given its tag to a specific cell."""
    return _teleport(self, tag, new_cell)
