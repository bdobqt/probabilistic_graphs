import networkx as nx
from anytree import RenderTree, Node
import heapq
import operator
import copy
import PGraph
import Search_Tree2
import time


class Bnb:
    # G is the main graph. It is initialized with probabilities_graph_uniform()
    # k is the number of sets we need.
    # s is the number of elements inside a set.
    # Hext is a max heap.
    # Htopk is a mean heap, k size, which contains [: clique].

    def __init__(self, k, s, graphclassobject = None):
        if graphclassobject == None:
            self.PG = PGraph.ProbabilityGraph(self.create_test_g(), None, None)
        else:
            self.PG = graphclassobject
        self.Hext = []
        self.Htopk = []
        heapq._heapify_max(self.Hext)
        heapq.heapify(self.Htopk)
        self.St2 = Search_Tree2.St2(self.PG.G.nodes)
        self.k = k
        self.s = s
        self.t = 0
        self.prmc = 0.0

    def branch_and_bound(self):
        root = self.St2.root
        while root.height is not 0:
            node = root.children[0]
            pruned = self.generate_children(node)
            if pruned is False:
                self.updatetopk(node.name)
            node.parent = None
        self.print_results()
        #'''
        while len(self.Hext) != 0:
            node = self.Hext[0][1]
            pruned = self.generate_children(node)
            heapq.heappop(self.Hext)
            if pruned is False:
                self.updatetopk(node.name)
        self.print_results()

    def generate_children(self, node):
        self.PG.add_children(node)
        ##print('\n')
        ##print(RenderTree(self.St2.root))
        #print("Node :   '{0}'   Children    :'{1}'  ".format(node.name, node.children))
        node_Graph = self.PG.converts_clique_to_subgraph(node.name)
        ##print("Node graph '{0}'".format(node_Graph.nodes))
        prc = self.PG.clique_prob_lemma2(node_Graph)
        print("Node :   '{0}'   Probability    :'{1}'  ".format(node.name, prc))
        if self.basic_prune(prc):
            return True
        if self.sized_based_prune(node):
            return True
        d = 1
        S = dict()  # S is a dict [ δ(Ci,C): listofnodes]that will be sorted later
        for child in node.children:  # For Each children of clique.
            #Convert child to graph
            child_Graph = self.PG.converts_clique_to_subgraph(child.name)
            ##print("Child graph '{0}'".format(child_Graph.nodes))
            # Childs probability
            PrCi = self.PG.clique_prob_lemma2(child_Graph)
            di = PrCi / prc
            # prc =  prc * di
            d = d * (1 - di)
            S[di] = child #[KEY = di : VALUE = child]
        self.prmc = prc * d
        print("Node :   '{0}'   Maximal Probability    :'{1}'  ".format(node.name, self.prmc))
        ##print("Prmc is :    '{0}'".format(self.prmc))
        sorted_S = sorted(S.items(), key=operator.itemgetter(0),
                          reverse=True)  # sorting the keys of S in descending order
        ##print(sorted_S)
        if self.look_ahead_prune(prc, len(node_Graph.nodes()), sorted_S):
            return True
        if self.anti_monotonicty_based_prune(sorted_S):
            return True
        for index in range(len(sorted_S) - 1, -1, -1):
            # Element_S contains a tuble of S [Probability : Neighbour Clique]
            print("Child : '{0}'    Probability : '{1}'".format(sorted_S[index][1], sorted_S[index][0]))
            flag = self.checkingLetterOrder(node.name, copy.deepcopy(sorted_S[index][1].name))
            element_S = sorted_S[index]
            if self.basic_prune(element_S[0]) == True:
                flag = False
            if flag:
                if len(element_S[1].name) <= self.s:
                    self.St2.add_element(element_S[1])
                else:
                    #print(element_S[1])
                    #print(element_S[1].name)
                    heapq.heappush(self.Hext, [prc * element_S[0], element_S[1]])# pushing [ Prci , Prci.name]
        return False

    #We can either use this or remove checking the same children over and over in our algorithm. Both are used.
    def checkingLetterOrder(self, clique, neighbourC):
        ##print("Clique : '{0}' Neighbour : '{1}'".format(clique, neighbourC))
        last = None
        for u in neighbourC:
            if u not in clique:
                last = u
        if last == None:
            return False
        else:
            return True

    def updatetopk(self, C):
        ##print("C : '{0}'    LengthC : '{1}' ".format(C,len(C)))
        if len(C) < self.s:
            return
        if len(self.Htopk) < self.k:
            heapq.heappush(self.Htopk, [self.prmc, C])
        elif len(self.Htopk) == self.k and self.prmc > self.t:
            heapq.heappop(self.Htopk)
            heapq.heappush(self.Htopk, [self.prmc, C])
        self.t = self.Htopk[0][0]

    def anti_monotonicty_based_prune(self, S):
        d = 1
        for index in range(1, len(S)):
            d = d * (1 - S[index][0])
        temp = 1 - 1 / (1 + d)
        if (len(S) == 0):
            return False
        if len(self.Htopk) == self.k and self.prmc <= self.t and S[0][0] <= temp:
            #print('Antimonotonicity Pruning')
            return True
        else:
            return False

    # S contains all neighbours of C and their Prc. d is PrCi / PrC.
    def look_ahead_prune(self, prc, lengthC, S):
        d = 1
        end = self.s - lengthC
        for index in range(0, end):
            d = d * S[index][0]
        if prc * d <= self.t and len(self.Htopk) == self.k :
            #print('Lookahead Pruning')
            return True
        else:
            return False

    # Pruning the subtree if the number of vertices is less than s. Checking the length of the children since they are parent + one adjacent node.
    def sized_based_prune(self, node):
        if len(node.name) + len(node.children) < self.s:
            #print('Sized based pruning')
            return True
        else:
            return False

    # If topk is full then there is a chance a node with less probability to be left out which has bigger cliques as children.
    def basic_prune(self, prc):
        if len(self.Htopk) == self.k and prc <= self.t:
            #print("Length of Htopk '{0}', K : '{1}', prc : '{2}',t : '{3}'".format(len(self.Htopk), self.k, prc, self.t))
            #print('Basic pruning')
            return True
        else:
            return False

    def print_results(self):
        '''
        for cliques in nx.find_cliques(self.PG.G):
            if len(cliques) == self.s or len(cliques) > self.s:
                print(cliques)
        '''
        print("Htopk : '{0}'\n".format(self.Htopk))
        print("Hext : '{0}'\n".format(self.Hext))

