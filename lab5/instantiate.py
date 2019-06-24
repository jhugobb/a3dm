import bpy
import operator

def I(objid, translation, scale, rotation):
  translation = tuple(map(operator.add, translation, (0, 0, scale[2])))
  if objid == "cube":
    bpy.ops.mesh.primitive_cube_add(location = translation, rotation = rotation)
    bpy.ops.transform.resize(value=scale)
  elif objid == "cylinder":
    bpy.ops.mesh.primitive_cylinder_add(location=translation, rotation = rotation)
    bpy.ops.transform.resize(value=scale)

