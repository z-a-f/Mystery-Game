import unittest

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from mystery_rewrite import cell
from mystery_rewrite.direction import Direction

class CellTest(unittest.TestCase):
  def setUp(self):
    self.cell = cell.Cell()

  def test_walls(self):
    wall_directions = (Direction.N, Direction.W)
    no_wall_directions = (Direction.S, Direction.E)

    self.assertEqual(0, len(self.cell.walls))

    self.cell.set_wall(*wall_directions)
    self.assertEqual(len(wall_directions), len(self.cell.walls))

    for d in wall_directions:
      self.assertTrue(d in self.cell.walls)
      self.assertFalse(self.cell.can_move(d))
    for d in no_wall_directions:
      self.assertFalse(d in self.cell.walls)
      self.assertTrue(self.cell.can_move(d))

  def test_object(self):
    self.assertEqual(0, len(self.cell.objects))
    self.cell.add_object(object(), object(), object())
    self.assertEqual(3, len(self.cell.objects))
    with self.assertRaises(RuntimeError):
      self.cell.remove_object(object())

  def test_target(self):
    # Initially empty
    self.assertEqual(0, len(self.cell.targets))
    objects = [ object() for _ in range(3) ]
    # Adding many targets
    self.cell.add_target(*objects)
    self.assertEqual(len(objects), len(self.cell.targets))
    # Removing a single target
    self.assertTrue(objects[0] in self.cell.targets)
    self.cell.remove_target(objects[0])
    self.assertEqual(len(objects)-1, len(self.cell.targets))
    self.assertFalse(objects[0] in self.cell.targets)

if __name__ == '__main__':
  unittest.main()
