from enum import Enum

class Color(Enum):
  R = 0xe53935
  G = 0x43a047
  B = 0x1e88e5
  Y = 0xfdd835
  C = 0x00bcd4
  M = 0xea80fc
  # Aliases
  RED = 0xe53935
  GREEN = 0x43a047
  BLUE = 0x1e88e5
  YELLOW = 0xfdd835
  CYAN = 0x00bcd4
  MAGENTA = 0xea80fc

  def to_hash(self):
    return f'#{hex(self.value)[2:]:0>6}'
