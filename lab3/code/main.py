import bpy
import mathutils
import sys
import os
import imp

from time import time

import ex1
import ex2
import ex7
import ex8

def r(a):
    return int(a*1000+0.5)/1000.0

# Creates an object and reorients its normals coherently
def createObj(verts, faces):
  prev = bpy.data.scenes['Scene'].objects.active
  me = bpy.data.meshes.new("DivMesh") 
  ob = bpy.data.objects.new("DivObj", me) 
  ob.location = bpy.context.scene.cursor_location 
  bpy.context.scene.objects.link(ob)
    
  me.from_pydata(verts, [], faces)
  me.update(calc_edges=True)

  # Recalculate normals
  bpy.context.scene.objects.active = ob
  bpy.ops.object.mode_set(mode='EDIT')
  bpy.ops.mesh.normals_make_consistent(inside=False)
  bpy.ops.object.mode_set(mode='OBJECT')
  bpy.context.scene.objects.active = prev
  
  return ob

# Used to have a mesh to process as a middle step
def createNotRenderedObj(verts, faces):
  me = bpy.data.meshes.new("Meshtemp") 
  ob = bpy.data.objects.new("Objtemp", me)
  me.from_pydata(verts, [], faces)
  me.update(calc_edges=True)
  return ob

# Receives:
#       · the number of the exercise to run
#       · The number of times to subdivide the selected object
#       · The list of edges marked as creases (for ex8)
def main(arg = 7, n = 1, creases = []):

    ob = bpy.data.scenes['Scene'].objects.active
    if not ob:
      print("An object must be selected")
      return

    t = time()
    if arg == 1:
      for i in range(n):
        verts, faces = ex1.simple_subdivision(ob)
        ob = createNotRenderedObj(verts, faces)
    elif arg == 2:
      for i in range(n):
        verts, faces = ex2.cat_clark_subdivision(ob)
        ob = createNotRenderedObj(verts, faces)
    elif arg == 7:
      for i in range(n):
        verts, faces = ex7.cat_clark_subdivision(ob)
        ob = createNotRenderedObj(verts, faces)
    elif arg == 8:
      for i in range(n):
        verts, faces, creased = ex8.cat_clark_creases(ob, creases)
        ob = createNotRenderedObj(verts, faces)
        creases = ex8.get_crease_index(ob, creased)
    else: print("This version is not supported")
    
    if verts != [] and faces != []:
      new_ob = createObj(verts, faces)

    print("Script took %6.2f secs.\n\n"%(time()-t)) 

    