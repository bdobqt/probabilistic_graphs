import networkx as nx
from anytree import RenderTree
import heapq
import operator
import copy
import PGraph
import SearchTree
import time


class Bnb:
    # G is the main graph. It is initialized with probabilities_graph_uniform()
    # k is the number of sets we need.
    # s is the number of elements inside a set.
    # Hext is a max heap.
    # Htopk is a mean heap, k size, which contains [: clique].
    # Root is a Node.
    #1,2

    def __init__(self, k, s, graphclassobject = None):
        #start = time.time()
        self.Cc = None
        if graphclassobject == None:
            self.PG = PGraph.ProbabilityGraph(self.create_test_g(), None, None)
        else:
            self.PG = graphclassobject
        self.Hext = []
        self.Htopk = []
        heapq._heapify_max(self.Hext)
        heapq.heapify(self.Htopk)
        start = time.time()
        self.St = SearchTree.St(self.PG.G, s)
        end = time.time()
        #print('Search Tree creation took %s' % (end - start))
        self.k = k
        self.s = s
        self.t = 0
        self.prmc = 0.0
        #print('Done bnb_int')
       # end = time.time()
       # dur = end - start
        #print('Init BnB took : ', dur)

    def create_test_g(self):
        G = nx.Graph()
        G.add_nodes_from([0, 1, 2, 3])
        G.add_edges_from([(0, 2),(0, 3),(0, 1), (1, 2), (1, 3), (2, 3)])
        return  G

    def branch_and_bound(self):
        #start = time.time()
        # For each vertex, we have already all the neighbours connected to to our Search Tree.
        root = self.St.search_troot
        while root.height is not 0:
            node = root.children[0]
            self.Cc = node.name
            pruned = self.generate_children(node)  # remove the poped root child from the search tree
            node.parent = None  # Deleting the node after we used it.
            if pruned is False:
                self.updatetopk(node.name)
        #self.print_results()
        while len(self.Hext) != 0:
            CfromExt = self.Hext[0][1]
            node = self.St.search_in_Solid_tree(CfromExt.name)
            self.Cc = node.name
            heapq.heappop(self.Hext)
            pruned = self.generate_children(node)
            if pruned is False:
                self.updatetopk(node.name)
        self.print_results()
       # end = time.time()
        #print("Bnb elapsed time %g seconds" %(end-start))

    def generate_children(self, node):
        #Convert the clique to a graph
        node_Graph = self.PG.converts_clique_to_subgraph(node.name)
        #Probability of the C clique
        prc = self.PG.clique_prob_lemma2(node_Graph)
        if self.basic_prune(prc) :
            return True
        if self.sized_based_prune(node) :
            return True
        d = 1
        S = dict()  # S is a dict [ δ(Ci,C): listofnodes]that will be sorted later
        for child in node.children:  # For Each children of clique.
            #Convert child to graph
            child_Graph = self.PG.converts_clique_to_subgraph(child.name)
            # Childs probability
            PrCi = self.PG.clique_prob_lemma2(child_Graph)

            di = PrCi / prc
            # prc =  prc * di
            d = d * (1 - di)
            S[di] = child #[KEY = di : VALUE = child]
        self.prmc = prc * d
        sorted_S = sorted(S.items(), key=operator.itemgetter(0),
                          reverse=True)  # sorting the keys of S in descending order
        if self.look_ahead_prune(prc, len(node_Graph.nodes()), sorted_S):
            return True
        if self.anti_monotonicty_based_prune(prc, sorted_S):
            return True
        for index in range(len(sorted_S) - 1, -1, -1):
            #flag = True
            # Element_S contains a tuble of S [Probability : Neighbour Clique]
            flag = self.checkingLetterOrder(node.name, copy.deepcopy(sorted_S[index][1].name))
            element_S = sorted_S[index]
            if self.basic_prune(element_S[0]) == True:
                flag = False
            if flag:
                if len(element_S[1].name) <= self.s:
                    self.St.add_element(element_S[1])
                else:
                    heapq.heappush(self.Hext, [prc * element_S[0], element_S[1]])# pushing [ Prci , Prci.name]
        return False

    def generate_children2(self, node):
        #Convert the clique to a graph
        node_Graph = self.PG.converts_clique_to_subgraph(node.name)
        #Probability of the C clique
        prc = self.PG.clique_prob_lemma2(node_Graph)
        if self.basic_prune(prc) :
            return True
        if self.sized_based_prune(node) :
            return True
        d = 1
        S = dict()  # S is a dict [ δ(Ci,C): listofnodes]that will be sorted later
        for child in node.children:  # For Each children of clique.
            #Convert child to graph
            child_Graph = self.PG.converts_clique_to_subgraph(child.name)
            # Childs probability
            PrCi = self.PG.clique_prob_lemma2(child_Graph)

            di = PrCi / prc
            # prc =  prc * di
            d = d * (1 - di)
            S[di] = child #[KEY = di : VALUE = child]
        self.prmc = prc * d
        sorted_S = sorted(S.items(), key=operator.itemgetter(0),
                          reverse=True)  # sorting the keys of S in descending order
        if self.look_ahead_prune(prc, len(node_Graph.nodes()), sorted_S):
            return True
        if self.anti_monotonicty_based_prune(prc, sorted_S):
            return True
        for index in range(len(sorted_S) - 1, -1, -1):
            #flag = True
            # Element_S contains a tuble of S [Probability : Neighbour Clique]
            flag = self.checkingLetterOrder(node.name, copy.deepcopy(sorted_S[index][1].name))
            element_S = sorted_S[index]
            if self.basic_prune(element_S[0]) == True:
                flag = False
            if flag:
                if len(element_S[1].name) <= self.s:
                    self.St.add_element(element_S[1])
                else:
                    heapq.heappush(self.Hext, [prc * element_S[0], element_S[1]])# pushing [ Prci , Prci.name]
        return False

    def checkingLetterOrder(self, clique, neighbourC):
        for i in range(0, len(clique)):
            if(clique[i] in neighbourC):
                neighbourC.remove(clique[i])
        vertex = neighbourC[0]
        for i in range(0, len(clique)):
            if clique[i] >= vertex:
                return False
        return True


    def updatetopk(self, C):
        if len(C) < self.s:
            return
        if len(self.Htopk) < self.k:
            heapq.heappush(self.Htopk, [self.prmc, C])
        elif len(self.Htopk) == self.k and self.prmc > self.t:
            heapq.heappop(self.Htopk)
            heapq.heappush(self.Htopk, [self.prmc, C])
        self.t = self.Htopk[0][0]

    def anti_monotonicty_based_prune(self, prc, S):
        d = 1
        for index in range(1, len(S)):
            d = d * (1 - S[index][0])
        temp = 1 - 1 / (1 + d)
        if (len(S) == 0):
            return False
        if len(self.Htopk) == self.k and self.prmc <= self.t and S[0][0] <= temp:
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
            return True
        else:
            return False

    # Pruning the subtree if the number of vertices is less than s. Checking the length of the children since they are parent + one adjacent node.
    def sized_based_prune(self, node):
        if len(node.name) + len(node.children) < self.s:
            return True
        else:
            return False

    def basic_prune(self, prc):
        if len(self.Htopk) == self.k and prc <= self.t:
            return True
        else:
            return False

    def print_results(self):
        for cliques in nx.find_cliques(self.PG.G):
            if len(cliques) == self.s :
                print(cliques)
        print('Hext : ')
        print(self.Hext)
        print('\nHtopk : ')
        print(self.Htopk)

    def test1(self):
        print(RenderTree(self.root))
        print(self.root.height)

    def checkingCl(self,s):
        for clique in nx.enumerate_all_cliques(self.PG.G):
            if len(clique) == s :
                print(clique)

