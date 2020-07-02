from .color import Color

def __header(world, cell, color, tag, tag_prefix):
  assert cell[0] >= 0 and cell[0] < world.rows
  assert cell[1] >= 0 and cell[1] < world.cols

  if tag is None:
    if isinstance(color, Color):
      tag = tag_prefix + color.name
      color = color.to_hash()
    else:
      tag = tag_prefix + color

  assert tag not in world.objects.keys(), \
    f"Object with tag {tag} already exists, but tags are expected to be unique."

  return tag, color

def _box(world, cell, color_obj, offset_in, tag):
  tag, color = __header(world, cell, color_obj, tag, 'box_')

  top_left = cell[0] * world.kPointsPerGrid, cell[1] * world.kPointsPerGrid
  bottom_right = top_left[0] + world.kPointsPerGrid, top_left[1] + world.kPointsPerGrid
  top_left = [ tl + offset_in for tl in top_left ]
  bottom_right = [br - offset_in for br in bottom_right ]

  idd = world.canvas.create_rectangle(top_left, bottom_right, fill=color,
                                      tags=('box', tag))
  world.objects[tag] = (idd, color_obj, cell)
  return tag

def _diamond(world, cell, color_obj, offset_in, tag):
  tag, color = __header(world, cell, color_obj, tag, 'diamond_')

  half = world.kPointsPerGrid // 2 - offset_in
  x = cell[0] * world.kPointsPerGrid + world.kPointsPerGrid // 2
  y = cell[1] * world.kPointsPerGrid + world.kPointsPerGrid // 2
  north = (x, y - half)
  east = (x + half, y)
  south = (x, y + half)
  west = (x - half, y)

  idd = world.canvas.create_polygon(north, east, south, west, fill=color,
                                    tags=('diamond', tag))
  world.objects[tag] = (idd, color_obj, cell)
  return tag
