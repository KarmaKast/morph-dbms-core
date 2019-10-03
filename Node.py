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

#from nodeLib.structure import node_struct 
from .structure import node_structs

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
        if "node_ID" in kwargs.keys():
            node_ID = node_structs.node_ID(
                **kwargs['node_ID']
                )
        self.node_data = node_structs.node_struct(
            node_ID = node_ID,
            data = kwargs["data"] if ("data") in kwargs.keys() else {},
            relations = node_structs(kwargs["relations"]) if ("relations") in kwargs.keys() else []
        )
        
    def add_relations(self, nodes, rel_from_to_to = None, rel_to_to_from = None, **kwargs):
        def add_relation(to_node , rel_from_to_to = None, rel_to_to_from = None):
            relation = node_structs.relation_struct(
                from_node = self,
                to_node = to_node,
                rel_from_to_to = rel_from_to_to,
                rel_to_to_from = rel_to_to_from
            )
            self.node_data.relations.append(relation)
        for to_node_ in nodes:
            add_relation(to_node = to_node_, rel_from_to_to=rel_from_to_to, rel_to_to_from = rel_to_to_from)
                
    def create_node(self, **kwargs):
        """
            create a new node related to this node. So that a node can be created without having to create a variable.
        """
        """[kwargs]
        node_ID
        rel_from_to_to
        rel_to_to_from
        data
        relations
        """
        node_ = Node(node_ID = kwargs["node_ID"])
        node_.add_relations(
            nodes = [self],
            rel_from_to_to = kwargs['rel_to_to_from'],
            rel_to_to_from = kwargs['rel_from_to_to']
        )
        self.add_relations(
            nodes = [node_],
            rel_from_to_to = kwargs['rel_from_to_to'],
            rel_to_to_from = kwargs['rel_to_to_from']
            )
    
    
    def packed(self, relation_type="member", include_self=True):
        """
        Given a Node return a packet containing all the nodes related to it and itself.
        """
        packet = []
        if include_self:
            packet.append(self)
            
        for relation_ in self.node_data.relations:
            if relation_.rel_to_to_from == relation_type:
                packet.append(relation_.to_node)
        
        #return packet
        return packet
    
    def describe(self):
        # describe self.node_data
        print(self.node_data.node_ID)
        print("---- DATA ----")
        for _ in self.node_data.data.items():
            print(_[0], " : ", _[1])
        print("---- RELATION ----")
        for count,_ in enumerate(self.node_data.relations):
            print("\n-- relation ",count," :")
            print('from_node')
            print('   ', _.from_node, '  ', _.from_node.node_data.node_ID)
            print('to_node')
            print('   ', _.to_node, '  ', _.to_node.node_data.node_ID)
            print('rel_from_to_to = ', _.rel_from_to_to)
            print('rel_to_to_from = ', _.rel_to_to_from)
    
    
 