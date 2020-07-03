import random
import tkinter as tk

from .color import Color
from ._env_object_defs import _box, _circle, _diamond
from ._env_tag_defs import _move, _teleport
from ._env_wall_defs import _wall, _vwall, _hwall
from ._env_wall_defs import _adjacent_cells_walled
from ._env_wall_defs import _is_hwall_between, _is_vwall_between


class World(tk.Tk):
  """Class for the world.

  Class members:
    kPointsPerGrid: Number of points per grid width/height
    kWindowTitle: Title of the Tk window

  Instance members:
    rows: Number of rows in the grid
    cols: Number of columns in the grid
    height: Canvas height in points
    width: Canvas width in points
    canvas: Tk.Canvas object

    score: Current score

    vwalls: All vertical wall objects (Tk widgets)
    hwalls: All horizontal wall objects (Tk widgets)
    objects: All non-wall objects (Tk widgets).
             Currently these are supported:
             - Boxes (with tag 'box')
             - Diamonds (with tag 'diamond')
             - Circles (with tag 'circle')

    num_boxes: Number of colored boxes added to the world.
               Currently updated using the `randomize` method only
    agent_name: Tag of the agent that was added to this world
    target_name: Tag of the target that was added to this world
  """
  kPointsPerGrid = 100
  kWindowTitle = 'Mystery Game'

  def __init__(self, h, w, bg='white'):
    """Entry point for the world generation.

    Args:
      h, w: Height and width of the canvas in number of cells
      bg: Background colorof the canvas
    """
    super(World, self).__init__()
    self.rows = w
    self.cols = h
    self.height = self.cols * self.kPointsPerGrid
    self.width = self.rows * self.kPointsPerGrid
    self.canvas = tk.Canvas(self, height=self.height, width=self.width, bg=bg)
    self.canvas.pack(fill=tk.BOTH, expand=True)
    self.canvas.bind('<Configure>', self._create_grid)
    self.resizable(0, 0)
    self.score = 0
    self.update_score(0)

    self.vwalls = set()
    self.hwalls = set()

    # Save map from key -> (id, object type, cell location)
    self.objects = dict()

    self.num_boxes = None
    self.agent_name = None
    self.target_name = None

  def _create_grid(self, event=None):
    self.canvas.delete('grid_line') # Will only remove the grid_line

    # Creates all vertical lines at intevals of 100
    for i in range(0, self.width, self.kPointsPerGrid):
        self.canvas.create_line([(i, 0), (i, self.height)], tag='grid_line')

    # Creates all horizontal lines at intevals of 100
    for i in range(0, self.height, self.kPointsPerGrid):
        self.canvas.create_line([(0, i), (self.width, i)], tag='grid_line')

  def update_score(self, value):
    """Sets the score in the title"""
    self.score += value
    self.winfo_toplevel().title(f'{self.kWindowTitle}... Score: {self.score}')

  def clear_canvas(self):
    """Clears the canvase (except grid) and resets the `self.objects`."""
    for tag in self.objects.keys():
      self.canvas.delete(tag)
    self.objects = {}
    self.num_boxes = 0

  def randomize(self, num_boxes=4, agent_name=None, target_name=None):
    """Randomizes the current game.

    TODO: Add wall randomization

    Args:
      num_boxes: Number of boxes to add.
                 Must be < total number of cells in the grid - 2
      agent_name: Tag to give to the agent (diamond shape)
      target_name: Tag to give to the target (circle shape)
    """
    self.clear_canvas()
    if (num_boxes + 2) > (self.rows * self.cols):
      raise ValueError(f'Cannot initialize game with {num_boxes} boxes in a ' \
                       f'grid of size {self.rows} x {self.cols}')
    if num_boxes > len(Color):
      raise ValueError(f'Cannot create {num_boxes} boxes, as I only have '\
                       f'{len(Color)} colors')
    if agent_name is not None:
      self.agent_name = agent_name
    if target_name is not None:
      self.target_name = target_name
    positions = list(range(self.rows * self.cols))
    colors = list(Color)
    random.shuffle(positions)
    for idx in range(num_boxes):
      row = positions[idx] // self.cols
      col = positions[idx] % self.cols
      self.add_box((row, col), colors[idx])
    # Agent
    row = positions[num_boxes] // self.cols
    col = positions[num_boxes] % self.cols
    self.add_diamond((row, col), 'gray', offset_in=5, tag=self.agent_name)
    # Target
    row = positions[num_boxes+1] // self.cols
    col = positions[num_boxes+1] % self.cols

    target_color_idx = random.randint(0, num_boxes-1)
    self.add_circle((row, col), colors[target_color_idx], offset_in=25,
                    tag=self.target_name)
    self.num_boxes = num_boxes

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

  def add_vwall(self, row, col, length):
    """Adds a vertical wall given the starting column and row, and the length.

    Note: The length can be negative
    """
    return _vwall(self, row, col, length)

  def add_hwall(self, row, col, length):
    """Adds a horizontal wall given the starting column and row, and the length.

    Note: The length can be negative
    """
    return _hwall(self, row, col, length)

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

  def add_circle(self, cell, color_obj, offset_in=5, tag=None):
    return _circle(self, cell, color_obj, offset_in, tag)

  def move(self, tag, direction):
    """Moves an object given its tag by one cell in a specified direction."""
    return _move(self, tag, direction)

  def teleport(self, tag, new_cell):
    """Moves an object given its tag to a specific cell."""
    return _teleport(self, tag, new_cell)
