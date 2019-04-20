from anytree import Node, RenderTree, find
import copy
import networkx as nx
import time

class St:
    a = 0
    #Create an St from a PGraph. Root is stored in search_troot.
    def __init__(self, graph, s):
        #print('Creating Stree')
        self.search_troot = Node("root", parent=None)
        for elements in nx.enumerate_all_cliques(graph):
            if len(elements) >= s + 1:
                break
            if len(elements) >= s-1:
                templist = list(elements)
                # Popping last element so we can find its parent and create the child on St
                templist.pop()
                #st = time.time()
                nodefound = find(self.search_troot, lambda node: node.name == templist)
                #ed = time.time()
                #print("Time took to search node : %s" % (ed - st))
                if nodefound is not None:
                    Node(elements, parent=nodefound)
                else:
                    Node(elements, parent=self.search_troot)
        #start = time.time()
        self.solidroot = copy.deepcopy(self.search_troot)  # close on ST
        #end = time.time()
        #print('Solid root time : %s '%(end - start))
        #print('Done Stree')


    def add_element(self, element_S):
        nodeFound = find(self.search_troot, lambda node: node.name == element_S.name)
        nodeFound.parent = self.search_troot

    def search_in_Solid_tree(self, nodename):
        nodeFound = find(self.solidroot, lambda node: node.name == nodename)
        return nodeFound


