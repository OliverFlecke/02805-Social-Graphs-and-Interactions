from networkx import Graph

def nodesWithGivenAttribute(G: Graph, attribute: str, value: str) -> dict:
    '''Find all the nodes from a given party

    @param G: networkx graph to look in
    @param attribute: used to group the nodes
    @param value: to filter all the nodes with
    @returns: A dictionary of nodes with their attributes
    '''
    return { x: G.node[x] for x in G.nodes() if G.node[x][attribute] == value }

def totalDegree(G: Graph, nodes: dict) -> int:
    '''Calculates the sum of all the degrees of the nodes

    @returns: The total degree of all the nodes
    '''
    return sum([G.degree(x) for x in nodes.keys()])

def totalNumberOfLinksWithinCommunity(G: Graph, nodes: dict) -> int:
    '''Find the total number of links within a community

    @param G: networkx graph to look in
    @param attribute: to group the community
    @param nodes: The community of nodes
    @returns: The number of links within a community
    '''
    return len([other
        for node in nodes
            for other in G.neighbors(node)
                if other in nodes
    ]) / 2

def modularityStats(G: Graph, nodes: dict) -> (float, float, float):
    '''Get the relevant constants for calculating modularity stats

    @param G: networkx graph to look in
    @param attribute: used to group the community
    @param party: to define the community

    @returns: (k_c, L_c, L)
    '''
    return (
        totalDegree(G, nodes)
        , totalNumberOfLinksWithinCommunity(G, nodes)
        , len(G.edges())
    )

def modularity(G: Graph, nodes: dict) -> float:
    '''Calculate the modularity of a community of nodes given the party

    @param G: networkx graph to look in
    @param party: The party that defines the community
    @returns: The modularity of the nodes in the graph with the given party
    '''
    k_c, L_c, L = modularityStats(G, nodes)

    M_c = L_c / L - (k_c / (2 * L))**2

    return M_c