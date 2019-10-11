import networkx as nx
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

#
#G= nx.dense_gnm_random_graph(10,10)
#G=nx.dodecahedral_graph()
#G = nx.complete_graph(8)
#S = nx.scale_free_graph(10)
#G = nx.stochastic_graph(S,weight = 666)

'''
G=nx.Graph()

G.add_edge('a','b',weight=0.6)
G.add_edge('a','c',weight=0.2)
G.add_edge('c','d',weight=0.1)
G.add_edge('c','e',weight=0.7)
G.add_edge('c','f',weight=0.9)
G.add_edge('a','d',weight=0.3)
pos=nx.spring_layout(G)
nx.draw_networkx_edge_labels(G,pos,edge_labels=None)
nx.draw_networkx(G,pos,arrows = True ,with_labels=True)
'''

G = nx.DiGraph()
G.add_nodes_from([1])
#G.add_edges_from([(1,1),(1,2),(2,3),(3,4),(4,3),(4,4)])
G.add_edges_from([(1,1)])
#pos=nx.spring_layout(G)
#nx.draw_networkx_edge_labels(G,pos,edge_labels=None)
#nx.draw_networkx(G,pos,arrows = True ,with_labels=True)
nx.draw_networkx(G)
plt.draw()  # pyplot draw()
plt.show()


#   pos=nx.get_node_attributes(G,'pos')
#nx.draw(G,pos)
#labels = nx.get_edge_attributes(G,'weight')
#nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
#nx.draw(G)  # networkx draw()