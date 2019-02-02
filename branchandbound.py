import testingstuff as ts
import networkx as nx
from anytree import Node, RenderTree, findall_by_attr, find
import heapq
import operator
import copy
import os
import pickle


class Bnb:
    G = nx.Graph()
    k = 0
    s = 0

    Hext = []
    Htopk = []
    t = 0
    root = None
    solidroot = None
    prmc = 0.0

    def __init__(self, k, s):
        self.G = ts.probabilities_graph_uniform()
        self.k = k
        self.s = s
        self.t = 0
        self.create_search_tree()
        self.solidroot = copy.deepcopy(self.root)
        heapq._heapify_max(self.Hext)
        heapq.heapify(self.Htopk)

    def branch_and_bound(self):
        # For each vertex, we have already all the neighbours connected to to our Search Tree.
        while self.root.height is not 0:
            nodepop = self.root.children[0]
            #print(RenderTree(self.root))
            pruned = self.generate_children(nodepop)  # remove the poped root child from the search tree
            nodepop.parent = None  # Deleting the node after we used it.
            if pruned is False:
                self.updatetopk(nodepop.name)
               # '''
        while len(self.Hext) != 0:
            CfromExt = self.Hext[0][1]
            nodepop = self.searchinroot(CfromExt.name)
            heapq.heappop(self.Hext)
            pruned = self.generate_children(nodepop)
            if pruned is False:
                self.updatetopk(nodepop.name)
                #'''

    def generate_children(self, nodepop):
        Cgraph = self.convert(nodepop.name)
        prc = ts.clique_prob_lemma2(Cgraph)
        if self.basic_prune(prc) :
            return True
        if self.sized_based_prune(nodepop) :
            return True
        d = 1
        S = dict()  # S is a dict [ δ(Ci,C): listofnodes]that will be sorted later
        #print(str(nodepop.name)+ '\texei\t'+str(len(nodepop.children))+'\tpaidia\t')
        for child in nodepop.children:  # Each children of nodepop has one neighbour.
            Cigraph = self.convert(child.name)
            PrCi = ts.clique_prob_lemma2(Cigraph)
            di = PrCi / prc
            # prc =  prc * di
            d = d * (1 - di)
            S[di] = child
            #print(RenderTree(child))
        self.prmc = prc * d
        #print(nodepop.name)
       # print('In gen - prmc :' + str(self.prmc))
        #print(self.prmc)
        sorted_S = sorted(S.items(), key=operator.itemgetter(0),
                          reverse=True)  # sorting the keys of S in descending order
        if self.look_ahead_prune(prc, len(Cgraph.nodes()), sorted_S):
            return True
        if self.anti_monotonicty_based_prune(prc, sorted_S):
            return True
        flag = True
        for index in range(len(sorted_S) - 1, -1, -1):
        #for index in range(0,len(sorted_S)-1):
            #print(RenderTree(sorted_S[index][1]))
            element_S = sorted_S[index]
            tempv = sorted_S[index][1]
            v = tempv.name[len(sorted_S[index]) - 1]
            for u in nodepop.name:
                if u >= v:
                    flag = False
            if flag:
                #prctemp = ts.clique_prob_lemma2(self.convert(element_S[1].name))
                #if not self.basic_prune(prctemp):
                if len(element_S[1].name) <= self.s:
                       # print('pusharei neo pruned tree')
                    self.pushh(element_S[1])
                else:
                    #print('pusharei sthn Hext')
                    heapq.heappush(self.Hext, [prc, element_S][1])
        return False

    def convert(self, treenodename):
        clique = self.G.subgraph(treenodename)
        return clique

    def updatetopk(self, C):
       # print('In updtk - prmc :' + str(self.prmc))
        prctemp = ts.clique_prob_lemma2(self.convert(C))
        # print(str(len(C)) +'  '+str(s))
        if len(C) < self.s:
            return
        if len(self.Htopk) == self.k and self.prmc > self.t:
            heapq.heappop(self.Htopk)
            heapq.heappush(self.Htopk, [self.prmc, C])
        if len(self.Htopk) < self.k:
            heapq.heappush(self.Htopk, [self.prmc, C])
        self.t = self.Htopk[0][0]
    '''
        print(C)
        print(str(self.t)+'\n')
        print(self.Htopk)
        print('\n')
    '''
    def searchinroot(self, nodename):
        nodeFound = find(self.solidroot, lambda node: node.name == nodename)
        return nodeFound


    def pushh(self, element_S):
        #print(element_S.name)
        #print(element_S.name[0:len(element_S.name)-1])
        #print(RenderTree(element_S))
        #print('\n')
        #print(RenderTree(self.root))
        nodeFound = find(self.root, lambda node: node.name == element_S.name)
        nodeFound.parent = self.root

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

    def look_ahead_prune(self, prc, lengthC, S):
        d = 1
        # print('s '+ str(s)+' C length '+ str(lengthC)+ ' S len '+ str(len(S)))
        if (self.s - lengthC > len(S) - 1):
            end = len(S) - 1
        else:
            end = self.s - lengthC
        for index in range(0, end):
            d = d * S[index][0]
        if prc * d <= self.t:
            return True
        else:
            return False

    def sized_based_prune(self, nodepop):
        # print('nodepop.name : ' + str(len(nodepop.name)) + ' nodepop.children :' + str(len(nodepop.children)))
        if len(nodepop.name) + len(nodepop.children) < self.s:
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

    def create_search_tree(self):
        self.root = Node("root", parent=None)
        templist = list()
        newnode = None
        for elements in nx.enumerate_all_cliques(self.G):
            templist = list(elements)
            # Popping last element so we can find its parent and create the child on St
            templist.pop()
            nodefound = find(self.root, lambda node: node.name == templist)
            if nodefound is not None:
                newnode = Node(elements, parent=nodefound)
            else:
                newnode = Node(elements, parent=self.root)

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

    def showmenu(self):
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








bnb1 = Bnb(3, 2)
#bnb1.importfiles()
bnb1.showmenu()
bnb1.branch_and_bound()
bnb1.print_results()

