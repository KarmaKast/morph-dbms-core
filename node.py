# Copyright 2019 Sree Chandan.R . All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List, Any

#from .structure import node_structs
#from nodeLib.structure import node_structs
import nodeLib
    
class NodePack:
    @staticmethod
    def pack(node_, include_self=True, **kwargs):
        """
        Given a Node return a packet containing all the nodes related to it and itself.
        """
        packet = []
        if include_self:
            packet.append(node_)
            
        for relation_ in node_.relations:
            if relation_.rel_to_to_from == kwargs['relation_type']:
                packet.append(relation_.to_node)
        
        #return packet
        return packet
    
class Node_Manager:
    def __init__(self, **kwargs):
        pass
        
    @staticmethod
    def create_node(**kwargs):
        """[kwargs]
        node_ID
        data
        relations
        """
        #self.node_data = node_struct.Node_struct(
        #    data = {},
        #    relations = []
        #)
        node_ID = None
        if {"node_ID"}.issubset(kwargs.keys()):
            node_ID = nodeLib.structure.node_structs.Node_ID(
                ID = kwargs['node_ID']['ID'],
                node_name = kwargs['node_ID']['node_name']
                )
        node = nodeLib.structure.node_structs.Node_Struct(
            node_ID = node_ID,
            data = kwargs["data"] if ("data") in kwargs.keys() else {},
            relations = nodeLib.structure.node_structs(kwargs["relations"]) if ("relations") in kwargs.keys() else []
        )
        return node
        
    @staticmethod
    def claim_relations(from_node, to_nodes:list, rel_from_to_to = None, rel_to_to_from = None):
        def add_relation(from_node, to_node , rel_from_to_to = None, rel_to_to_from = None):
            relation = nodeLib.structure.node_structs.Relation_Struct(
                from_node = from_node,
                to_node = to_node,
                rel_from_to_to = rel_from_to_to,
                rel_to_to_from = rel_to_to_from
            )
            from_node.relations.append(relation)
        for to_node_ in to_nodes:
            add_relation(from_node, to_node_, rel_from_to_to, rel_to_to_from)
           
    @staticmethod
    def accept_relations(node_, from_nodes):
        for from_node in from_nodes:
            for relation in from_node.relations:
                if relation.to_node == node_:
                    Node_Manager.claim_relations(from_node = node_, to_nodes = [relation.from_node], rel_from_to_to=relation.rel_to_to_from, rel_to_to_from = relation.rel_from_to_to)
                    #print("DEBUG", relation)
                    
    @staticmethod
    def create_related_node(**kwargs):
        """
            use create_node() and then add relations btw them
        """
        """[kwargs]
        from_node
        node_ID
        rel_from_to_to
        rel_to_to_from
        
        #data
        #relations
        """
        new_node_ = Node_Manager.create_node(node_ID = kwargs["node_ID"])
        if {'from_node','rel_to_to_from','rel_from_to_to'}.issubset(set(kwargs.keys())):
            Node_Manager.claim_relations(
                from_node = kwargs['from_node'],
                to_nodes = [new_node_],
                rel_from_to_to = kwargs['rel_from_to_to'],
                rel_to_to_from = kwargs['rel_to_to_from']
                )
            Node_Manager.claim_relations(
                from_node = new_node_,
                to_nodes = [kwargs['from_node']],
                rel_from_to_to = kwargs['rel_to_to_from'],
                rel_to_to_from = kwargs['rel_from_to_to']
            )
        if {'data'}.issubset(set(kwargs.keys())):
            new_node_.node_data.data.update(kwargs['data'])
            
        return new_node_
    
    @staticmethod
    def get_rel_node(node_, location: List[int]):
            node_ = node_.relations[location[0]].to_node
            for i in location[1:]:
                node_ = node_.relations[i].to_node
            return node_
    
    @staticmethod
    def get_rel_nodes(node_, locations: List[List[int]]):
        nodes_ = []
        for location in locations:
            nodes_.append(Node_Manager.get_rel_node(node_, location))
        
        return nodes_
    
class Debug_Node:
    @staticmethod
    def describe(node_, mode:str = None):
        # describe self.node_data
        if mode == 'compact':
            print(node_.node_ID)
            print("---- DATA ----")
            print(node_.data)
            print("---- RELATIONS ----")
            for count,_ in enumerate(node_.relations):
                print("\n-- relation ",count," :")
                #print('from_node : ', _.from_node.node_ID)
                print('to_node : ',  _.to_node.node_ID)
                print('rel_from_to_to = ', _.rel_from_to_to, ' | rel_to_to_from = ', _.rel_to_to_from)
        else:
            print(node_.node_ID)
            print("---- DATA ----")
            for _ in node_.data.items():
                print(_[0], " : ", _[1])
            print("---- RELATIONS ----")
            for count,_ in enumerate(node_.relations):
                print("\n-- relation ",count," :")
                print('from_node')
                print( _.from_node.node_ID)
                print('to_node')
                print(_.to_node.node_ID)
                print('rel_from_to_to = ', _.rel_from_to_to, ' | rel_to_to_from = ', _.rel_to_to_from)
 