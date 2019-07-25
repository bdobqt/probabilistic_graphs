import networkx as nx
from anytree import Node
import heapq
import operator
import copy
import ST
import time


class Algorithm:

    # G is the main graph. It is initialized with probabilities_graph_uniform()
    # k is the number of sets we need.
    # s is the number of elements inside a set.
    # Hext is a max heap.
    # Htopk is a mean heap, k size, which contains [: clique].
    # Search_Tree is our main Search Tree
    # t is our temporary maximal clique probability
    # visited is a list of visited cliques when proceeding to add children to Search Tree.
    # prune 1,2,3,4 are test variables for pruning.

    def __init__(self, k, s, graphclassobject = None):
        self.k = k
        self.s = s
        self.PG = graphclassobject
        self.Hext = []
        self.Htopk = []
        heapq._heapify_max(self.Hext)
        heapq.heapify(self.Htopk)
        self.St2 = ST.Search_Tree(self.PG.G.nodes)
        self.t = 0
        self.prmc = 0.0
        self.visited = []
        self.prune1 = 0
        self.prune2 = 0
        self.prune3 = 0
        self.prune4 = 0

# After popping the first node from our Search Tree we will be adding children to it.
#

    def add_children(self, node):
        #f = open('timecheck.txt', 'a')
        st = time.time()
        tempGraph = nx.Graph()
        tempedges = self.PG.G.edges(node.name)
        tempGraph.add_edges_from(tempedges)
        st1 = time.time()
        enum_cliques = [x for x in nx.enumerate_all_cliques(tempGraph) if len(node.name) +1 == len(x)]
        en1 = time.time()
        #print('enum_cliques time : %s \n' % (en1 - st1))
        en1 = time.time()
        #f.write(' First Half Add children Dur : %s \n' % (en1 - st))
        for clique in enum_cliques:
            tempcl = copy.deepcopy(clique)
            tempcl.sort()
            #'''
            if tempcl not in self.visited:
                Node(clique, parent= node)
                self.visited.append(tempcl)
            #'''
        en = time.time()
        #f.write(' Second Half Add children Dur : %s \n' % (en - en1))
        #f.write(' Add children Dur : %s \n' % (en - st))
        #f.close()

