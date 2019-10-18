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
from . import debug

class Node_Manager:
        
    @staticmethod
    def create_node(**kwargs):
        """[kwargs]
        node_ID
        data
        relation_claims
        """
        node_ID : structure.node_structs.Node_ID_Struct
        if {"node_ID"}.issubset(kwargs.keys()):
            node_ID = structure.node_structs.Node_ID_Struct(
                ID = kwargs['node_ID']['ID'] if 'ID' in kwargs['node_ID'].keys() else None,
                node_name = kwargs['node_ID']['node_name'] if 'node_name' in kwargs['node_ID'].keys() else None
                )
        else:
            node_ID = structure.node_structs.Node_ID_Struct(
                ID = None,
                node_name = None
                )
        node_ = structure.node_structs.Node_Struct(
            node_ID = node_ID,
            data = kwargs["data"] if ("data") in kwargs.keys() else {},
            relation_claims = set()
        )
        node_.__hash__()
        debug.Debug_Tools.debug_msg('{} is created'.format(node_), True)
        
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
                from_node.relation_claims.add(relation)
            if rel_to_to_from != None:
                relation = structure.node_structs.Relation_Claim_Struct(
                    to_node = to_node,
                    relation = structure.node_structs.Relation_Struct(relation_name = rel_to_to_from),
                    rel_direction = 'to_to_from'
                )
                from_node.relation_claims.add(relation)
        for to_node_ in to_nodes:
            add_relation(from_node, to_node_, rel_from_to_to, rel_to_to_from)
           
    @staticmethod
    def accept_relations(node_:structure.node_structs.Node_Struct, from_nodes:List[structure.node_structs.Node_Struct]):
        """ if from_nodes has relation claims towards node_ , create counter claims
            Arguments:
                node_ {structure.node_structs.Node_Struct} -- [description]
                from_nodes {List[structure.node_structs.Node_Struct]} -- [description]
        """
        debug.Debug_Tools.debug_msg('Node accept_relations started')
        for from_node in from_nodes:
            for relation in from_node.relation_claims:
                if relation.to_node == node_:
                    if relation.rel_direction == 'to_to_from':
                        Node_Manager.claim_relations(from_node = node_, to_nodes = [from_node], rel_from_to_to=relation.relation.relation_name)
                    elif relation.rel_direction == 'from_to_to':
                        Node_Manager.claim_relations(from_node = node_, to_nodes = [from_node], rel_to_to_from = relation.relation.relation_name)
        debug.Debug_Tools.debug_msg('Node accept_relations ended')
                    
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
    def get_rel_node(
        node_ : structure.node_structs.Node_Struct, 
        hash_deep: List[int]=None, 
        nodeID_deep: List[structure.node_structs.Node_ID_Struct]=None,
        data_deep: List[dict]=None):
        """[summary]
            
            Arguments:
                node_ {structure.node_structs.Node_Struct} -- [description]
            
            Keyword Arguments:
                hash_deep {List[int]} -- [description] (default: {None})
                nodeID_deep {List[structure.node_structs.Node_ID_Struct]} -- [description] (default: {None})
                data_deep {List[dict]} -- [description] (default: {None})
            
            Returns:
                [type] -- [description]
        """
        def _get_rel_node(
            node_ : structure.node_structs.Node_Struct, 
            hash_shallow:int=None, 
            nodeID_shallow: structure.node_structs.Node_ID_Struct=None,
            data_shallow: dict=None):
            """[summary]
                
                Arguments:
                    node_ {structure.node_structs.Node_Struct} -- [description]
                
                Keyword Arguments:
                    hash_shallow {int} -- [description] (default: {None})
                    nodeID_shallow {structure.node_structs.Node_ID_Struct} -- [description] (default: {None})
                    data_shallow {dict} -- [description] (default: {None})
                
                Returns:
                    [type] -- [description]
            """
            # only first order relations
            ret_node_ = None
            if hash_shallow != None:
                for relation_claim in node_.relation_claims:
                    if hash_shallow == relation_claim.to_node._hash:
                        ret_node_ = relation_claim.to_node
                        break
            elif nodeID_shallow != None:
                # if only ID is given and not node_name
                for relation_claim in node_.relation_claims:
                    if nodeID_shallow['ID'] == relation_claim.to_node.node_ID.ID:
                        ret_node_ = relation_claim.to_node
                        break # hoping there are no duplicates
            elif data_shallow != None:
                for relation_claim in node_.relation_claims:
                    do_ret = True
                    for key in data_shallow.keys():
                        if key in relation_claim.to_node.data.keys():
                            if data_shallow[key] != relation_claim.to_node.data[key]:
                                do_ret = False
                                break
                    if do_ret:
                        ret_node_ = relation_claim.to_node
                        break
            
            return ret_node_
        ret_node_ = None
        if hash_deep != None:
            ret_node_ = _get_rel_node(node_, hash_shallow=hash_deep[0])
            for i in hash_deep[1:]:
                ret_node_ = _get_rel_node(node_, hash_shallow=i)
        elif nodeID_deep != None:
            ret_node_ = _get_rel_node(node_, nodeID_shallow=nodeID_deep[0])
            for i in nodeID_deep[1:]:
                ret_node_ = _get_rel_node(node_, nodeID_shallow=i)
        elif data_deep != None:
            ret_node_ = _get_rel_node(node_, data_shallow=data_deep[0])
            for i in data_deep[1:]:
                ret_node_ = _get_rel_node(node_, data_shallow=i)
        return ret_node_
    
    @staticmethod
    def get_rel_nodes(
        node_, 
        hash_deep_list: List[List[int]]=None, 
        nodeID_deep_list: List[List[structure.node_structs.Node_ID_Struct]]=None,
        data_deep_list: List[List[dict]] = None):
        
        _nodes : List[structure.node_structs.Node_Struct] = []
        if hash_deep_list!=None:
            for hash_deep in hash_deep_list:
                _nodes.append(Node_Manager.get_rel_node(node_, hash_deep=hash_deep))
        elif nodeID_deep_list!=None:
            for nodeID_deep in nodeID_deep_list:
                _nodes.append(Node_Manager.get_rel_node(node_, nodeID_deep=nodeID_deep))
        elif data_deep_list!=None:
            for data_deep in data_deep_list:
                _nodes.append(Node_Manager.get_rel_node(node_, data_deep=data_deep))
        
        return _nodes
    
    @staticmethod
    def describe(node_ : structure.node_structs.Node_Struct, to_node_data_keys:list = None, mode:str = None, describer_ = print, describer_args: list = None):
        # describe self.node_data
        def describer(msg=''):
            if describer_args == None:
                describer_(msg)
            else:
                describer_(msg, *describer_args)
            # TODO support **kwargs also
            
        describer()
        describer("-----------------------------------------------------------")
        if mode == 'compact':
            describer("FROM : {}".format(node_.node_ID))
            describer("---- DATA ----")
            describer(node_.data)
            describer("---- RELATIONS ----")
            for count,relation_claim in enumerate(node_.relation_claims):
                describer("\n-- relation {} :".format(count))
                #print('from_node : ', _.from_node.node_ID)
                describer('to_node : {}'.format(relation_claim.to_node.node_ID))
                if to_node_data_keys != None:
                    data = [ (key,relation_claim.to_node.data[key]) if key in relation_claim.to_node.data.keys() else ('','') for key in to_node_data_keys ]
                    data = dict(data)
                    describer('   to_node_data: {}'.format(data))
                describer('{} = {}'.format(relation_claim.rel_direction, relation_claim.relation.relation_name))
        else:
            describer("FROM : {}".format(node_.node_ID))
            describer("---- DATA ----")
            for data_ in node_.data.items():
                describer("{} : {}".format(data_[0],data_[1]))
            describer("---- RELATIONS ----")
            for count,relation_claim in enumerate(node_.relation_claims):
                describer("\n-- relation {} :".format(count))
                describer('to_node')
                describer( relation_claim.to_node.node_ID)
                if to_node_data_keys != None:
                    for key in to_node_data_keys:
                        if key in relation_claim.to_node.data.keys():
                            describer((key,relation_claim.to_node.data[key]))
                        else:
                            describer(())
                describer('relation_name = {}\nrel_direction = {}'.format(relation_claim.relation.relation_name, relation_claim.rel_direction))

