from anytree import Node, RenderTree, find
import copy
import networkx as nx

class Search_Tree:
    def __init__(self, graph_Nodes):
        self.root = Node('root', parent=None)
        for node in graph_Nodes:
            Node([node, ], parent=self.root)

    #Adds element to the root of the St
    def add_element(self,element):
        Node(element.name, parent=self.root)
