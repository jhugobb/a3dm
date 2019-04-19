import collections as ct

class edgeDict(dict):
    def __missing__(self, key):
       return list()

def simple_subdivision(ob):
  new_faces = []
  new_verts = []
  
  verts = ob.data.vertices
  edges = ob.data.edges
  faces = ob.data.polygons
  edge_keys = ob.data.edge_keys
  face_edge_map = {ek: edges[i] for i, ek in enumerate(edge_keys)}
  
  # Builds E:{F}
  edge_dict = ct.defaultdict(list)
  for count, p in enumerate(faces):
    for key in p.edge_keys:
      edge_dict[key].append(count)

  n_old_verts = len(verts)
  n_faces = len(faces)


  # Builds V:{E}
  vert_dict = ct.defaultdict(list)
  for count, e in enumerate(edges):
    for key in e.vertices:
      vert_dict[key].append(count)

  for v in verts:
    new_verts.append(v.co)

  for face in faces:
    x = 0
    y = 0
    z = 0
    for v in face.vertices:
      vertex = verts[v].co
      x += vertex[0]
      y += vertex[1]
      z += vertex[2]
    n = len(face.vertices)
    new_vertex = (x/n, y/n, z/n)
    new_verts.append(new_vertex)

  for e in edges:
    v1 = verts[e.vertices[0]].co
    v2 = verts[e.vertices[1]].co
    x = (v1[0] + v2[0])
    y = (v1[1] + v2[1])
    z = (v1[2] + v2[2])
    new_vertex = (x/2, y/2, z/2)
    new_verts.append(new_vertex)

  for count, f in enumerate(faces):
    print("This is face " + str(count))
    center_idx = n_old_verts + count
    for e in f.edge_keys:
      print("edgeface: " + str(e))
    for v in f.vertices:
      edges_of_face = []
      print("length of vert_dict: " + str(len(vert_dict[v])))
      print("vertex: " + str(v))
      for e in f.edge_keys:
        print("edge: " + str(e))
        if v in e:
          ed = face_edge_map[e]
          edges_of_face.append(ed.index)
      print("length: " + str(len(edges_of_face)))

      edge_mid1_idx = n_old_verts + n_faces +  edges_of_face[0]
      edge_mid2_idx = n_old_verts + n_faces +  edges_of_face[1]
      new_face = (v, edge_mid2_idx, center_idx, edge_mid1_idx)
      new_faces.append(new_face)
  
  return new_verts, new_faces
      

def e_f_dict(ob):
  edge_dict = edgeDict()
  for count, p in enumerate(ob.data.polygons):
    for key in p.edge_keys:
      edge_dict[key].append(count)
  return edge_dict