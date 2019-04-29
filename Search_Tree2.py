from anytree import Node, RenderTree, find
import copy
import networkx as nx

class St2:
    def __init__(self, graph_Nodes):
        self.root = Node('root', parent=None)
        for node in graph_Nodes:
            node = (node,)
            Node(node, parent=self.root)


    def add_element(self,element):
        Node(element.name, parent=self.root)
