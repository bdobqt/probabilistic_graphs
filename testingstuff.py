import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
import anytree as at
from anytree import RenderTree
import random


#Function for creating graphs and adding probabilities to both edges and vertices.
#Different ways of graph generation could be added.

#NEEDS DEBUGGING ~ POSSIBLE ISSUES WHEN PLAYING AROUND WITH NEW GRAPH SETS

class Node(object):
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)



def probabilities_graph_uniform():
    G = nx.dense_gnm_random_graph(10, 14 , seed=333)
    #G = nx.connected_caveman_graph(100, 50)
    for node in list(G.nodes):
        probability = random.uniform(0, 1)
        G.nodes[node]['probability'] = probability
    for edge in list(G.edges):
        probability = random.uniform(0, 1)
        G.edges[edge]['probability'] = probability
    return G

#We are calculating the probability of a subgraph.

def graph_probability(graph,subgraph):
    Pv = 1
    Pe = 1
    for node in list(graph.nodes):
        nodeP = graph.nodes[node]['probability']
        if subgraph.has_node(node):
            Pv = Pv * (1 - nodeP)
        else:
            Pv = Pv * nodeP
    for edge in list(graph.edges):
        edgeP = graph.edges[edge]['probability']
        if subgraph.has_edge(edge):
            Pe = Pe * (1 - edgeP)
        else:
            Pe = Pe * edgeP
    return Pv * Pe

#Calculating the clique probability using lemma2

def clique_prob_lemma2(graph):
    Pe = 1
    Pv = 1
    for node in graph.nodes(data = True):
        if node[1]:
            nodeP = node[1]['probability']
            Pv = Pv * nodeP
    for edge in graph.edges(data = True):
        Pe = Pe * edge[2]['probability']
    return Pv * Pe

#Calculating maximum clique probability using lemma 3
def getFistNode(g):
    for node in g.nodes(data=True):
        return node

def max_clique_prob_lemma3(graph):
    C = nx.Graph()
    a =getFistNode(graph)
    C.add_node(a[0],probability = a[1]['probability'])
    PrC = clique_prob_lemma2(C)
    maxProb = PrC
    Ci = nx.Graph()
    for edge in graph.edges(data = True):
        Ci.add_edge(edge[0],edge[1], probability = edge[2]['probability'])
    for node in graph.nodes(data = True):
        Ci.add_node(node[0], probability=node[1]['probability'])
        PrCi = clique_prob_lemma2(Ci)
        maxProb = maxProb * (1 - (PrCi/PrC))
    return maxProb

def test1(G,k,s):
    #creating our tree root with data = "root"
    root = at.Node("root")
    #Cliques return a list of nodes so we have to linearly dig into the graph and fetch each node and edge zZzZZ...
    for clique in nx.find_cliques(G):
        w = 0
        for i in range(0, len(clique)):#reseting and moving down to next lvl

            w = w + 1
            for j in range(0,len(clique)-w):# from the first element create all k level combinations using k sets. n-k iterations. j defines i in (i,j).
                for l in range(j+1,len(clique)):#in (i,j) clique this iteration helps with j.
                     x= 3
#                    print()
                    #print("Level : %d  -  clique ( %d, %d )" % (k,j,l))



            #len(clique) - i
            #print(len(clique))
            #αdd list[i] of the children root and then act as sets
            #for j in range():

            #for j in range

         #   at.Node(node,parent=root)
        #print(clique)
        #print(clique[0])
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))



    #print(list(nx.find_cliques(G)))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#########paper2- network reliability

#Calculating the probability of a sample graph.

def sampling_probability(graph,sample):
    Pe = 1
    for edge in list(graph.edges):
        edgeP = graph.edges[edge]['probability']
        if sample.has_edge(edge):
            Pe = Pe * edgeP
        else:
            Pe = Pe * (1 - edgeP)
    return Pe

#Network Riliability for samples of a graph

def network_reliability_graph(graph,sample):
    if nx.is_connected(sample):
        is_connected = 1
    else:
        is_connected = 0
    probability = sampling_probability(graph,sample)
    return is_connected * probability


#creating uncertain graphs.
def uncertain_graph_generator():
    G = nx.connected_caveman_graph(55,15)
    print(list(G.nodes))
    nx.draw_networkx(G)
    plt.show()

#uncertain_graph_generator()
test1(probabilities_graph_uniform(),1,1)
#test1(probabilities_graph_uniform(),4,4)


'''

G = nx.Graph()
L = nx.Graph()
G.add_nodes_from([1],probability = 0.3)
G.add_nodes_from([2],probability = 0.1)
G.add_nodes_from([3],probability = 0.2)
G.add_edge(1,2,probability = 0.4)
G.add_edge(2,3,probability = 0.4)
G.add_edge(1,3,probability = 0.4)
L.add_nodes_from([1],probability = 0.3)
L.add_nodes_from([2],probability = 0.1)
L.add_edge(1,2,probability = 0.4)

root = Node("root")
root.add_child(Node(G))
root.add_child(Node(L))
for s in root.children:
    print(s.data.nodes(data=True))
'''


#test = {1 : G}
#print(test[1].nodes(data = True))


'''
for node in G.nodes(data = True):
    probability = random.uniform(0, 1)
    G.nodes[node[0]]['probability'] = probability
for edge in G.edges(data = True):
    probability = random.uniform(0, 1)
    G[edge[0]][edge[1]]['probability'] = probability
    '''
#print(G.nodes(data = True))
#print(max_clique_prob_lemma3(G))

'''
G = nx.Graph()
#G.add_nodes_from([1, 2, 3, 4])
G.add_node(1, prob = 0.5)
s = getFistNode(G)
print(s)
'''

'''
G = nx.Graph()
G.add_nodes_from([1, 2, 3, 4])
G.nodes()
G.add_edge(1, 2)
G.add_edge(3, 4)
G.add_edge(2, 3)
G.remove_node(2)
print(list(G.edges))
'''
'''
G = nx.Graph()
G.add_nodes_from([1, 2, 3, 4])
G.add_edge(1, 2)
G.add_edge(3, 4)
nx.draw_networkx(G)
plt.show()
'''