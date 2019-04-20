import networkx as nx
import random
import time
from multiprocessing import Pool
from threading import Thread

class ProbabilityGraph:

    #Constructor for random dense graph(v,e) G or recieves a set graph
    def __init__(self, graph = None, v = None, e = None):
        self.G = nx.Graph()
        f = open("results.txt", "a")
        if graph == None:
            start = time.time()
            self.G = nx.dense_gnm_random_graph(v, e)
            end = time.time()
            start2 = time.time()
            self.createGraph()
            end2 =time.time()
            print('Bhke')
            f.write("Creating Dense G first Elapsed time %g seconds\n" % (end - start))
            f.write("Creating The probaility tree Elapsed time %g seconds\n" % (end2 - start2))
            f.close()
            #print(list(nx.enumerate_all_cliques(self.G)))
        else:
            #Which mean i got an input graph which is a list with N tuples.(NodeA, NodeB, Probability).
            self.createGraphfromList(graph)

    def createGraphfromList(self, list):
        #nodeA = line[0], nodeB = line[1], probability = line[2]
        #a = 0
        for line in list:
            #random.seed(a)
            probability = random.uniform(0, 1)
            self.G.add_node(line[0], probability=probability)
            #a = a + 1
            #random.seed(a)
            probability = random.uniform(0, 1)
            self.G.add_node(line[1], probability=probability)
            probability = float(line[2])
            self.G.add_edge(line[0], line[1], probability=probability)
        #print('Done')
            #a = a + 1


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

    def createGraph(self):
        # Filling Vertices and Edges with probabilities.
       # start = time.time()
        for node in list(self.G.nodes):
            self.createPrNode(node)
        for edge in list(self.G.edges):
            self.createPrEdge(edge)
        #end = time.time()
       # duration = end - start
        #print('Creating graph took ', duration)

    def createPrNode(self, node):
        probability = random.uniform(0, 1)
        self.G.nodes[node]['probability'] = probability

    def createPrEdge(self, edge):
        probability = random.uniform(0, 1)
        self.G.edges[edge]['probability'] = probability

