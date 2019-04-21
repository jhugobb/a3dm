def step(verts_simple, verts_cat_clark, t):
  res_verts = []
  for i in range(len(verts_simple)):
    vx = (1-t) * verts_simple[i][0] + t * verts_cat_clark[i][0]
    vy = (1-t) * verts_simple[i][1] + t * verts_cat_clark[i][1]
    vz = (1-t) * verts_simple[i][2] + t * verts_cat_clark[i][2]
    res_verts.append((vx, vy, vz))
  return res_verts