import argparse

from mystery_game.agent import Agent
from mystery_game.world import World
from mystery_game.color import Color
from mystery_game.movement import Direction, attach_UDLR_to_tags

def parse_args():
  def process_x_list(lst):
    if lst is None:
      return None
    result = []
    for el in lst:
      result.append(list(map(int, el.split('x'))))
    return result

  parser = argparse.ArgumentParser(
    description='Mystery Game, rules unknown, control using numbers 1-6')
  parser.add_argument('--grid-size', metavar='ROWSxCOLS', type=str, nargs=1,
                      default='4x4', help='Number of rows and columns')
  parser.add_argument(
    '--vwalls', metavar='ROWxCOLxLENGTH', default=None, nargs='*',
    help='Put a vertical wall(s) at ROW, COL, and of length LENGTH')
  parser.add_argument(
    '--hwalls', metavar='ROWxCOLxLENGTH', default=None, nargs='*',
    help='Put a horizontal wall(s) at ROW, COL, and of length LENGTH')

  args = parser.parse_args()
  args.grid_size = process_x_list(args.grid_size)[0]
  args.vwalls = process_x_list(args.vwalls)
  args.hwalls = process_x_list(args.hwalls)
  return args

def main():
  args = parse_args()

  world = World(*args.grid_size)
  if args.vwalls is not None:
    for vwall in args.vwalls:
      world.add_vwall(*vwall)
  if args.hwalls is not None:
    for hwall in args.hwalls:
      world.add_hwall(*hwall)

  agent_name = 'agent'
  target_name = 'target'

  world.randomize(4, agent_name, target_name)
  agent = Agent(world)

  world.mainloop()

if __name__ == '__main__':
  main()
