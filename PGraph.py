import networkx as nx
import random

class ProbabilityGraph:

    #Constructor for random dense graph(v,e) G or recieves a set graph
    def __init__(self, graph = None, v = None, e = None):
        self.G = nx.Graph()
        if graph == None:
            self.G = nx.dense_gnm_random_graph(v, e)
            self.createGraph()
        else:
            #Which mean i got an input graph which is a list with N tuples.(NodeA, NodeB, Probability).
            self.createGraphfromList(graph)

    def createGraphfromList(self, list):
        #nodeA = line[0], nodeB = line[1], probability = line[2]
        a = 0
        for line in list:
            random.seed(a)
            probability = random.uniform(0, 1)
            self.G.add_node(line[0], probability=probability)
            a = a + 1
            random.seed(a)
            probability = random.uniform(0, 1)
            self.G.add_node(line[1], probability=probability)
            probability = float(line[2])
            self.G.add_edge(line[0], line[1], probability=probability)
            a = a + 1

    def createGraph(self):
        # Filling Vertices and Edges with probabilities.
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
        Pe = 1.0
        Pv = 1.0
        for node in graph.nodes(data = True):
            if node[1]:
                nodeP = node[1]['probability']
                Pv = Pv * nodeP
        for edge in graph.edges(data = True):
            #print(type(edge[2]['probability']))
            Pe = Pe * edge[2]['probability']
        return Pv * Pe