# This is the main Algorithm Branch and Bound.

    def branch_and_bound(self):
        root = self.St2.root
       # open('timecheck.txt', 'w').close()
       # open('Pruning.txt', 'w').close()
       # open('children.txt', 'w').close()
        while root.height != 0:
           # f = open('timecheck.txt', 'a')
            #f.write(str((len(root.children))) + '\n')
            st = time.time()
            node = root.children[0]
            prunedt = time.time()
            pruned = self.generate_children(node)
            prunede = time.time()
            updatet = time.time()
            if pruned is False:
                self.updatetopk(node.name)
            updatee = time.time()
            node.parent = None
            en = time.time()
            #print('pruned time : %s \n' % (prunede - prunedt))
            #print('Update time : %s \n' % (updatee - updatet))
            #f.write(' pruned time : %s \n' % (en - st))
            #f.close()
        self.print_results()
        while len(self.Hext) != 0:
            node = self.Hext[0][2]
            prunedt = time.time()
            pruned = self.generate_children(node)
            prunede = time.time()
            heapq.heappop(self.Hext)
            updatet = time.time()
            if pruned is False:
                self.updatetopk(node.name)
            updatee = time.time()
            #print('pruned time : %s \n' % (prunede - prunedt))
            #print('Update time : %s \n' % (updatee - updatet))
        self.print_results()


    def generate_children(self, node):
        st1 = time.time()
        self.add_children(node)
        en1 = time.time()
        #print('Adding children time : %s \n' % (en1 - st1))
        #print("Node :   '{0}'   Children    :'{1}'  ".format(node.name, node.children))
        node_Graph = self.PG.converts_clique_to_subgraph(node.name)
        prc = self.PG.clique_prob_lemma2(node_Graph)
        #print("Node :   '{0}'   Probability    :'{1}'  ".format(node.name, prc))
        #f = open('children.txt', 'a')
        #f.write("Node :   '{0}'   Children    :'{1}'  \n".format(node.name, node.children))
        #f.close()
        if self.basic_prune(prc):
            return True
        if self.sized_based_prune(node):
            return True
        d = 1
        S = dict()  # S is a dict [ δ(Ci,C): listofnodes]that will be sorted later
        for child in node.children:  # For Each children of clique.
            child_Graph = self.PG.converts_clique_to_subgraph(child.name)
            PrCi = self.PG.clique_prob_lemma2(child_Graph)
            di = PrCi / prc
            # prc =  prc * di
            d = d * (1 - di)
            S[di] = child #[KEY = di : VALUE = child]
        self.prmc = prc * d
        sorted_S = sorted(S.items(), key=operator.itemgetter(0),
                          reverse=True)  # sorting the keys of S in descending order
        ##print(sorted_S)
        if self.look_ahead_prune(node_Graph, sorted_S):
            return True
        if self.anti_monotonicty_based_prune(sorted_S):
            return True
        for index in range(len(sorted_S) - 1, -1, -1):
            # Element_S contains a tuble of S [Probability : Neighbour Clique]
            element_S = sorted_S[index]
            if self.basic_prune(element_S[0]) != True:
                if len(element_S[1].name) <= self.s:
                    self.St2.add_element(element_S[1])
                else:
                    heapq.heappush(self.Hext, [prc * element_S[0] , time.time(), element_S[1]])# pushing [ Prci , Node(Prci.name)]
        return False

    def updatetopk(self, C):
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
        temp = 1 - (1 / (1 + d))
        if (len(S) == 0):
            return False
        if len(self.Htopk) == self.k and self.prmc <= self.t and S[0][0] <= temp:
            self.prune4 +=1
            #f = open('Pruning.txt', 'a')
            #f.write("anti_monotonicty_based_prune '{0}'\n ".format(self.prune4))
            #f.close()
            return True
        else:
            return False

    # S contains all neighbours of C and their Prc. d is PrCi / PrC.
    def look_ahead_prune(self,node_graph, S):
        prc = self.PG.clique_prob_lemma2(node_graph)
        lengthC = len(node_graph.nodes())
        d = 1
        end = len(S) - lengthC
        for index in range(0, end + 1):
            d = d * S[index][0]
       # print("Prc :  '{0}'  t :  '{1}' \n ".format(prc * d, self.t))
        if prc * d <= self.t and len(self.Htopk) == self.k:
            self.prune3 += 1
            #f = open('Pruning.txt', 'a')
            #f.write("Look_ahead_prune '{0}'\n ".format(self.prune3))
            #f.close()
            return True
        else:
            return False


    # Pruning the subtree if the number of vertices is less than s. Checking the length of the children since they are parent + one adjacent node.
    def sized_based_prune(self, node):
        if len(node.name) + len(node.children) < self.s:
            self.prune2 +=1
            #f = open('Pruning.txt', 'a')
            #f.write("sized_based_prune '{0}'\n ".format(self.prune2))
            #f.close()
            return True
        else:
            return False


    # If topk is full then there is a chance a node with less probability to be left out which has bigger cliques as children.
    def basic_prune(self, prc):
        if len(self.Htopk) == self.k and prc <= self.t:
            self.prune1 += 1
            #f = open('Pruning.txt', 'a')
            #f.write("Basic_prune '{0}'\n ".format(self.prune1))
            #f.close()
            return True
        else:
            return False


    def print_results(self):
        '''
        for cliques in nx.find_cliques(self.PG.G):
            if len(cliques) == self.s or len(cliques) > self.s:
                print(cliques)
        '''
        print("")
        #f = open('results.txt','a')
        #f.write("Htopk : '{0}'\n".format(self.Htopk))
        #f.write("Hext : '{0}'\n".format(self.Hext))
        #f.close
'''
    def print_size_of_objects(self):
        print("Clique Set : '{0}', St : '{1}', Htopk : '{1}', Hext : '{2}', G : '{3}' \n".format(getsizeof(self.setOfAllCliques), getsizeof(self.Htopk), getsizeof(self.Hext), getsizeof(self.PG.G)))
'''
