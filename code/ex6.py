#Auxiliary dict classes with default value
class edgeDict(dict):
    def __missing__(self, key):
       return 0

class unionDict(dict):
    def __missing__(self, key):
       return False

#Union find algorithm
def union_find(collection):
    collection = map(set, collection)
    unions = []
    for el in collection:
        tmp = []
        for u in unions:
            if not u.isdisjoint(el):
                el = u.union(el)
            else:
                tmp.append(u)
        tmp.append(el)
        unions = tmp
    return unions

#We use this so we can add an attribute to blender read-only polygons
class obj:
    def __init__(self, value):
        self.value = value
def initSet(el): #Initialise
     el.manyfold = True #True if the element belongs to a manyfold shell

def calShells(ob):

    #Find unions 
    edges = []
    for e in ob.data.edges:
        edges.append([e.vertices[0],e.vertices[1]])
    verts_unions = union_find(edges)
    nshells = len(verts_unions)

    #Initialise structure for checking if a polygon belongs to a manyfold shell
    polygons = [()] * len(ob.data.polygons)
    for i in range(len(ob.data.polygons)):
        polygons[i] = (obj(ob.data.polygons[i]))
        initSet(polygons[i])

    #Check how many times each edge is referenced
    edge_dict = edgeDict()
    for p in ob.data.polygons:
        for key in p.edge_keys:
            edge_dict[key]+=1
    
    #Check which shells are manyfold
    not_manyfold_shell = unionDict()
    not_manyfold = set()
    for poly in ob.data.polygons:
        for key in poly.edge_keys:
            if edge_dict[key] != 2:
                not_manyfold.add(key[0])
                not_manyfold.add(key[1])
                for i in range(len(verts_unions)):
                    union = verts_unions[i]
                    if key[0] in union or key[1] in union:
                        not_manyfold_shell[i] = True

    #Mark which polygons are manyfold (used in ex9)
    for i in range(len(ob.data.polygons)):
        poly = ob.data.polygons[i]
        for vert in poly.vertices:
            for j in range(len(verts_unions)):
                union = verts_unions[j]
                if vert in union and not_manyfold_shell[j]:
                    polygons[i].manyfold = False                    
                    
    
    return nshells, polygons