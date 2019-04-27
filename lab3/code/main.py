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

def createNotRenderedObj(verts, faces):
  me = bpy.data.meshes.new("Meshtemp") 
  ob = bpy.data.objects.new("Objtemp", me)
  me.from_pydata(verts, [], faces)
  me.update(calc_edges=True)
  return ob

def main(arg = 7, creases = [], n = 1):

    ob = bpy.data.scenes['Scene'].objects.active
    t = time()
    if arg == 1:
      verts, faces = ex1.simple_subdivision(ob)
    elif arg == 2:
      verts, faces = ex2.cat_clark_subdivision(ob)
    elif arg == 7:
      verts, faces = ex7.cat_clark_subdivision(ob)
    elif arg == 8:
      for i in range(n):
        verts, faces, creased = ex8.cat_clark_creases(ob, creases)
        ob = createNotRenderedObj(verts, faces)
        creases = ex8.get_crease_index(ob, creased)
      
    new_ob = createObj(verts, faces)

    print("Script took %6.2f secs.\n\n"%(time()-t)) 

    