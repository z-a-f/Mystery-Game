
from .color import Color

class Target(object):
  def __init__(self, color):
    self.color = color

  def __eq__(self, other):
    if isinstance(other, Color):
      return self.color == other
    return self.color == other.color
