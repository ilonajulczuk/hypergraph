import networkx as nx
from matplotlib import pyplot as plt


def draw_bipartite_graph(G, group_1, group_2):
    pos = {x: (0, float(i % 20) * 2) for i, x in enumerate(group_1)}
    pos.update({node: (18.3, 0 + float(i % 20) * 2) for i,
                node in enumerate(group_2)})

    plt.figure()
    nx.draw(G, pos, node_color='m', node_size=800,
            with_labels=True, width=1.3, alpha=0.4)


def hipergraph_to_bipartite_parts(G):
    group_1 = (node for node in G.nodes() if not isinstance(node, tuple))
    group_2 = (node for node in G.nodes() if isinstance(node, tuple))
    return group_1, group_2



