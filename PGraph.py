import networkx as nx
import random

class ProbabilityGraph:

    #G = nx.Graph()

    #Constructor for random dense graph(v,e) G.
    def __init__(self, graph = None):
        if graph == None:
            self.G = nx.dense_gnm_random_graph(100, 140)
        else:
            self.G = graph
        a = 0
        for node in list(self.G.nodes):
            random.seed(a)
            probability = random.uniform(0, 1)
            self.G.nodes[node]['probability'] = probability
            a = a + 1
        a = 0
        for edge in list(self.G.edges):
            random.seed(a)
            probability = random.uniform(0, 1)
            self.G.edges[edge]['probability'] = probability
            a = a + 1

    # Converts a treenode from the search tree(clique) to a graph item.
    # Our clique is a list of vertices.

    def converts_clique_to_subgraph(self, clique):
        subg = self.G.subgraph(clique)
        return subg

    def clique_prob_lemma2(self,graph):
        Pe = 1
        Pv = 1
        for node in graph.nodes(data = True):
            if node[1]:
                nodeP = node[1]['probability']
                Pv = Pv * nodeP
        for edge in graph.edges(data = True):
            Pe = Pe * edge[2]['probability']
        return Pv * Pe