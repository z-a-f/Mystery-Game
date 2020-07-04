from .color import Color
from .direction import Direction

class Cell(object):
  def __init__(self, row=None, col=None, boxes=None, walls=None,
               has_agent=False, has_target=False):
    # Current row and column are optional
    self.row = row
    self.col = col
    # Boxes are saved as a set of colors
    self.boxes = set() if boxes is None else set(boxes)
    # Walls are saved as a list of bools representing [N, S, W, E]
    self.walls = [ False * 4 ] if walls is None else list(walls)
    self._agent = has_agent
    self._target = has_target

  def add_box(self, box_color):
    assert isinstance(box_color, Color), 'Expecting Color object'
    if box_color in self.boxes:
      return False
    else:
      self.boxes.add(box_color)
      return True

  def remove_box(self, box_color):
    if box_color in self.boxes:
      self.boxes.remove(box_color)
      return True
    else:
      return False

  def add_wall(self, d):
    assert isinstance(d, Direction), 'Expecting Direction object'
    for idx, direction in enumerate([Direction.N,
                                     Direction.S,
                                     Direction.W,
                                     Direction.E]):
      if d is direction:
        self.walls[idx] = True
        break

  @property
  def agent(self):
    return self._agent
  @agent.setter
  def agent(self, agent_here):
    self._agent = agent_here

  @property
  def target(self):
    return self._target
  @target.setter
  def target(self, target_here):
    self._target = target_here
