import networkx as nx
import matplotlib.pyplot as plt

# First undirected graph
G = nx.Graph()
G.add_nodes_from(range(1, 6))

G.add_edge(1, 2)
G.add_edge(1, 3)
G.add_edge(1, 4)
G.add_edge(1, 6)

G.add_edge(2, 3)
G.add_edge(2, 4)

G.add_edge(3, 6)

# Second directed graph
H = nx.DiGraph()
H.add_nodes_from(G)
H.add_edge(1, 2)

H.add_edge(2, 3)
H.add_edge(2, 4)

H.add_edge(3, 1)
H.add_edge(3, 2)

H.add_edge(4, 1)

H.add_edge(6, 1)
H.add_edge(6, 3)


plt.subplot(121)
nx.draw(G, with_labels=True, font_weight='bold')

plt.subplot(122)
options = {
    'node_color': 'blue'
}
nx.draw(H, with_labels=True, font_weight='bold', **options)
plt.show()
