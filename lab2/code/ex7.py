def eulerEQShells(S, ob):
    nverts = len(ob.data.vertices)
    nfaces = len(ob.data.polygons)
    nedges = len(ob.data.edges)
    R = 0
    # F + V = E + R + 2(S - G)
    # G = -(F + V - E - R)/2 + S
    return (nedges + R - nfaces - nverts)/2 + S