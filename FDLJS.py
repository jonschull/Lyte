#!/usr/bin/env python3

"""
Force Directed Layout JS (JS=Jon Schull)
(Based on jgraph for python.)

Generates network coordinates using a force-directed layout.
(tweaked for rapydsript compatibility, TBD: and for incremental layout)
"""

import makemyPYJ

from random import uniform
from math import sqrt
#from itertools import  repeat

def combinations( iter='ABCD', len=2 ):  # ONLY works for len=2!  #NOW INLINE
    combos = [ ]
    for i in iter:
        for j in iter:
            if i != j:
                if (i, j) not in combos:
                    if (j, i) not in combos:
                        combos.append( (i, j) )
    return combos



def run(edges, iterations=10, force_strength=5.0, dampening=0.01,
        max_velocity=2.0, max_distance=50, is_3d=True):
    """Runs a force-directed-layout algorithm on the input graph.

    iterations - Number of FDL iterations to run in coordinate generation
    force_strength - Strength of Coulomb and Hooke forces
                     (edit this to scale the distance between nodes)
    dampening - Multiplier to reduce force applied to nodes
    max_velocity - Maximum distance a node can move in one step
    max_distance - The maximum distance considered for interactions
    """

    # Get a list of node ids from the edge data
    nodes = set(e['source'] for e in edges) | set(e['target'] for e in edges)

    # Convert to a data-storing object and initialize some values
    d = 3 if is_3d else 2

    ######## this doesn't work in rapydscript
    #nodes = {n: {'velocity': [0.0] * d, 'force': [0.0] * d} for n in nodes}
    ####### therefore....
    newDict=dict()
    for n in nodes:
        newDict[n]={'velocity': [0.0] * d, 'force': [0.0] * d} 
    nodes = newDict
    ####### tadum!
    
    
    # Repeat n times (is there a more Pythonic way to do this?)
    for i in range (iterations):

        # Add in Coulomb-esque node-node repulsive forces
        for node1, node2 in combinations(nodes.values(), 2):
            _coulomb(node1, node2, force_strength, max_distance)

        # And Hooke-esque edge spring forces
        for edge in edges:
            _hooke(nodes[edge['source']], nodes[edge['target']],
                   force_strength * edge.get('size', 1), max_distance)

        # Move by resultant force
        
        for key, node in nodes.items():
            # Constrain the force to the bounds specified by input parameter
            force = [_constrain(dampening * f, -max_velocity, max_velocity)
                     for f in node['force']]
            # Update velocities and reset force
            node['velocity'] = [v + dv
                                for v, dv in zip(node['velocity'], force)]
            node['force'] = [0] * d
            print('=====', key, node['velocity'])
            
        #print(nodes)

    # Clean and return
    for node in nodes.values():
        del node['force']
        node['location'] = node['velocity']
        del node['velocity']
        # Even if it's 2D, let's specify three dimensions
        if not is_3d:
            node['location'] += [0.0]
    return nodes


def _coulomb(n1, n2, k, r):
    """Calculates Coulomb forces and updates node data."""
    # Get relevant positional data
    delta = [x2 - x1 for x1, x2 in zip(n1['velocity'], n2['velocity'])]
    distance = sqrt(sum(d ** 2 for d in delta))

    # If the deltas are too small, use random values to keep things moving
    if distance < 0.1:
        delta = [uniform(0.1, 0.2) for i in range(3)]
        distance = sqrt(sum(d ** 2 for d in delta))

    # If the distance isn't huge (ie. Coulomb is negligible), calculate
    if distance < r:
        force = (k / distance) ** 2
        n1['force'] = [f - force * d for f, d in zip(n1['force'], delta)]
        n2['force'] = [f + force * d for f, d in zip(n2['force'], delta)]


def _hooke(n1, n2, k, r):
    """Calculates Hooke spring forces and updates node data."""
    # Get relevant positional data
    delta = [x2 - x1 for x1, x2 in zip(n1['velocity'], n2['velocity'])]
    distance = sqrt(sum(d ** 2 for d in delta))

    # If the deltas are too small, use random values to keep things moving
    if distance < 0.1:
        delta = [uniform(0.1, 0.2) for i in range(3)]
        distance = sqrt(sum(d ** 2 for d in delta))

    # Truncate distance so as to not have crazy springiness
    distance = min(distance, r)

    # Calculate Hooke force and update nodes
    force = (distance ** 2 - k ** 2) / (distance * k)
    n1['force'] = [f + force * d for f, d in zip(n1['force'], delta)]
    n2['force'] = [f - force * d for f, d in zip(n2['force'], delta)]


def _constrain(value, min_value, max_value):
    """Constrains a value to the inputted range."""
    return max(min_value, min(value, max_value))


if __name__ == '__main__':

    edges=[(1,2),(2,3), (3,1)]

    # Convert to internal representation
    edges = [{'source': str(s), 'target': str(t)} for s, t in edges]

    # Handle additional args
    kwargs = {'force_strength': 5.0, 'is_3d': True}
##    for i, arg in enumerate(sys.argv):
##        if arg == '--force-strength':
##            kwargs['force_strength'] = float(sys.argv[i + 1])
##        elif arg == '--2D':
##            kwargs['is_3d'] = False

    # Generate nodes
    nodes = run(edges, **kwargs)
    
    #nodes = AttrThing(nodes)
    print(nodes)
    
    # Convert to json and print
    #print(json_formatter.dumps({'edges': edges, 'nodes': nodes}))
