import collections as ct

par = 2

class edgeDict(dict):
    def __missing__(self, key):
       return list()

def cat_clark_subdivision(ob):
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
      ed = face_edge_map[key]
      ind = ed.index
      edge_dict[ind].append(count)

  n_old_verts = len(verts)
  n_faces = len(faces)


  # Builds V:{E}
  vert_dict = ct.defaultdict(list)
  for count, e in enumerate(edges):
    for key in e.vertices:
      vert_dict[key].append(count)

  # Builds V:{F}
  vert_dict_faces = ct.defaultdict(list)
  for count, f in enumerate(faces):
    for key in f.vertices:
        vert_dict_faces[key].append(count)

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
    c1 = n_old_verts + edge_dict[e.index][0]
    c2 = n_old_verts + edge_dict[e.index][1]
    x = (par*v1[0] + par*v2[0] + new_verts[c1][0] + new_verts[c2][0])
    y = (par*v1[1] + par*v2[1] + new_verts[c1][1] + new_verts[c2][1])
    z = (par*v1[2] + par*v2[2] + new_verts[c1][2] + new_verts[c2][2])
    n = 2 + 2 * par
    new_vertex = (x/n, y/n, z/n)
    new_verts.append(new_vertex)

  for count, f in enumerate(faces):
    center_idx = n_old_verts + count
    for v in f.vertices:
      edges_of_face = []
      for e in f.edge_keys:
        if v in e:
          ed = face_edge_map[e]
          edges_of_face.append(ed.index)

      edge_mid1_idx = n_old_verts + n_faces +  edges_of_face[0]
      edge_mid2_idx = n_old_verts + n_faces +  edges_of_face[1]

      fx = 0
      fy = 0
      fz = 0
      # Computes centroid of adjacent faces
      for fa in vert_dict_faces[v]:
        fx += new_verts[n_old_verts + fa][0]
        fy += new_verts[n_old_verts + fa][1]
        fz += new_verts[n_old_verts + fa][2]
      l = len(vert_dict_faces[v])
      F = (fx/l, fy/l, fz/l)

      rx = 0
      ry = 0
      rz = 0
      # Computes centroid of edge midpoints
      for ed in vert_dict[v]:
        rx += new_verts[n_old_verts + n_faces + ed][0]
        ry += new_verts[n_old_verts + n_faces + ed][1]
        rz += new_verts[n_old_verts + n_faces + ed][2]
      lr = len(vert_dict[v])
      R = (rx/lr, ry/lr, rz/lr)
      nvx = (F[0] + 2*R[0] + (par*lr - 3)*verts[v].co[0])/(par*lr) 
      nvy = (F[1] + 2*R[1] + (par*lr - 3)*verts[v].co[1])/(par*lr) 
      nvz = (F[2] + 2*R[2] + (par*lr - 3)*verts[v].co[2])/(par*lr) 
      nv = (nvx, nvy, nvz)

      new_verts[v] = nv
      new_face = (v, edge_mid2_idx, center_idx, edge_mid1_idx)
      new_faces.append(new_face)
  return new_verts, new_faces
      

def e_f_dict(ob):
  edge_dict = edgeDict()
  for count, p in enumerate(ob.data.polygons):
    for key in p.edge_keys:
      edge_dict[key].append(count)
  return edge_dict