import networkx as nx
import random
import time
from multiprocessing import Pool
from threading import Thread
from anytree import Node

class ProbabilityGraph:

    #Constructor for random dense graph(v,e) G or recieves a set graph
    def __init__(self, graph = None, v = None, e = None):
        self.G = nx.Graph()
        f = open("results.txt", "a")
        if graph == None:
            start = time.time()
            self.G = nx.dense_gnm_random_graph(v, e, seed = 444)
            end = time.time()
            start2 = time.time()
            self.createGraph()
            end2 =time.time()
            #print('Bhke')
            f.write("Creating Dense G first Elapsed time %g seconds\n" % (end - start))
            f.write("Creating The probaility tree Elapsed time %g seconds\n" % (end2 - start2))
            f.close()
            #print(list(nx.enumerate_all_cliques(self.G)))
        else:
            #Which mean i got an input graph which is a list with N tuples.(NodeA, NodeB, Probability).
            self.createGraphfromList(graph)
        self.setOfAllCliques = set(tuple(x) for x in list(nx.enumerate_all_cliques(self.G)))
        #print(self.setOfAllCliques)
        #Remove from set everytime i access the setOfAllCliques!


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

    def add_children(self, node):
        children = [x for x in self.setOfAllCliques if self.tuple_Condition(node.name, x)]
        for element in children:
            self.setOfAllCliques.remove(element)

        #print("Children : '{0}'".format(children))
        for child in children:
            Node(child, parent=node)


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

    def tuple_Condition(self, tupleA, tupleB):
        #print("Tuple A : '{0}' Tuple B : '{1}'".format(tupleA,tupleB))
        #tupleA = tuple([tupleA])
        #print("Tuple A : '{0}' Tuple B : '{1}'".format(tupleA,tupleB))
        #print("Tuple A :'{0}' and Tuple B : '{1}'".format(tupleA,tupleB))
        if len(tupleA) + 1 != len(tupleB):
            #print("Len A :'{0}' and Len B : '{1}'".format(len(tupleA), len(tupleB)))
            return False
        else:
            for element in tupleA:
                if element not in tupleB:
                    return False
           # print("True child   '{0}'".format(element))
            return True

'''
def tuple_Condition(tupleA, tupleB):
    if len(tupleA) + 1 != len(tupleB):
        return False
    else:
        for i in range(0, len(tupleA)):
            if tupleA[i] not in tupleB:
                return False
        return True



a = (4,3)
seta = {(4,), (4, 2),(4, 3, 5), (4, 3, 7), (4, 2, 6), (6,)}
matches = [x for x in seta if tuple_Condition(a , x)]
for lol in matches:
    print(lol)

'''

'''
name = 'krogane_prob.txt'
#name = 'gavin_prob.txt'
alllines = []
txtfile = open(name,"r")
for line in txtfile:
    line = line.rstrip('\n')
    templine = line.split()
    alllines.append(templine)
txtfile.close()
PG = ProbabilityGraph(alllines, None, None)
start = time.time()
listCl = list(nx.enumerate_all_cliques(PG.G))

a = list()
for child in listCl:
    if '2' in child:
        print(child)
        a.append(child)
end = time.time()
print(a)
print('Searching took %s' % (end - start))

start2 = time.time()
#a = [x for x in listCl if '2' in x]
set1 = set(tuple(x) for x in listCl)
end2 = time.time()
print(set1)
#print(a)
print('Searching 2 took %s' % (end2 - start2))

'''


'''
v= 4000
e =4000
G = nx.Graph()
G = nx.dense_gnm_random_graph(v, e)
matches2 = list()
st = time.time()
matches = [x for x in list(nx.enumerate_all_cliques(G)) if 1 in x]
end = time.time()
print(' Matches took %s' %(end - st))
print(matches)
st2 = time.time()
for x in list(nx.enumerate_all_cliques(G)):
    if 1 in x:
        matches2.append(x)
end2 = time.time()
print(' Matches 2 took %s' %(end2 - st2))
print(matches2)'''

'''
a ={(2,), (4, 2)}
a.remove((2,))
print(a)

'''