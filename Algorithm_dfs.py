import networkx as nx
from anytree import Node
import heapq
import operator
import math
import ST
import time
import datetime


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
        self.prune_basic = 0
        self.prune_size_based = 0
        self.prune3_antimonoton = 0
        self.prune_lookahead = 0
        self.prune_basic_c = 0
        self.prune_size_based_c = 0
        self.prune3_antimonoton_c = 0
        self.prune_lookahead_c = 0
        self.gench_ph1 = 0
        self.gench_ph2 = 0
        self.uptopk_ph1 = 0
        self.add_ch_ph1 = 0

# After popping the first node from our Search Tree we will be adding children to it.

    def add_children(self, node):
        st_add = time.time()
        #grafos me ola ta edges tou kombou.
        tempGraph = nx.Graph()
        tempedges = self.PG.G.edges(node.name)
        tempGraph.add_edges_from(tempedges)
        #print(tempGraph.edges)
        enum_cliques = [x for x in nx.enumerate_all_cliques(tempGraph) if len(node.name) +1 == len(x)]
        #print("Nodes : {0} List :{1}\n".format(node.name,list(enum_cliques)))
        for clique in enum_cliques:
            Node(clique, parent=node)
        dur_ch = time.time() - st_add
        self.add_ch_ph1 += dur_ch