class Node_Pack:
    @staticmethod
    def create_pack(seed_node: structure.node_structs.Node_Struct):
        """
        creates a list of nodes from a related collected of nodes using a seed_node

        Arguments:
            seed_node {structure.node_structs.Node_Struct} -- any node that is related to the collection of related nodes
        
        Returns:
            [type] -- [description]
        """
        debug.Debug_Tools.debug_msg('Nodepack create_pack started')
        
        nodePack_ = structure.node_structs.NodePack_Struct(
            pack = set()
        )
        nodePack_.pack.add(seed_node)
        def add_relations(node_: structure.node_structs.Node_Struct):
            for relation in node_.relation_claims:
                if relation.to_node not in nodePack_.pack:
                    nodePack_.pack.add(relation.to_node)
                    add_relations(relation.to_node)
        add_relations(seed_node)
        
        debug.Debug_Tools.debug_msg('Nodepack create_pack ended')
        return nodePack_
    
    @staticmethod
    def generate_IDs(nodePack_ : structure.node_structs.NodePack_Struct):
        debug.Debug_Tools.debug_msg('Nodepack generate_IDs started',True)
        def generate_relative(nodePack_ : structure.node_structs.NodePack_Struct):
            """ NOTE currently nodepack is a list, each item in a list already has a unique index.
            But Im looking to make nodepack into a unordered set or something.
            """
            pass
        debug.Debug_Tools.debug_msg('Nodepack generate_IDs ended',True)
    
    @staticmethod
    def describe(nodePack_ : structure.node_structs.NodePack_Struct, to_node_data_keys:list = None, mode:str = None, describer_ = print, describer_args: list = None):
        debug.Debug_Tools.debug_msg('Nodepack describe started',True)
        for node_ in nodePack_.pack:
            Node_Manager.describe(
                node_= node_, 
                to_node_data_keys = to_node_data_keys,
                mode = mode, 
                describer_ = describer_, 
                describer_args = describer_args)
        debug.Debug_Tools.debug_msg('Nodepack describe ended',True)

