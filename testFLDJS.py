from FDLJS import run
#IRS scam? 2023350440

from vpython import sphere
from vpython import vector as V
from attrthing import AttrThing, gimme

#import makemyVPHTML

edges=[(1,2),(2,3), (3,1), (3,4), (4,5), (4,6), (5,6)]

def IDsFromEdges(edges):
    IDs=[]
    for t in edges:
        IDs.append(str(t[0]))
        IDs.append(str(t[1]))
    return set(IDs)

spheres=AttrThing()
IDs = IDsFromEdges(edges)
for ID in IDs:
    spheres[ID] = sphere()

def updateSpheres(nodes):
    global spheres,k,v
    for k,v in nodes.items():
        x,y,z = v['velocity']
        #print('--', k, spheres[k])
        spheres[str(k)].pos = V(x,y,z)

#Convert to internal representation
edges = [AttrThing(source = str(s), target = str(t)) for s, t in edges]

# Generate nodes
nodes = run(edges, iterations= 3000, updateNodes= updateSpheres, is_3d=False)