# This is the main Algorithm Branch and Bound.

    def branch_and_bound(self):
        print(len(self.PG.G.nodes()))
        print(len(self.PG.G.edges()))
        print('\n')
        print("3 : {0}".format(len([x for x in list(nx.enumerate_all_cliques(self.PG.G)) if len(list(x)) == 3])))
        print("4 : {0}".format(len([x for x in list(nx.enumerate_all_cliques(self.PG.G)) if len(list(x)) == 4])))
        print("5 : {0}".format(len([x for x in list(nx.enumerate_all_cliques(self.PG.G)) if len(list(x)) == 5])))
        print("6 : {0}".format(len([x for x in list(nx.enumerate_all_cliques(self.PG.G)) if len(list(x)) == 6])))
        print("7 : {0}".format(len([x for x in list(nx.enumerate_all_cliques(self.PG.G)) if len(list(x)) == 7])))
        print("8 : {0}".format(len([x for x in list(nx.enumerate_all_cliques(self.PG.G)) if len(list(x)) == 8])))
        start_ph1 = time.time()
        root = self.St2.root
        frontHead = self.St2.frontHead
        while root.height != 0 or frontHead.height != 0:
            #print('len front {0}'.format(len(frontHead.children)))
            if frontHead.height == 0 :
                node = root.children[0]
            else:
                node = frontHead.children[0]
            start_gench = time.time()
            node.parent = None
            pruned = self.generate_children(node)
            dur_gench = time.time() - start_gench
            self.gench_ph1 += dur_gench
            start_up_ph1 = time.time()
            if pruned is False:
                self.updatetopk(node.name)
            #dur_uptopk_ph1 = time.time() - start_up_ph1
            dur_uptopk_ph1 = time.time() - start_up_ph1
            self.uptopk_ph1 += dur_uptopk_ph1
            #print(self.gench_ph1)
        dur_ph1 = time.time() - start_ph1
        #print(" Len Hext : {0} \n".format(len(self.Hext)))
        start_ph2 = time.time()
        #print('ph2')
        while len(self.Hext) != 0:
            #print(len(self.Hext))
            node = self.Hext[0][1]
            heapq.heappop(self.Hext)
            start_gench = time.time()
            pruned = self.generate_children(node)
            dur_gench = time.time() - start_gench
            self.gench_ph2 += dur_gench
            if pruned is False:
                self.updatetopk(node.name)
        dur_ph2 = time.time() - start_ph2
        self.printtxt(dur_ph1, dur_ph2)


    def printtxt(self, ph1, ph2):
        f = open("times.txt", "a")
        f.write("Phase 1 : '{0}'\n".format(str(datetime.timedelta(seconds=ph1))))
        f.write("Phase 2 : '{0}'\n".format(str(datetime.timedelta(seconds=ph2))))
        f.write("Gen Children Ph1 : '{0}'\n".format(str(datetime.timedelta(seconds=self.gench_ph1))))
        f.write("Gen Children Ph2 : '{0}'\n".format(str(datetime.timedelta(seconds=self.gench_ph2))))
        f.write("Add Children Ph1 : '{0}'\n".format(str(datetime.timedelta(seconds=self.add_ch_ph1))))
        f.write("Update topk : '{0}'\n".format(str(datetime.timedelta(seconds=self.uptopk_ph1))))
        f.write("Basic_Pruning : '{0}'\n".format(str(datetime.timedelta(seconds=self.prune_basic))))
        f.write("Basic_Pruning #: '{0}'\n".format( self.prune_basic_c))
        f.write("Size_Based : '{0}'\n".format(str(datetime.timedelta(seconds=self.prune_size_based))))
        f.write("Size_Based #: '{0}'\n".format(self.prune_size_based_c))
        f.write("Antimonotonicty : '{0}'\n".format(str(datetime.timedelta(seconds=self.prune3_antimonoton))))
        f.write("Antimonotonicty #: '{0}'\n".format(self.prune3_antimonoton_c))
        f.write("Look_Ahead : '{0}'\n".format(str(datetime.timedelta(seconds=self.prune_lookahead))))
        f.write("Look_Ahead #: '{0}'\n".format(self.prune_lookahead_c))
        f.close()
        print("Htopk : {0} \n".format(self.Htopk))
        print("Hext : {0} \n".format(self.Hext))

    def generate_children(self, node):
        #print('Bhke gen')
        self.add_children(node)
        node_Graph = self.PG.converts_clique_to_subgraph(node.name)
        #("Node.name {0}".format(node.name))
        prc = self.PG.clique_prob_lemma2(node_Graph)
        if self.basic_prune(prc):
            return True
        if self.sized_based_prune(node):
            return True
        d = 1
        #print('Prc : {0} nodes {1}'.format(prc, node.name))
        S = dict()  # S is a dict [ δ(Ci,C): listofnodes]that will be sorted later
        for child in node.children:  # For Each children of clique. (Nodechild1, Nodechild2..)
            child_Graph = self.PG.converts_clique_to_subgraph(child.name)
            PrCi = self.PG.clique_prob_lemma2(child_Graph)
            #print('Prci : {0}, child : {1}'.format(PrCi, child))
            di = PrCi / prc
            # prc =  prc * di
            d = d * (1 - di)
            S[di] = child #[KEY = di : VALUE = child]
        self.prmc = prc * d
       # print('Bhke prmc')
        #print('PRMC : {0}'.format(self.prmc))
        sorted_S = sorted(S.items(), key=operator.itemgetter(0),
                          reverse=True)  # sorting the keys of S in descending order
        #print("Prc : {0}, Neighbours {1}".format(prc,S.keys()))
        if self.look_ahead_prune(node_Graph, sorted_S, prc):
            return True
        if self.anti_monotonicty_based_prune(sorted_S):
            return True
        tempRoot = Node('tempRoot',parent= None)
        for index in range(len(sorted_S) - 1, -1, -1):
            # Element_S contains a tuble of S [Probability : Neighbour Clique]
            element_S = sorted_S[index]
            newIntChild = map(int,element_S[1].name)
            maxNeighbour = max(newIntChild)
            #print("Node.Name : {0}, MaxNeighbour : {1}, Child : {2}".format(node.name, maxNeighbour, element_S[1].name))
            if maxNeighbour not in map(int,node.name):
                if self.basic_prune(element_S[0]) is False: #!= True:
                    if len(element_S[1].name) <= self.s:
                        element_S[1].parent = tempRoot
                        #self.St2.add_frontHead(element_S[1].name)
                    else:
                        heapq.heappush(self.Hext, [prc * element_S[0], element_S[1]])# pushing [ Prci , Node(Prci.name)]
        #print(tempRoot.children)
        #print('Bhke geitones')
        for child in tempRoot.children[::-1]:
            #print(child)
            self.St2.add_frontHead(child)
        return False


    def updatetopk(self, C):
        if len(C) < self.s:
            return
        if len(self.Htopk) < self.k:
            heapq.heappush(self.Htopk, [self.prmc, C])
        elif len(self.Htopk) == self.k and self.prmc > self.t:
            #heapq.heappop(self.Htopk)
            #heapq.heappush(self.Htopk, [self.prmc, C])
            heapq.heappushpop(self.Htopk,[self.prmc, C])
        self.t = self.Htopk[0][0]

    def anti_monotonicty_based_prune(self, S):
        #print('S {0} and lenS : {1}'.format(S,len(S)))
        start_anti = time.time()
        d = 1
        if (len(S) == 0):
            return False
        for index in range(1, len(S)):
            d = d * (1.0 - S[index][0])
        temp = 1.0 - (1.0 / (1.0 + d))
        #print("Prmc : {0}, self.t : {1}, Product :{2}".format(self.prmc, self.t, temp))
        #print("S : {0}, S[0] : {1} t : {2}\n".format(S, S[0][0], self.t))
        if len(self.Htopk) == self.k and self.prmc <= self.t and S[0][0] <= temp:
            anti_dur = time.time() - start_anti
            self.prune3_antimonoton_c += 1
            self.prune3_antimonoton += anti_dur
            return True
        else:
            return False

    # S contains all neighbours of C and their Prc. d is PrCi / PrC.
    def look_ahead_prune(self,node_graph, S, prc):
        start_look = time.time()
        lengthC = len(list(node_graph.nodes()))
        #print("Length C : {0}, S : {1} ".format(lengthC,list(node_graph.nodes())))
        d = 1
        end = self.s - lengthC
        if end > len(S):
            end = len(S)
       # print("Prc :  '{0}'  t :  '{1}' \n ".format(prc * d, self.t))
        for index in range(0, end):
            # print("Bhke : {0}".format(S[index]))
             d = d * S[index][0]
        #if len(self.Htopk) != 0:
            #print("rootofHtopk : {0}  prc * d : {1} ".format(self.Htopk[0][0], prc*d))
            #print("ROUNDED prc * d : {0}  t  : {1} , end : {2}".format(round((prc * d),5), round((self.t),5), end1))
        #if len(self.Htopk) == self.k:
            #print(" prc * d : {0}  t  : {1}".format(round((prc * d),8), round(self.t,8)))
        if prc * d < self.t  and len(self.Htopk) == self.k:
            #print("ROUNDED prc * d : {0}  t  : {1}".format(prc * d, self.t))
            dur_look = time.time() - start_look
            self.prune_lookahead += dur_look
            self.prune_lookahead_c +=1
            return True
        else:
            return False


    # Pruning the subtree if the number of vertices is less than s. Checking the length of the children since they are parent + one adjacent node.
    def sized_based_prune(self, node):
        start_sized = time.time()
        #print('len node : {0}, len chilren : {1}'.format(len(node.name) , len(node.children)))
        if len(node.name) + len(node.children) < self.s:
            #f = open('Pruning.txt', 'a')
            #f.write("sized_based_prune '{0}'\n ".format(self.prune2))
            #f.close()
            end_sized = time.time()
            dur_sized = end_sized - start_sized
            self.prune_size_based += dur_sized
            self.prune_size_based_c +=1
            return True
        else:
            return False


    # If topk is full then there is a chance a node with less probability to be left out which has bigger cliques as children.
    def basic_prune(self, prc):
        start_basic = time.time()
        if len(self.Htopk) == self.k and prc <= self.t:
            end_basic = time.time()
            dur_basic = end_basic - start_basic
            self.prune_basic += dur_basic
            self.prune_basic_c +=1
            return True
        else:
            return False


#'''