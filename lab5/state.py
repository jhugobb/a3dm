import instantiate
import operator

class state(object):
  def __init__(self):
    self.size_stack = [(0,0,0)]
    self.translation_stack = [(0,0,0)]
    self.rotation_stack = [(0,0,0)]

  def push_state(self):
    self.size_stack.append(self.size_stack[len(self.size_stack)-1])
    self.rotation_stack.append((0,0,0))
    self.translation_stack.append((0,0,0))

  def pop_state(self):
    self.size_stack.pop()
    self.translation_stack.pop()
    self.rotation_stack.pop()

  def translate(self, translation):
    curr = self.translation_stack[len(self.translation_stack)-1]
    new = tuple(map(operator.add, curr, translation))
    self.translation_stack[len(self.translation_stack)-1] = new
  
  def rotate(self, rotation):
    curr = self.rotation_stack[len(self.rotation_stack)-1]
    new = tuple(map(operator.add, curr, rotation))
    self.rotation_stack[len(self.rotation_stack)-1] = new

  def scale(self, scale):
    self.size_stack[len(self.size_stack)-1] = scale

  def instantiate(self, idobj):
    t = self.translation_stack[len(self.translation_stack)-1]
    s = self.size_stack[len(self.size_stack)-1]
    r = self.rotation_stack[len(self.rotation_stack)-1]
    instantiate.I(idobj, t, s, r)