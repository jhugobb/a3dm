import bpy
import mathutils
import sys
import os
import imp

from time import time

import ex1
import ex2

def r(a):
    return int(a*1000+0.5)/1000.0

def createObj(verts, faces):
  me = bpy.data.meshes.new("DivMesh") 
  ob = bpy.data.objects.new("DivObj", me) 
  ob.location = bpy.context.scene.cursor_location 
  bpy.context.scene.objects.link(ob)
    
  me.from_pydata(verts, [], faces)
  me.update(calc_edges=True)

  # Recalculate normals
  bpy.context.scene.objects.active = ob
  bpy.ops.object.mode_set(mode='EDIT')
  bpy.ops.mesh.select_all(action='SELECT')
  bpy.ops.mesh.normals_make_consistent(inside=False)
  bpy.ops.object.editmode_toggle()

def main():

    ob = bpy.data.scenes['Scene'].objects.active

    t = time()
    verts, faces = ex2.cat_clark_subdivision(ob)
    createObj(verts, faces)
    print("Script took %6.2f secs.\n\n"%(time()-t)) 

    