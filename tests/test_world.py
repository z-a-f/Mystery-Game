import unittest

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from mystery_rewrite import world
from mystery_rewrite.direction import Direction

class _WorldTest(unittest.TestCase):
  def setUp(self):
    self.ROWS = 3
    self.COLS = 4
    self.world = world.World(self.ROWS, self.COLS)

class WorldTest(_WorldTest):
  def test_constructor(self):
    self.assertEqual(self.ROWS, len(self.world.cells))
    self.assertEqual(self.COLS, len(self.world.cells[0]))

    self.assertEqual(0, len(self.world.targets))
    self.assertEqual(0, len(self.world.objects))

class WorldWallsTest(_WorldTest):
  def test_add_a_wall_at_a_time(self):
    for row in range(self.ROWS):
      for col in range(self.COLS):
        self.world.add_hwall(row, col, col, loc='both')
        self.world.add_vwall(row, row, col, loc='both')
        self.assertFalse(self.world[row, col].can_move())

  def test_add_row_wall(self):
    row = 1
    self.world.add_hwall(row, 0, -1, loc='both')

    for col in range(0, self.COLS):
      self.assertTrue(self.world[row, col].can_move())
      self.assertFalse(self.world[row, col].can_move(Direction.N, Direction.S))

  def test_add_col_wall(self):
    col = 1
    self.world.add_vwall(0, -1, col, loc='both')

    for row in range(0, self.ROWS):
      self.assertTrue(self.world[row, col].can_move())
      self.assertFalse(self.world[row, col].can_move(Direction.E, Direction.W))

class WorldObjectTest(_WorldTest):
  def test_add_object(self):
    for row in range(self.ROWS):
      for col in range(self.COLS):
        objects_to_add = [ object() for _ in range(3) ]
        self.world.add_object(row, col, *objects_to_add)
        self.assertEqual(len(objects_to_add), len(self.world[row, col].objects))

        for idx in range(len(objects_to_add)):
          self.assertTrue(objects_to_add[idx] in self.world[row, col].objects)
          self.assertEqual((row, col), self.world.objects[objects_to_add[idx]])

  def test_add_target(self):
    for row in range(self.ROWS):
      for col in range(self.COLS):
        targets_to_add = [ object() for _ in range(3) ]
        self.world.add_target(row, col, *targets_to_add)
        self.assertEqual(len(targets_to_add), len(self.world[row, col].targets))

        for idx in range(len(targets_to_add)):
          self.assertTrue(targets_to_add[idx] in self.world[row, col].targets)
          self.assertEqual((row, col), self.world.targets[targets_to_add[idx]])

  def test_pop_target(self):
    row, col = 0, 1
    targets = self.world.pop_targets(row, col)
    self.assertEqual(0, len(targets))

    targets_to_add = [ object() for _ in range(3) ]
    self.world.add_target(row, col, *targets_to_add)

    targets = self.world.pop_targets(row, col)
    self.assertEqual(len(targets_to_add), len(targets))

  def test_remove_target(self):
    row, col = 0, 1
    targets_to_add = [ object() for _ in range(3) ]
    self.world.add_target(row, col, *targets_to_add)

    self.world.remove_target(targets_to_add[0])
    self.assertEqual(len(targets_to_add)-1, len(self.world.targets))


if __name__ == '__main__':
  unittest.main()
