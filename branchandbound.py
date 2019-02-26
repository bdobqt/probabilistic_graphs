import testingstuff as ts
import networkx as nx
from anytree import Node, RenderTree, findall_by_attr, find
import heapq
import operator
import copy
import os
import pickle
import PGraph
import SearchTree



class Bnb:
    # G is the main graph. It is initialized with probabilities_graph_uniform()
    # k is the number of sets we need.
    # s is the number of elements inside a set.
    # Hext is a max heap.
    # Htopk is a mean heap, k size, which contains [: clique].
    # Root is a Node.
    #1,2

    def __init__(self, k, s):
        self.Hext = []
        self.Htopk = []
        heapq._heapify_max(self.Hext)
        heapq.heapify(self.Htopk)
        self.PG = PGraph.ProbabilityGraph()
        #self.PG = PGraph.ProbabilityGraph(self.create_test_g())
        self.St = SearchTree.St(self.PG.G)
        self.k = k
        self.s = s
        self.t = 0
        self.prmc = 0.0

    def debugme(self):
        print()
        #print(RenderTree(self.St.solidroot))#correct
        #for e in nx.find_cliques(self.PG.G):
        #    print(e)
        #for e in nx.enumerate_all_cliques(self.PG.G):
         #   print(e)



    def create_test_g(self):
        G = nx.Graph()
        G.add_nodes_from([0, 1, 2, 3])
        G.add_edges_from([(0, 2),(0, 3),(0, 1), (1, 2), (1, 3), (2, 3)])
        return  G

    def branch_and_bound(self):
        # For each vertex, we have already all the neighbours connected to to our Search Tree.
        root = self.St.search_troot
        while root.height is not 0:
            node = root.children[0]
            pruned = self.generate_children(node)  # remove the poped root child from the search tree
            node.parent = None  # Deleting the node after we used it.
            if pruned is False:
                self.updatetopk(node.name)
        self.print_results()
        while len(self.Hext) != 0:
            CfromExt = self.Hext[0][1]
            node = self.St.search_in_Solid_tree(CfromExt.name)
            heapq.heappop(self.Hext)
            pruned = self.generate_children(node)
            if pruned is False:
                self.updatetopk(node.name)
        self.print_results()

    def generate_children(self, node):
        node_Graph = self.PG.converts_clique_to_subgraph(node.name)
        prc = self.PG.clique_prob_lemma2(node_Graph)
        print('Prc of ' + str(node.name) + ' is ' + str(prc))
        print('Children of ' + str(node.name) + ' are ' + str(node.children))
        if self.basic_prune(prc) :
            print(' Basic_pruning ' + str(node.name))
            return True
        if self.sized_based_prune(node) :
            print(' Size_Based_pruning ' + str(node.name))
            return True
        d = 1
        S = dict()  # S is a dict [ δ(Ci,C): listofnodes]that will be sorted later
        for child in node.children:  # Each children of nodepop has one neighbour.
            child_Graph = self.PG.converts_clique_to_subgraph(child.name)
            PrCi = ts.clique_prob_lemma2(child_Graph)
            di = PrCi / prc
            # prc =  prc * di
            d = d * (1 - di)
            S[di] = child #[KEY = di : VALUE = child]
        self.prmc = prc * d
        print('Maximal Prob of ' + str(node.name) + ' is ' + str(self.prmc))
        sorted_S = sorted(S.items(), key=operator.itemgetter(0),
                          reverse=True)  # sorting the keys of S in descending order
        if self.look_ahead_prune(prc, len(node_Graph.nodes()), sorted_S):
            print(' Look_ahead_pruning ' + str(node.name))
            return True
        if self.anti_monotonicty_based_prune(prc, sorted_S):
            print('Anti_monotonicity_pruning ' + str(node.name))
            return True
        for index in range(len(sorted_S) - 1, -1, -1):
            flag = True
            element_S = sorted_S[index]
            tempv = sorted_S[index][1] # storing the d(ci,c)
            tempu = copy.deepcopy(tempv.name)
            for temp in node.name:
                if(temp in tempu):
                    tempu.remove(temp)
            #print('U is '+ str(tempu))
            #   print('V is '+ str(v))
            for v in node.name:
                for u in tempu:
                    print('U is '+ str(u))
                    print('V is '+ str(v))
                    if (u < v):
                       flag = False
            if flag:
                if len(element_S[1].name) <= self.s:
                    print('Adds to st the element ' + str(element_S[1].name))
                    self.St.add_element(element_S[1])
                else:
                    print('Pushes to Hext element ' + str(element_S[1].name))
                    heapq.heappush(self.Hext, [prc * element_S[0], element_S[1]])# pushing [ Prci , Prci.name]
        return False

    def updatetopk(self, C):
        prctemp = ts.clique_prob_lemma2(self.PG.converts_clique_to_subgraph(C))
        if len(C) < self.s:
            return
        if len(self.Htopk) == self.k and self.prmc > self.t:
            heapq.heappop(self.Htopk)
            heapq.heappush(self.Htopk, [self.prmc, C])
        if len(self.Htopk) < self.k:
            heapq.heappush(self.Htopk, [self.prmc, C])
        self.t = self.Htopk[0][0]

    def anti_monotonicty_based_prune(self, prc, S):
        #print('In antim - prmc :' + str(self.prmc))
        lenhtopk = len(self.Htopk)
        d = 1
        for index in range(1, len(S)):
            d = d * (1 - S[index][0])
        temp = 1 - 1 / (1 + d)
        if (len(S) == 0):
            return False
        if lenhtopk == self.k and self.prmc <= self.t and S[0][0] <= temp:
            return True
        else:
            return False
    # S contains all neighbours of C and their Prc. d is PrCi / PrC.
    def look_ahead_prune(self, prc, lengthC, S):
        d = 1
        # print('s '+ str(s)+' C length '+ str(lengthC)+ ' S len '+ str(len(S)))
        #if (self.s - lengthC > len(S) - 1):
            #end = len(S) - 1
        #lse:
        end = self.s - lengthC
        for index in range(0, end):
            d = d * S[index][0]
        if prc * d <= self.t:
            return True
        else:
            return False
    # Pruning the subtree if the number of vertices is less than s. Checking the length of the children since they are parent + one adjacent node.
    def sized_based_prune(self, node):
        # print('nodepop.name : ' + str(len(node.name)) + ' node.children :' + str(len(nodepop.children)))
        if len(node.name) + len(node.children) < self.s:
            #print('Sized_based /T/ nodepop.name : ' + str(nodepop.name) + ' nodepop.children :' + str(nodepop.children))
            return True
        else:
            # print('Sized_based /F/ nodepop.name : ' + str(nodepop.name) + ' nodepop.children :' + str(nodepop.children))
            return False

    def basic_prune(self, prc):
        # print('prc: ' + str(prc) + ' t :' + str(t))
        if len(self.Htopk) == self.k and prc <= self.t:
            #print('Basic Prune /T/ prc: ' + str(prc) + ' t :' + str(self.t))
            return True
        else:
            # print('Basic Prune /F/ prc: ' + str(prc) + ' t :' + str(t))
            return False

    def print_results(self):
        print('Hext : \n')
        print(self.Hext)
        print('\nHtopk : \n')
        print(self.Htopk)

    def printmc(self):
        for i in nx.find_cliques(self.G):
            print(i)

    def importfiles(self):
        alllines= []
        directory = 'datasets'
        wd = os.getcwd()
        G = nx.Graph()
        for root, dirs, files in os.walk(directory):
            for file in files:
                print(file)
                if file.endswith('.txt'):
                    f = open(wd +'\\'+ directory + '\\' + file ,'r')
                    for line in f:
                        lines = line.rstrip('\n')
                        lines = lines.split()
                        alllines.append(lines)
                    G = ts.convertListToGraph(alllines)
                    f.close()
                ts.writeGtoFile(G,file)
                alllines = []

    def showmenuandload(self):
        wd = os.getcwd()
        i = 1
        for root, dirs, files in os.walk(wd):
            for file in files:
                if file.endswith('.pickle'):
                    print(str(i) + '. ' + str(file))
                    with open(wd+ '\\' + file, 'rb') as handle:
                        b = pickle.load(handle)
                    handle.close()
                    i = i + 1
        self.G = b
        #print(self.G.nodes(data = True))

    def test1(self):
        print(RenderTree(self.root))
        print(self.root.height)




#'''
bnb1 = Bnb(4, 3)
#bnb1.importfiles()
#bnb1.showmenuandload()
#bnb1.test1()
bnb1.branch_and_bound()
bnb1.debugme()

#bnb1.print_results()

#'''
