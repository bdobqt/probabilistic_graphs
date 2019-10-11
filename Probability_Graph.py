import random
import time
import networkx as nx

class ProbabilityGraph:

    #Constructor for random dense graph(v,e) G or recieves a set graph
    def __init__(self, graph = None, v = None, e = None):
        self.G = nx.Graph()
        f = open("results.txt", "a")
        if graph == None:
            #self.G = nx.caveman_graph(1,4)
            #self.G = nx.dense_gnm_random_graph(v, e, seed = 444)
            self.G = nx.complete_graph(v)
            self.createGraph()
            #print(list(nx.enumerate_all_cliques(self.G)))
        else:
            self.createGraphfromList(graph)


    def createGraphfromList(self, list):
        #nodeA = line[0], nodeB = line[1], probability = line[2]
        for line in list:
           # probability = 1
            random.seed(a=line[0])
            probability = random.uniform(0.4, 1)
            self.G.add_node(line[0], probability=probability)
            #probability = 1
            random.seed(a=line[1])
            probability = random.uniform(0.4, 1)
            self.G.add_node(line[1], probability=probability)
            if(len(line) == 3):
                probability = float(line[2])
                self.G.add_edge(line[0], line[1], probability=probability)
            else:
                probability = random.uniform(0.4, 1)
            self.G.add_edge(line[0], line[1], probability=probability)

    def createGraph(self):
        # Filling Vertices and Edges with probabilities.
        for node in list(self.G.nodes):
            self.createPrNode(node)
        for edge in list(self.G.edges):
            self.createPrEdge(edge)

    def createPrNode(self, node):
        #probability = 1
        random.seed(a = node)
        probability = random.betavariate(0.1,1)
        #print('Node : {0} Probability : {1}'.format(node, probability))
        self.G.nodes[node]['probability'] = probability

    def createPrEdge(self, edge):
        random.seed(a= edge[0])
        probability = random.betavariate(0.1,1)
        self.G.edges[edge]['probability'] = probability

    # Converts a treenode from the search tree(clique) to a graph item.
    # Our clique is a list of vertices.

    def converts_clique_to_subgraph(self, clique):
        subg = self.G.subgraph(clique)
        #print("Nodes: '{0}' Edges : '{1}'".format(subg.nodes(data = True), subg.edges(data = True)))
        return subg

    def clique_prob_lemma2(self,graph):
        Pe = 1.0
        Pv = 1.0
        #print("Nodes : {0}, len : {1}".format(list(graph.nodes),len(list(graph.nodes))))
        for node in graph.nodes(data = True):
            Pv = Pv * node[1]['probability']
        for edge in graph.edges(data = True):
            #print("Edge {0}".format(edge))
            #print(type(edge[2]['probability']))
            Pe = Pe * edge[2]['probability']
        return Pv * Pe
