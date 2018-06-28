// backtick  v
var source = `

#these lines comes from tmp.py


"""
Force Directed Layout
Based on http://patrickfuller.github.io/jgraph/examples/ipython.html

Generates network coordinates using a force-directed layout.
tweaked for rapydsript compatibility, TBD: and for incremental layout
"""
from vpython import *

def uniform(a,b):
    range=b-a
    return(a + (random()*range) )

def oKeys(o):
    return [k for k in o]

def oValues(o):
    return [o[k] for k in o]

def oItems(o):
    return list(zip(oKeys(o), oValues(o)))

def IDsFromEdges(edges):
    IDs=[]
    for t in edges:
        IDs.append(str(t['source']))
        IDs.append(str(t['target']))
    return list(set(IDs))

def combinations( iter='ABCD', len=2 ):  # ONLY works for len=2!
    combos = [ ]
    for i in iter:
        for j in iter:
            if i != j:
                if (i, j) not in combos:
                    if (j, i) not in combos:
                        combos.append( (i, j) )
    return combos


def run(params):
    edges =         params['edges']
    iterations =    params['iterations']
    updateNodes=    params['updateNodes']
    is_3D =         params['is_3D']
    dampening =     params['dampening']
    force_strength= params['force_strength']
    max_velocity  = params['max_velocity']
    max_distance  = params['max_distance']

    global nodes

    """Runs a force-directed-layout algorithm on the input graph.

    iterations - Number of FDL iterations to run in coordinate generation
    force_strength - Strength of Coulomb and Hooke forces
                     (edit this to scale the distance between nodes)
    dampening - Multiplier to reduce force applied to nodes
    max_velocity - Maximum distance a node can move in one step
    max_distance - The maximum distance considered for interactions
    """

    nodeIDs = IDsFromEdges(edges)

    #fix edge.size to eliminate #get below
    for i, edge in enumerate(edges):
        if not ('size' in oKeys(edge)):  #(parens around boolean mandatory in RS)
            edges[i]['size']=1
    # Convert to a data-storing object and initialize size
    d = 3 if is_3D else 2

    newDict={}
    for n in nodeIDs:
        newDict[n]={'velocity': [0.0, 0.0, 0.0], 'force': [0.0, 0.0, 0.0]}  #changed JS
    nodes = newDict

    # Repeat n times (is there a more Pythonic way to do this?)
    for i in range (iterations):
        # Add in Coulomb-esque node-node repulsive forces
        for node1, node2 in combinations( oValues(nodes), 2):
            _coulomb(node1, node2, force_strength, max_distance)

         # And Hooke-esque edge spring forces
        for edge in edges:
            _hooke(nodes[edge['source']], nodes[edge['target']],
                   force_strength * edge['size'], max_distance)
                   #force_strength * edge.get('size', 1), max_distance)

        for key, node in oItems(nodes):
            force = [_constrain(dampening * f, -max_velocity, max_velocity)
                     for f in node['force']]
            node['velocity'] = [v + dv
                                for v, dv in zip(node['velocity'], force)]
            node['force'] = [0.0, 0.0, 0.0]
            if not is_3D:
                node['velocity'][2]=0.0

        if updateNodes:
            scene.waitfor("redraw")
            updateNodes(nodes)

    # Clean and return at end
    for node in oValues(nodes):
        del node['force']
        node['location'] = node['velocity']
        del node['velocity']
        # Even if it's 2D, let's specify three dimensions
        if not is_3D:
            node['location'].append(0.0)
    return nodes


def _coulomb(n1, n2, k, r):
    """Calculates Coulomb forces and updates node data."""
    # Get relevant positional data
    delta = [x2 - x1 for x1, x2 in zip(n1['velocity'], n2['velocity'])]
    distance = sqrt(sum([d * d for d in delta]))

    # If the deltas are too small, use random values to keep things moving
    if distance < 0.1:
        delta = [uniform(0.1, 0.2) for i in range(3)]
        distance = sqrt(sum([d ** 2 for d in delta]))

    # If the distance isn't huge (ie. Coulomb is negligible), calculate
    if distance < r:
        force = (k / distance) ** 2
        n1['force'] = [f - force * d for f, d in zip(n1['force'], delta)]
        n2['force'] = [f + force * d for f, d in zip(n2['force'], delta)]
    #print('cc', n1['force'])

def _hooke(n1, n2, k, r):  #k and r are undefined!!!!
    """Calculates Hooke spring forces and updates node data."""
    # Get relevant positional data
    delta = [x2 - x1 for x1, x2 in zip(n1['velocity'], n2['velocity'])]
    distance = sqrt(sum([d ** 2 for d in delta]))

    # If the deltas are too small, use random values to keep things moving
    if distance < 0.1:
        delta = [uniform(0.1, 0.2) for i in range(3)]
        distance = sqrt(sum([d ** 2 for d in delta]))

    # Truncate distance so as to not have crazy springiness
    distance = min(distance, r)

    # Calculate Hooke force and update nodes
    force = (distance ** 2 - k ** 2) / (distance * k)

    n1['force'] = [f + force * d for f, d in zip(n1['force'], delta)]
    n2['force'] = [f - force * d for f, d in zip(n2['force'], delta)]

    #print('xx', n1['force'])

def _constrain(value, min_value, max_value):
    """Constrains a value to the inputted range."""
    return max(min_value, min(value, max_value))

def showNodes(nodes): #this is a proxy for updating
    for k, node in oItems(nodes):
        print(k, node['velocity']) #actually x,y,z

if __name__ == '__main__':

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
    print('printing from glowscript')


`
//backtick
