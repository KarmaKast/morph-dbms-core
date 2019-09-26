from typing import NamedTuple, List, Any

#from nodeLib.structure import node_struct 
from nodeLib.structure import node_structs

class properties:
    """
    
    """
    pass
    
class NodePack:
    pass
    
class Relations:
    def __init__(self, **kwargs):
        pass
    
class Node:
    def __init__(self, **kwargs):
        #self.node_data = node_struct.Node_struct(
        #    data = {},
        #    relations = []
        #)
        self.node_data = node_structs.node_struct(
            data = kwargs["data"] if ("data") in kwargs.keys() else {},
            relations = kwargs["relations"] if ("relations") in kwargs.keys() else []
        )
    def add_relations(self, **kwargs):
        def add_relation(node , rel_to_to_from):
            relation = node_structs.relation_struct(
                from_node = self,
                to_node = node,
                rel_from_to_to = None,
                rel_to_to_from = rel_to_to_from
            )
            self.node_data.relations.append(relation)
        if "nodes" in kwargs.keys():
            for node in kwargs["nodes"]:
                add_relation(node = node, rel_to_to_from = kwargs["rel_to_to_from"])
        pass
    def packed(self, relation_type):
        """
        Given a Node return a packet containing all the nodes related to it and itself.
        """
        packet = [self]
        for relation_ in self.node_data.relations:
            if relation_.rel_to_to_from == relation_type:
                packet.append(relation_.to_node)
        
        #return packet
        return packet
    
    
 