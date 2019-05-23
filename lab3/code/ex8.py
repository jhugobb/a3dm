import collections as ct

# For ex4
par = 1.2

def cat_clark_creases(ob, creases):
  new_faces = []
  new_verts = []
  creased = []
  
  verts = ob.data.vertices
  edges = ob.data.edges
  faces = ob.data.polygons
  edge_keys = ob.data.edge_keys
  # Builds a map that can take face edge keys and return edge indexes
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
  
  # Create face vertices 
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

  # Create edge vertices
  for e in edges:
    v1 = verts[e.vertices[0]].co
    v2 = verts[e.vertices[1]].co

    x = (par*v1[0] + par*v2[0])
    y = (par*v1[1] + par*v2[1])
    z = (par*v1[2] + par*v2[2])
    if e.index not in creases:
      for i in edge_dict[e.index]:
        c = n_old_verts + i
        x += new_verts[c][0]
        y += new_verts[c][1]
        z += new_verts[c][2]
      n = len(edge_dict[e.index]) + 2 * par
    else:
      n = 2 * par
    new_vertex = (x/n, y/n, z/n)
    new_verts.append(new_vertex)
    if e.index in creases:
      creased.append(new_vertex)

  # Define faces
  for count, f in enumerate(faces):
    center_idx = n_old_verts + count
    for v in f.vertices:
      edges_of_face = []

      # Checks to see if the vertex belongs to a crease
      cr = False
      for e in vert_dict[v]:
        if e in creases:
          cr = True
          break

      for e in f.edge_keys:
        if v in e:
          ed = face_edge_map[e]
          edges_of_face.append(ed.index)

      edge_mid1_idx = n_old_verts + n_faces +  edges_of_face[0]
      edge_mid2_idx = n_old_verts + n_faces +  edges_of_face[1]

      if not cr:
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
      if cr and new_verts[v] not in creased: creased.append(new_verts[v])
      new_faces.append(new_face)
  return new_verts, new_faces, creased
      
# Receives an object and a set of vertices that belong to parent crease edges
# Returns the list of edge indexes that are childs of crease parents
def get_crease_index(ob, creased_verts):
  verts = ob.data.vertices
  edges = ob.data.edges
  res = []

  # Handles numeric errors of calculating midpoints
  cr_verts = []
  for v2 in verts:
    for v in creased_verts:
      if (abs(v[0]-v2.co[0]) < 0.05 and abs(v[1]-v2.co[1]) < 0.05 and abs(v[2]-v2.co[2]) < 0.05):
        cr_verts.append(v2.co)

  # Finds edges that contain both vertices in the list of crease vertices
  for e in edges:
    is_crease = True
    for v in e.vertices:
      if verts[v].co not in cr_verts:
        is_crease = False
    if is_crease: res.append(e.index)
  
  return res