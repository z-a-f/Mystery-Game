"""Definitions for manipulating the tags."""

from .direction import Direction

def _move(world, tag, direction):
  current_cell = world.objects.get(tag, None)
  if current_cell is None:
    raise ValueError(f'Cannot find tag "{tag}"')
  idd, obj, current_cell = current_cell

  if isinstance(direction, Direction):
    direction = direction.value
  dx, dy = direction

  next_cell = []
  for idx in range(0, len(current_cell), 2):
    next_cell.append(current_cell[idx] + dx)
    next_cell.append(current_cell[idx+1] + dy)
  if next_cell[0] < 0.0 or next_cell[0] >= world.rows:
    return False
  if next_cell[1] < 0.0 or next_cell[1] >= world.cols:
    return False
  if world.adjacent_cells_walled(current_cell, next_cell):
    return False

  world.objects[tag] = idd, obj, next_cell

  # Need to work with object point coordinates, not the cell cooredinates.
  dx *= world.kPointsPerGrid
  dy *= world.kPointsPerGrid
  crd = world.canvas.coords(tag)
  new_crd = []
  for idx in range(0, len(crd), 2):
    new_crd.append(crd[idx] + dx)
    new_crd.append(crd[idx + 1] + dy)

  world.canvas.coords(tag, new_crd)
  return True

def _teleport(world, tag, new_cell):
  current_cell = world.objects.get(tag, None)
  if current_cell is None:
    raise ValueError(f'Cannot find tag "{tag}"')
  idd, obj, current_cell = current_cell

  if new_cell[0] < 0 or new_cell[1] < 0:
    return False
  if new_cell[0] >= world.rows or new_cell[1] >= world.cols:
    return False
  updated_cell = [ c * world.kPointsPerGrid for c in new_cell ]
  world.canvas.coords(tag, updated_cell)
  world.objects[tag] = idd, obj, new_cell
  return True

def tags_in_cell(world, cell):
  top = cell[1] * world.kPointsPerGrid
  left = cell[0] * world.kPointsPerGrid
  bottom = top + world.kPointsPerGrid
  right = left + world.kPointsPerGrid

  ids = world.canvas.find_enclosed(left, top, right, bottom)
  tags = [ world.canvas.gettags(i) for i in ids ]
  return tags
