
lfrom PPGSOincrementallayout import *

def getIDs(edges):
    IDs=[]
    for t in edges:
        IDs.append(str(t[0]))
        IDs.append(str(t[1]))
    return set(IDs)


edges=[(1,2),(2,3), (3,1), (3,4), (4,5), (4,6), (5,6), (6,7), (7,8),(8,9),(9,6)]

spheres={}
IDs = getIDs(edges)
for ID in IDs:
    spheres[ID] = sphere(color=color.yellow)

def updateSpheres(nodes):
    for k,v in oItems(nodes):
        x,y,z = v['velocity']
        spheres[str(k)].pos = vector(x,y,z)

#Convert to internal representation
edges = [{'source' : str(s), 'target' : str(t)} for s, t in edges]

# Generate nodes
params={'edges':edges,
        'iterations'    : 100,
        'updateNodes'   : updateSpheres,
        'is_3D'         : False,
        'force_strength': 5.0,
        'dampening'     : 0.01,
        'max_velocity'  : 2.0,
        'max_distance'  : 50}


nodes = run(params)
