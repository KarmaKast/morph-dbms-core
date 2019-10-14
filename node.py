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

#import nodeLib
from . import structure

    
class Node_Manager:
    def __init__(self, **kwargs):
        pass
        
    @staticmethod
    def create_node(**kwargs):
        """[kwargs]
        node_ID
        data
        relation_claims
        """
        #self.node_data = node_struct.Node_struct(
        #    data = {},
        #    relation_claims = []
        #)
        node_ID : structure.node_structs.Node_ID_Struct
        if {"node_ID"}.issubset(kwargs.keys()):
            node_ID = structure.node_structs.Node_ID_Struct(
                ID = kwargs['node_ID']['ID'],
                node_name = kwargs['node_ID']['node_name']
                )
        node_ = structure.node_structs.Node_Struct(
            node_ID = node_ID,
            data = kwargs["data"] if ("data") in kwargs.keys() else {},
            relation_claims = []
        )
        return node_
        
    @staticmethod
    def claim_relations(from_node, to_nodes:list, rel_from_to_to = None, rel_to_to_from = None):
        def add_relation(from_node, to_node , rel_from_to_to = None, rel_to_to_from = None):
            if rel_from_to_to != None:
                relation = structure.node_structs.Relation_Claim_Struct(
                    to_node = to_node,
                    relation = structure.node_structs.Relation_Struct(relation_name = rel_from_to_to),
                    rel_direction = 'from_to_to'
                )
                from_node.relation_claims.append(relation)
            if rel_to_to_from != None:
                relation = structure.node_structs.Relation_Claim_Struct(
                    to_node = to_node,
                    relation = structure.node_structs.Relation_Struct(relation_name = rel_to_to_from),
                    rel_direction = 'to_to_from'
                )
                from_node.relation_claims.append(relation)
        for to_node_ in to_nodes:
            add_relation(from_node, to_node_, rel_from_to_to, rel_to_to_from)
           
    @staticmethod
    def accept_relations(node_, from_nodes):
        for from_node in from_nodes:
            for relation in from_node.relation_claims:
                if relation.to_node == node_:
                    Node_Manager.claim_relations(from_node = node_, to_nodes = [relation.from_node], rel_from_to_to=relation.rel_to_to_from, rel_to_to_from = relation.rel_from_to_to)
                    #print("DEBUG", relation)
                    
    @staticmethod
    def create_related_node(**kwargs):
        """
            use create_node() and then add relation_claims btw them
            [kwargs]
                from_node
                node_ID
                data
                rel_from_to_to
                rel_to_to_from
        """
        assert 'node_ID' in kwargs.keys()
        new_node_ : structure.node_structs.Node_Struct
        if 'data' in kwargs.keys():
            new_node_ = Node_Manager.create_node(node_ID = kwargs["node_ID"], data = kwargs['data'])
        else:
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
            
        return new_node_
    
    @staticmethod
    def get_rel_node(node_, location: List[int]):
            node_ : structure.node_structs.Node_Struct = node_.relation_claims[location[0]].to_node
            for i in location[1:]:
                node_ = node_.relation_claims[i].to_node
            return node_
    
    @staticmethod
    def get_rel_nodes(node_, locations: List[List[int]]):
        nodes_ : List[deLib.structure.node_structs.Node_Struct] = []
        for location in locations:
            nodes_.append(Node_Manager.get_rel_node(node_, location))
        
        return nodes_
 