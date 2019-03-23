import bpy
import mathutils
import sys
import os
import imp

from time import time


dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )
    print(sys.path)

import ex6
import ex7

import ex9

imp.reload(ex6)
imp.reload(ex7)
imp.reload(ex9)

def r(a):
    return int(a*1000+0.5)/1000.0

def main():

    ob = bpy.data.scenes['Scene'].objects.active

    #Ex6 needed for 7
    t = time()
    s, polygons = ex6.calShells(ob)
    print ("Object has %d shells"%r(s))
    print("Script took %6.2f secs.\n\n"%(time()-t)) 

    #Ex7 
    t = time()
    g = r(ex7.eulerEQShells(s, ob))
    print("Object has genus %d"%g)
    print("Script took %6.2f secs.\n\n"%(time()-t)) 

    #Ex9
    t = time()
    vol = r(ex9.volume(ob, polygons))
    print("Object has volume %6.2f"%vol)
    print("Script took %6.2f secs.\n\n"%(time()-t)) 

    