
def _wall(world, start_row, end_row, start_col, end_col, width=5,
              tag='wall'):
  assert (start_row == end_row) or (start_col == end_col), \
         'Only horizontal or vertical lines are allowed.'
  assert (start_row >= 0) and (start_col >= 0), \
         'Starting row/col must be >= 0'
  assert (end_row <= world.rows) and (end_col <= world.cols), \
         'Ending row/col must be <= the total rows/cols'

  # (x0, y0, x1, y1), ...
  if start_col == end_col:
    wall_list = world.vwalls
  elif start_row == end_row:
    wall_list = world.hwalls
  wall_list.add((start_col, start_row, end_col, end_row))

  start_row *= world.kPointsPerGrid
  end_row *= world.kPointsPerGrid
  start_col *= world.kPointsPerGrid
  end_col *= world.kPointsPerGrid

  return world.canvas.create_line([(start_col, start_row), (end_col, end_row)],
                                  width=width, tags=tag)

def _vwall(world, col, row, length):
  start_row = row
  start_col = col
  end_row = start_row + length
  end_col = start_col

  if start_row < end_row:  # In case of negative length
    start_row, end_row = end_row, start_row

  if end_row > world.rows:
    end_row = world.rows

  return world.add_wall(start_row, end_row, start_col, end_col)

def _hwall(world, col, row, length):
  start_row = row
  start_col = col
  end_row = start_row
  end_col = start_col + length

  if start_col < end_col:  # In case of negative length
    start_col, end_col = end_col, start_col

  if end_col > world.cols:
    end_col = world.cols

  return world.add_wall(start_row, end_row, start_col, end_col)

def _adjacent_cells_walled(world, cell1, cell2):
  if (cell1[0] == cell2[0]) and (cell1[1] == cell2[1]):
    return False  # Same cell not walled
  assert (cell1[0] == cell2[0]) or (cell1[1] == cell2[1]), \
         'Cells must be adjacent to check if walled'

  if cell1[0] == cell2[0]:  # Vertical adjacency, check horizontal lines
    return world.is_hwall_between(cell1, cell2)
  else:  # Horizontal adjacency, check vertical lines
    return world.is_vwall_between(cell1, cell2)

def _is_hwall_between(world, cell1, cell2):
  if cell1[1] > cell2[1]:
    cell1, cell2 = cell2, cell1
  assert cell1[0] == cell2[0], 'Cells are not vertically adjacent'
  assert cell1[1] + 1 == cell2[1], 'Cells are not vertically adjacent'
  for wall in world.hwalls:
    if wall[1] != cell2[1]:
      continue
    if wall[0] <= cell1[0] < wall[2]:
      return True
    if wall[2] <= cell1[0] < wall[0]:
      return True
  return False

def _is_vwall_between(world, cell1, cell2):
  if cell1[0] > cell2[0]:
    cell1, cell2 = cell2, cell1
  assert cell1[1] == cell2[1], 'Cells are not horizontally adjacent'
  assert cell1[0] + 1 == cell2[0], 'Cells are not horizontally adjacent'
  for wall in world.vwalls:
    if wall[0] != cell2[0]:
      continue
    if wall[1] <= cell1[1] < wall[3]:
      return True
    if wall[3] <= cell1[1] < wall[1]:
      return True
  return False
