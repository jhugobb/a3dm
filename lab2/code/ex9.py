def volume(ob, polygons):
    result = 0
    for i in range(len(polygons)): #Generalised for any kind of mesh
        if polygons[i].manyfold: #We only want those polygons belonging to a manyfold shell
            el = ob.data.polygons[i]
            nverts = len(el.vertices)
            vX = [()] * nverts
            normalX = el.normal[0]
            sx = el.area * normalX
            for i in range(nverts):
                index = el.vertices[i]
                vX[i] = ob.data.vertices[index].co[0]
            result += sx * sum(vX) * (1/nverts)
    return result