import instantiate
import state
import operator
import copy
import random

class Ruler(object):
  state = state.state()

  def __init__(self):
    self.state = state.state()

  def parse(self, string):
    tokens = string.split(" ")

    for token in tokens:
      word = token.split("*")
      if word[0] == "e": # Terminal symbol 
        continue
      elif word[0] == "R": # Rotate
        self.R(word[1])
      elif word[0] == "S": # Size
        self.S(word[1])
      elif word[0] == "T": # Position  
        self.T(word[1])
      elif word[0] == "I": # Instantiate
        self.I(word[1])
      elif word[0] == "[": # Push state
        self.push()
      elif word[0] == "]": # Pop state
        self.pop()
      elif word[0] == "Subdiv": # Subdivision
        w = token.split("{")
        w[0] = w[0].split("*")[1]
        self.subdivide(w[0], w[1])
      elif word[0] == "lot":
        self.lot(word[1])
      elif word[0] == "sidewings":
        self.sidewings()
      elif word[0] == "sidewing":
        self.sidewing()
  
  # Basic Grammar Operations
  def R(self, string):
    rot = eval(string)
    self.state.rotate(rot)

  def T(self, string):
    trans = eval(string)
    self.state.translate(trans)
  
  def S(self, string):
    scale = eval(string)
    self.state.scale(scale)
  
  def I(self, string):
    self.state.instantiate(string)
  
  def push(self):
    self.state.push_state()
  
  def pop(self):
    self.state.pop_state()
  
  def subdivide(self, string_1, string_2):

    types = string_2.split("}")[0]
    types = types.split("|")

    params = eval(string_1)
    axis = params[0]

    abs_sum = 0
    rel_sum = 0
    for i in range(1, len(params)):
      if type(params[i]) != str:
        abs_sum += params[i]
      else:
        value = eval(params[i][0])
        rel_sum += value

    if axis == "X":
      idx = 0
    elif axis == "Y":
      idx = 1
    elif axis == "Z":
      idx = 2
    
    rot = self.state.rotation_stack[len(self.state.rotation_stack)-1]
    trans = self.state.translation_stack[len(self.state.translation_stack)-1]
    size = self.state.size_stack[len(self.state.size_stack)-1]
    for i in range(0, len(types)):

      self.push()

      value = params[i+1]

      if type(params[i+1]) == str:
        value = eval(params[i+1][0])
        value = value * (size[idx] - abs_sum) / rel_sum
      
      if idx == 0:
        trans = tuple(map(operator.add, trans, (value, 0, 0)))
        s = (value, size[1], size[2])
      elif idx == 1:
        trans = tuple(map(operator.add, trans, (0, value, 0)))
        s = (size[0], value, size[2])
      else:
        trans = tuple(map(operator.add, trans, (0, 0, value)))
        s = (size[0], size[1], value)

      self.state.rotate(rot)
      self.state.translate(trans)
      self.state.scale(s)

      self.parse(types[i])
      self.pop()
      self.state.scale(size)

  # End of Basic Grammar Operations

  #def A(self, string)


  def lot(self, string):
    size = self.state.size_stack[len(self.state.size_stack)-1]
    str_size = "S*({0},{1},".format(size[0], size[1]) + string + ") "
    str_subdiv = "Subdiv*('Y',{0},'1r')".format(size[1] * random.uniform(0.2, 0.6)) + "{I*cube|sidewings}"
    self.parse(str_size + str_subdiv)

  def sidewings(self):
    size = self.state.size_stack[len(self.state.size_stack)-1]
    str_subdiv_1 = "Subdiv*('X',{0},'1r')".format(size[0] * random.uniform(0.2, 0.6)) + "{sidewing|e} " 
    str_subdiv_2 = "Subdiv*('X','1r',{0})".format(size[1] * random.uniform(0.2, 0.6)) + "{e|sidewing}"
    self.parse(str_subdiv_1 + str_subdiv_2)

  def sidewing(self):
    random_probability = random.random()
    size = self.state.size_stack[len(self.state.size_stack)-1]
    if random_probability < 0.5:
      str_size = "S*({0},{1},{2})".format(size[0], size[1] * random.uniform(0.4, 1), size[2]) + " I*cube"
    elif random_probability < 0.8:
      str_size = "S*({0},{1},{2})".format(size[0], size[1] * random.uniform(0.4, 1), size[2] * random.uniform(0.2, 0.9)) + " I*cube"
    else: return
    self.parse(str_size)

#Example Grammar
