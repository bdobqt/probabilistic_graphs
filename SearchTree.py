from anytree import Node, RenderTree, find
import copy
import networkx as nx

class St:
    a = 0

    #Create an St from a PGraph. Root is stored in search_troot.
    def __init__(self, graph):
        self.search_troot = Node("root", parent=None)
        for elements in nx.enumerate_all_cliques(graph):
            templist = list(elements)
            # Popping last element so we can find its parent and create the child on St
            templist.pop()
            nodefound = find(self.search_troot, lambda node: node.name == templist)
            if nodefound is not None:
                Node(elements, parent=nodefound)
            else:
                Node(elements, parent=self.search_troot)
        self.solidroot = copy.deepcopy(self.search_troot)  # close on ST


    def add_element(self, element_S):
        nodeFound = find(self.search_troot, lambda node: node.name == element_S.name)
        nodeFound.parent = self.search_troot

    def search_in_Solid_tree(self, nodename):
        nodeFound = find(self.solidroot, lambda node: node.name == nodename)
        return nodeFound

