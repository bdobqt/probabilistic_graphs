import testingstuff as ts
import networkx as nx
from anytree import Node, RenderTree, findall_by_attr , find
import heapq
#from heapq import heapify, heappush, heappop
import operator
from operator import itemgetter

def test(G, k ,s):
#def test():
   # s = 2  # Each set contains at least s vertex.
   # k = 2  # number of vertex sets in our collection.
    #G = ts.probabilities_graph_uniform()
    Htopk = [] # min-heap - dict [ Prmc : List of clique nodes]
    Hext = [] # max-heap - dict [ Prc : List of clique nodes]
    heapq._heapify_max(Hext)
    heapq.heapify(Htopk)
    t = 0 # Holds the maximal clique probability in Htopk
    root = create_search_tree(G) #This is a full-created Search Tree
    pruned = False # Init
    pop = 0 # pops
    C = [] # C is our graph - list
    clique = nx.Graph()
    #print(RenderTree(root))
    # For each vertex, we have already all the neighbours connected to to our Search Tree.
    while root.height != 0:
    #List of children is always being reduced,so our pops will
    ##always target the 0 element of the list until the list becomes empty.
        nodePop = root.children[0]
        nodePop.parent = None
        pruned = generate_children(Htopk, k, G, t, nodePop, s, root, Hext) #remove the poped root child from the search tree
        if pruned == False:
            updatetopk(C,s,Htopk,k)
    while len(Hext) != 0:
        CfromExt = Hext[0][1]
        heapq.heappop(Hext)
        pruned = generate_children(Htopk, k, G, t, CfromExt, s, root, Hext)
        if pruned == False:
            updatetopk(CfromExt, s, Htopk, k)
    print(Htopk)
    return


def generate_children(Htopk, k, G, t, nodePop, s, root, Hext):
    C = convert(nodePop.name, G)
    PrC = ts.clique_prob_lemma2(C)
    if basic_prune(Htopk, k, PrC, t) == True:
        return True
    if sized_based_prune(s, nodePop) == True :
        return True
    d = 1
    S = dict() # S is a dict [ δ(Ci,C): listofnodes]that will be sorted later
    for child in nodePop.children: #Each children of nodePop has one neighbour.
        Ci = convert(child.name,G)
        PrCi = ts.clique_prob_lemma2(Ci)
        di =  PrCi / PrC
        PrC =  PrC * di
        d = d * (1 - di)
        S[di] = child
    Prmc = PrC * d
    sorted_S = sorted(S.items(), key=operator.itemgetter(0),reverse=True) #sorting the keys of S in descending order
    if look_ahead_prune(PrC, len(C.nodes()), sorted_S, t, s):
        return True
    if anti_monotonicty_based_prune(sorted_S, t):
        return True
    #return True
    flag = True
    for index in range(len(sorted_S) - 1,0,-1):
        element_S  = sorted_S[index]
        v = sorted_S[index][len(sorted_S[index])-1]
        for u in nodePop.name:
            if u >= v :
                flag = False
        if flag == True :
            Prctemp = ts.clique_prob_lemma2(convert(element_S))
            if basic_prune(Htopk,k,Prctemp,t):
                if len(element_S)<= s:
                    pushh(element_S, root)
                else:
                    heapq.heappush(Hext, [PrC, element_S])

    return True

def updatetopk(C,s,Htopk, k, t ,Prmc):
    Prctemp = ts.clique_prob_lemma2(convert(C))
    if len(C) < s :
        return
    if len(Htopk) < k:
        heapq.heappush(Htopk, [Prctemp, C])
    if len(Htopk) == k and Prmc > t :
        heapq.heappop(Htopk)
        heapq.heappush(Htopk, [Prctemp, C])
    t = Htopk[0][0]


def pushh(element_S,root):
    nodeFound = find(root, lambda node: node.name == element_S)
    nodeFound.parent = root

def anti_monotonicty_based_prune(lengthHtopk, k, PrC, Prmc,S, t):
    d= 1
    listkeys = list(S.keys())
    for index in range(1,len(listkeys)):
        d = d * (1 - listkeys[index])
    temp = 1 - 1/(1 + d)
    if lengthHtopk == k and Prmc <= t and listkeys[0] <= temp:
        return True
    else:
        return False

def look_ahead_prune(PrC, lengthC, S, t, s):

    d = 1
    listkeys = list(S.keys())
    for index in range(0,s - lengthC):
        d = d * listkeys[index]
    if PrC *d <= t:
        return True
    else:
        return False

def sized_based_prune(s,nodePop):
    if len(nodePop.name) + len(nodePop.children) < s:
        return False
    else:
        return True

def basic_prune(Htopk,k,Prc,t):
    if len(Htopk) == k  and Prc <= t:
        return False
    else:
        return True


#Creates a subgraph of G using a given set of nodes.
def convert(treenodename, G):
    clique = nx.Graph()
    clique = G.subgraph(treenodename)
    #print(clique.nodes(data = True))
    #print(clique.edges(data = True))
    return clique


#We can create the tree to reach S + 1 levels since we only need sets of s Vertex.
def create_search_tree(G):
    G = ts.probabilities_graph_uniform()
    root = Node("root",parent=None)
    tempList = list()
    for elements in nx.enumerate_all_cliques(G):
        tempList = list(elements)
        #Popping last element so we can find its parent and create the child on St
        tempList.pop()
        nodeFound = find(root, lambda node: node.name == tempList)
        if nodeFound != None:
            newNode = Node(elements, parent= nodeFound)
        else:
            newNode = Node(elements, parent= root)
    return root

test(ts.probabilities_graph_uniform(),2,2)
