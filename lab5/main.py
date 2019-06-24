import bpy
import mathutils
import sys
import os
import imp

from time import time

import rules

def main(string = ""):
  
  ruler = rules.Ruler()

  ruler.parse(string)
