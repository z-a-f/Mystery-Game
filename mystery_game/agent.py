from .movement import Direction, attach_UDLR_to_tags
from ._env_tag_defs import tags_in_cell

class Agent(object):
  def __init__(self, world, rewards=None):
    self.world = world
    self.name = self.world.agent_name
    self.target = self.world.target_name

    self.movement_tags = set([self.name])
    self.has_target = False

    if rewards is None:
      # [Move, pick_up, drop_on_wrong, drop_on_right]
      rewards = {
        'move': -1,
        'pick_target': 1,
        'pick_no_target': -1,
        'drop_target_no_win': 0,
        'drop_target_win': 10,
        'drop_no_target': -1,
        'wrong_action': 0
      }
    self.reward = rewards

    for key in range(10):
      self.setup_callback(key)

  def setup_callback(self, key):
    def callback(event):
      for tag in list(self.movement_tags):
        self.action(tag, key)
    key = str(key)
    self.world.bind(key, callback)
    self.world.bind(f'<KP_{key}>', callback)

  def check_if_over(self):
    if self.has_target:
      return False
    target_info = self.world.objects[self.target]
    box_name = f'box_{target_info[1].name}'
    box_location = tuple(self.world.objects[box_name][2])
    return box_location == tuple(target_info[2])

  def action(self, tag, value):
    won = False
    value = int(value)
    if value == 1:
      self.world.move(tag, Direction.W)
      reward = self.reward['move']
    elif value == 2:
      self.world.move(tag, Direction.S)
      reward = self.reward['move']
    elif value == 3:
      self.world.move(tag, Direction.E)
      reward = self.reward['move']
    elif value == 5:
      self.world.move(tag, Direction.N)
      reward = self.reward['move']
    elif value == 4:
      try:
        agent_location = tuple(self.world.objects[self.name][2])
        target_location = tuple(self.world.objects[self.target][2])
      except:
        print(self.world.objects)
      if agent_location == target_location:
        self.movement_tags.add(self.target)
        self.has_target = True
        reward = self.reward['pick_target']
      else:
        reward = self.reward['pick_no_target']
    elif value == 6:
      if self.has_target:
        self.movement_tags.remove(self.target)
        self.has_target = False
        if self.check_if_over():
          reward = self.reward['drop_target_win']
          won = True
        else:
          reward = self.reward['drop_target_no_win']
      else:
        reward = self.reward['drop_no_target']
    else:
      reward = self.reward['wrong_action']
    self.world.update_score(reward)
    if won:
      self.world.randomize()
    return reward