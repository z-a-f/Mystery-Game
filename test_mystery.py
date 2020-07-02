from mystery_game.world import World
from mystery_game.color import Color
from mystery_game.movement import Direction, attach_UDLR_to_tags

world = World(10, 10)

world.add_vwall(9, 10, -5)
world.add_vwall(1, 3, 3)
world.add_vwall(3, 0, 7)
world.add_hwall(10, 9, -5)
world.add_hwall(3, 1, 3)
world.add_hwall(0, 3, 7)

red_box = world.add_box((0, 0), Color.R)
green_box = world.add_box((4, 4), Color.G)
diamond = world.add_diamond((5, 4), Color.M)


# DEBUG WALLS
for row in range(world.rows):
  for col in range(world.cols):
    num = row * world.cols + col
    row_p = row * world.kPointsPerGrid + (world.kPointsPerGrid // 2)
    col_p = col * world.kPointsPerGrid + (world.kPointsPerGrid // 2)
    world.canvas.create_text(row_p, col_p, text=f'({row}, {col})', fill='black')

cells = []
for row in range(world.rows):
  for col in range(world.cols):
    cells.append((row, col))

for cell1 in cells:
  cell1_row = cell1[0] * world.kPointsPerGrid + (world.kPointsPerGrid // 2)
  cell1_col = cell1[1] * world.kPointsPerGrid + (world.kPointsPerGrid // 2)
  for cell2 in cells:
    cell2_row = cell2[0] * world.kPointsPerGrid + (world.kPointsPerGrid // 2)
    cell2_col = cell2[1] * world.kPointsPerGrid + (world.kPointsPerGrid // 2)
    try:
      if world.is_vwall_between(cell1, cell2):
        world.canvas.create_line((cell1_row, cell1_col), (cell2_row, cell2_col), width=3, fill='red')
    except:
      pass
    try:
      if world.is_hwall_between(cell1, cell2):
        world.canvas.create_line((cell1_row, cell1_col), (cell2_row, cell2_col), width=3, fill='blue')
    except:
      pass
    try:
      if world.adjacent_cells_walled(cell1, cell2):
        world.canvas.create_line((cell1_row, cell1_col), (cell2_row, cell2_col), fill='green')
    except:
      pass
# END DEBUG WALLS

attach_UDLR_to_tags(world, [diamond, green_box], [5, 2, 1, 3])
# attach_UDLR_to_tags(world, ['box_G'], [5, 2, 1, 3])

world.mainloop()
