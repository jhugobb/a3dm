import bpy
import mathutils
import sys
import os
import imp

from time import time

import ex1
import ex2
import ex3

def r(a):
    return int(a*1000+0.5)/1000.0

def createObj(verts, faces):
  bpy.ops.object.delete()
  me = bpy.data.meshes.new("DivMesh") 
  ob = bpy.data.objects.new("DivObj", me) 
  ob.location = bpy.context.scene.cursor_location 
  bpy.context.scene.objects.link(ob)
    
  me.from_pydata(verts, [], faces)
  me.update(calc_edges=True)
  # bpy.data.objects["Subdiv1"].select = True
  # bpy.context.scene.objects.active = bpy.data.objects["DivObj"]
  # ob.select = True

  # Recalculate normals
  bpy.ops.object.mode_set(mode='EDIT')
  bpy.ops.mesh.select_all(action='SELECT')
  bpy.ops.mesh.normals_make_consistent(inside=False)
  bpy.ops.object.editmode_toggle()
  bpy.ops.object.mode_set(mode='OBJECT')

  print("hey")

def createNotRenderedObj(verts, faces):
  me = bpy.data.meshes.new("DivMeshtemp") 
  ob = bpy.data.objects.new("DivObjtemp", me)
  me.from_pydata(verts, [], faces)
  me.update(calc_edges=True)
  return ob

def subdivide(ob, n):
  ob_simple = ob
  ob_cat_clark = ob
  for i in range(n):
    verts_simple, faces_simple = ex1.simple_subdivision(ob_simple)
    verts_cat_clark, faces_cat_clark = ex2.cat_clark_subdivision(ob_cat_clark)
    ob_simple = createNotRenderedObj(verts_simple, faces_simple)
    ob_cat_clark = createNotRenderedObj(verts_cat_clark, faces_cat_clark)
  return verts_simple, verts_cat_clark, faces_simple

def main(n = 2):

    ob = bpy.data.scenes['Scene'].objects.active
    location = ob.location
    # If we are in edit mode
    bpy.ops.object.mode_set(mode='OBJECT')

    t = time()
    verts_simple, verts_cat_clark, faces_simple = subdivide(ob, n)

    def interpolation(t):
      res_verts = ex3.step(verts_simple, verts_cat_clark, t)
      bpy.ops.object.delete()
      me = bpy.data.meshes.new("DivMesh") 
      ob = bpy.data.objects.new("DivObj", me) 
      ob.location = location
      bpy.context.scene.objects.link(ob)
        
      me.from_pydata(res_verts, [], faces_simple)
      me.update(calc_edges=True)
      bpy.data.objects["DivObj"].select = True
      bpy.context.scene.objects.active = bpy.data.objects["DivObj"]
      ob.select = True

      # Recalculate normals
      bpy.ops.object.mode_set(mode='EDIT')
      bpy.ops.mesh.select_all(action='SELECT')
      bpy.ops.mesh.normals_make_consistent(inside=False)
      bpy.ops.object.mode_set(mode='OBJECT')

    def Callback(scene):
      start = scene.frame_start
      end = scene.frame_end
      num = end-start
      frame = scene.frame_current
      step = float(frame-start)/num
      interpolation(step)

    bpy.data.scenes['Scene'].frame_end=100
    bpy.data.scenes['Scene'].frame_current=0

    bpy.app.handlers.frame_change_pre.clear()
    bpy.app.handlers.frame_change_pre.append(Callback)
      
    print("Script took %6.2f secs.\n\n"%(time()-t)) 

    