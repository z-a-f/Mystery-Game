from .color import Color

def __header(world, cell, color, tag, tag_prefix):
  assert cell[0] >= 0 and cell[0] < world.rows
  assert cell[1] >= 0 and cell[1] < world.cols

  if isinstance(color, Color):
    tag_suffix = color.name
    color = color.to_hash()
  else:
    tag_suffix = color
  if tag is None:
      tag = tag_prefix + tag_suffix

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
  world.objects[tag] = ('box', color_obj, cell)
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
  world.objects[tag] = ('diamond', color_obj, cell)
  return tag

def _circle(world, cell, color_obj, offset_in, tag):
  tag, color = __header(world, cell, color_obj, tag, 'circle_')

  top_left = cell[0] * world.kPointsPerGrid, cell[1] * world.kPointsPerGrid
  bottom_right = top_left[0] + world.kPointsPerGrid, top_left[1] + world.kPointsPerGrid
  top_left = [ tl + offset_in for tl in top_left ]
  bottom_right = [br - offset_in for br in bottom_right ]

  idd = world.canvas.create_oval(top_left, bottom_right, fill=color,
                                 tags=('circle', tag))
  world.objects[tag] = ('circle', color_obj, cell)
  return tag
