
"""
from: https://gist.github.com/joninvski/701720
The Bellman-Ford algorithm
Graph API:
    iter(graph) gives all nodes
    iter(graph[u]) gives neighbours of u
    graph[node][neighbour] gives weight of edge (node, neighbour)
"""

# Step 1: For each node prepare the destination and predecessor
def initialize(graph, source):
    weight = {}  # Stands for node weighting
    predecessor = {}  # Stands for predecessor
    for node in graph:
        weight[node] = float('Inf') # We start admitting that the rest of nodes are very far away
        predecessor[node] = None
    weight[source] = 0 # For the source we know how to reach
    return weight, predecessor

def retrace_negative_loop(p, start):
    arbitrageLoop = [start]
    next_node = start
    while True:
        next_node = p[next_node]
        if next_node not in arbitrageLoop:
            arbitrageLoop.append(next_node)
        else:
            arbitrageLoop.append(next_node)
            arbitrageLoop = arbitrageLoop[arbitrageLoop.index(next_node):]
            return arbitrageLoop

def relax(node, neighbour, graph, weight, predecessor):
    # If the distance between the node and the neighbour is lower than the one I have now
    if weight[neighbour] > weight[node] + graph[node][neighbour]:
        # Record this lower distance
        weight[neighbour] = weight[node] + graph[node][neighbour]
        predecessor[neighbour] = node

def bellman_ford(graph, source):
    weight, predecessor = initialize(graph, source)
    print('bellman start', weight, predecessor)
    for i in range(len(graph)-1):  # Run this until is converges
        for node in graph:
            for neighbour in graph[node]:  # For each neighbour of current node
                relax(node, neighbour, graph, weight, predecessor)  # Lets relax it

    # Step 3: check for negative-weight cycles
    for node in graph:
        for neighbour in graph[node]:
            if weight[neighbour] > weight[node] + graph[node][neighbour]:
                print('negative cycle')

    return weight, predecessor


def test():
    graph = {
        'a': {'b': -1, 'c':  4},
        'b': {'c':  3, 'd':  2, 'e':  2},
        'c': {},
        'd': {'b':  1, 'c':  5},
        'e': {'d': -3}
        }

    d, p = bellman_ford(graph, 'a')

    # 1. find node with shortest distance (arb_node)
    # 2. find arb_node as key in predecessor dict
    # 3. in predecessor follow links to starting node ("None")

    assert d == {
        'a':  0,
        'b': -1,
        'c':  2,
        'd': -2,
        'e':  1
        }

    assert p == {
        'a': None,
        'b': 'a',
        'c': 'b',
        'd': 'e',
        'e': 'b'
        }

    chain_node = sorted(d, key=d.get)[0]
    arbitrage_list = [chain_node]
    while chain_node is not None:
        arbitrage_list.append(p[chain_node])
        chain_node = p[chain_node]
    print('arbitrage list ==> ',arbitrage_list)

if __name__ == '__main__':
    test()