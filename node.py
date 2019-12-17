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

from typing import List, Set, Dict, Any

#import nodeLib
from . import structure
from .debug import Debug_Tools


class Node_Manager:

    @staticmethod
    def create_node(**kwargs):
        """[kwargs]
        node_ID
        data
        relation_claims
        """
        node_ID: structure.node_structs.Node_ID_Struct
        if {"node_ID"}.issubset(kwargs.keys()):
            node_ID = structure.node_structs.Node_ID_Struct(
                ID=kwargs['node_ID']['ID'] if 'ID' in kwargs['node_ID'].keys(
                ) else None,
                node_name=kwargs['node_ID']['node_name'] if 'node_name' in kwargs['node_ID'].keys(
                ) else None
            )
        else:
            node_ID = structure.node_structs.Node_ID_Struct(
                ID=None,
                node_name=None
            )
        node_ = structure.node_structs.Node_Struct(
            node_ID=node_ID,
            data=kwargs["data"] if ("data") in kwargs.keys() else {},
            relation_claims=set()
        )
        node_.__hash__()
        Debug_Tools.debug_msg('{} is created'.format(node_), True)

        return node_

    @staticmethod
    def add_relation(check_nodes: Set[structure.node_structs.Node_Struct],
                     rel_from_to_to: str = None,
                     rel_to_to_from: str = None):

        relations:  Dict[structure.node_structs.Relation_Struct] = dict()

        if rel_from_to_to != None:
            exists = False
            for node_ in check_nodes:
                # TODO check if relation is already exists in this node
                for relation_claim in node_.relation_claims:
                    if rel_from_to_to == relation_claim.relation.relation_name:
                        exists = True
                        relations['from_to_to'] = relation_claim.relation
                        break
            if not exists:
                relation = structure.node_structs.Relation_Struct(
                    relation_name=rel_from_to_to)
                relation.__hash__()
                relations['from_to_to'] = relation

        if rel_to_to_from != None:
            exists = False
            for node_ in check_nodes:
                # TODO check if relation is already exists in this node
                for relation_claim in node_.relation_claims:
                    if rel_to_to_from == relation_claim.relation.relation_name:
                        exists = True
                        relations['to_to_from'] = relation_claim.relation
                        break
            if not exists:
                relation = structure.node_structs.Relation_Struct(
                    relation_name=rel_to_to_from)
                relation.__hash__()
                relations['to_to_from'] = relation

        return relations

    @staticmethod
    def add_relation_claim(from_node: structure.node_structs.Node_Struct,
                           to_node: structure.node_structs.Node_Struct,
                           rel_from_to_to: str = None,
                           rel_to_to_from: str = None):

        relations = Node_Manager.add_relation(
            [from_node, to_node], rel_from_to_to, rel_to_to_from)
        Debug_Tools.debug_msg(relations)

        relation_claims: Set[structure.node_structs.Relation_Struct] = set()
        if rel_from_to_to != None:
            exists = False  # TODO check if relation claim already exists in from_node
            for relation_claim in from_node.relation_claims:
                bools = [False, False, False]
                if relation_claim.to_node == to_node:
                    assert relation_claim.to_node._hash == to_node._hash
                    bools[0] = True
                if relation_claim.relation.relation_name == relations['from_to_to']:
                    assert relation_claim.relation._hash == relations['from_to_to']._hash
                    bools[1] = True
                if relation_claim.rel_direction == 'from_to_to':
                    bools[2] = True
                if bools[0] and bools[1] and bools[2]:
                    exists = True
                    relation_claims.add(relation_claim)
                    break

            if not exists:
                relation:  structure.node_structs.Relation_Struct = relations['from_to_to']
                relation_claim = structure.node_structs.Relation_Claim_Struct(
                    to_node=to_node,
                    relation=relation,
                    rel_direction='from_to_to'
                )
                # relation_claim.__hash__()
                relation_claims.add(relation_claim)

        if rel_to_to_from != None:
            exists = False  # TODO check if relation claim already exists in from_node
            for relation_claim in from_node.relation_claims:
                bools = [False, False, False]
                if relation_claim.to_node == to_node:
                    assert relation_claim.to_node._hash == to_node._hash
                    bools[0] = True
                if relation_claim.relation.relation_name == relations['to_to_from']:
                    assert relation_claim.relation._hash == relations['to_to_from']._hash
                    bools[1] = True
                if relation_claim.rel_direction == 'to_to_from':
                    bools[2] = True
                if bools[0] and bools[1] and bools[2]:
                    exists = True
                    relation_claims.add(relation_claim)
                    break

            if not exists:
                relation:  structure.node_structs.Relation_Struct = relations['to_to_from']
                relation_claim = structure.node_structs.Relation_Claim_Struct(
                    to_node=to_node,
                    relation=relation,
                    rel_direction='to_to_from'
                )
                # relation_claim.__hash__()
                relation_claims.add(relation_claim)
            Debug_Tools.debug_msg(relation_claims)
        return relation_claims

    @staticmethod
    def claim_relations(from_node: structure.node_structs.Node_Struct,
                        to_nodes: Set[structure.node_structs.Node_Struct],
                        rel_from_to_to: str = None,
                        rel_to_to_from: str = None):
        for to_node_ in to_nodes:
            relation_claims = Node_Manager.add_relation_claim(
                from_node, to_node_, rel_from_to_to, rel_to_to_from)
            from_node.relation_claims.update(relation_claims)

    @staticmethod
    def accept_relations(node_: structure.node_structs.Node_Struct, from_nodes: List[structure.node_structs.Node_Struct]):
        """ if from_nodes has relation claims towards node_ , create counter claims
            Arguments:
                node_ {structure.node_structs.Node_Struct} -- [description]
                from_nodes {List[structure.node_structs.Node_Struct]} -- [description]
        """
        Debug_Tools.debug_msg('Node accept_relations started')
        for from_node in from_nodes:
            for relation in from_node.relation_claims:
                if relation.to_node == node_:
                    if relation.rel_direction == 'to_to_from':
                        Node_Manager.claim_relations(from_node=node_, to_nodes=[
                                                     from_node], rel_from_to_to=relation.relation.relation_name)
                    elif relation.rel_direction == 'from_to_to':
                        Node_Manager.claim_relations(from_node=node_, to_nodes=[
                                                     from_node], rel_to_to_from=relation.relation.relation_name)
        Debug_Tools.debug_msg('Node accept_relations ended')

    @staticmethod
    def create_related_node(from_node: structure.node_structs.Node_Struct,
                            node_ID: structure.node_structs.Node_ID_Struct = None,
                            data: dict = None,
                            rel_from_to_to: str = None,
                            rel_to_to_from: str = None):
        """
            use create_node() and then add relation_claims btw them
            [kwargs]
                from_node
                node_ID
                data
                rel_from_to_to
                rel_to_to_from
        """
        new_node_ = Node_Manager.create_node(node_ID=node_ID, data=data)

        Node_Manager.claim_relations(
            from_node=from_node,
            to_nodes=[new_node_],
            rel_from_to_to=rel_from_to_to,
            rel_to_to_from=rel_to_to_from
        )
        Node_Manager.claim_relations(
            from_node=new_node_,
            to_nodes=[from_node],
            rel_from_to_to=rel_to_to_from,
            rel_to_to_from=rel_from_to_to
        )

        return new_node_

    @staticmethod
    def get_rel_node(
            node_: structure.node_structs.Node_Struct,
            hash_deep: List[int] = None,
            nodeID_deep: List[structure.node_structs.Node_ID_Struct] = None,
            data_deep: List[dict] = None):
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
                node_: structure.node_structs.Node_Struct,
                hash_shallow: int = None,
                nodeID_shallow: structure.node_structs.Node_ID_Struct = None,
                data_shallow: dict = None):
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
            for relation_claim in node_.relation_claims:
                if hash_shallow != None:
                    if hash_shallow == relation_claim.to_node._hash:
                        ret_node_ = relation_claim.to_node
                        break
                elif nodeID_shallow != None:
                    # if only ID is given and not node_name
                    if nodeID_shallow['ID'] == relation_claim.to_node.node_ID.ID:
                        ret_node_ = relation_claim.to_node
                        break  # hoping there are no duplicates
                    # TODO if only node_name is give
                    # TODO if both ID and node_name is given
                elif data_shallow != None:
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
            hash_deep_list: List[List[int]] = None,
            nodeID_deep_list: List[List[structure.node_structs.Node_ID_Struct]] = None,
            data_deep_list: List[List[dict]] = None):

        _nodes: List[structure.node_structs.Node_Struct] = []
        if hash_deep_list != None:
            for hash_deep in hash_deep_list:
                _nodes.append(Node_Manager.get_rel_node(
                    node_, hash_deep=hash_deep))
        elif nodeID_deep_list != None:
            for nodeID_deep in nodeID_deep_list:
                _nodes.append(Node_Manager.get_rel_node(
                    node_, nodeID_deep=nodeID_deep))
        elif data_deep_list != None:
            for data_deep in data_deep_list:
                _nodes.append(Node_Manager.get_rel_node(
                    node_, data_deep=data_deep))

        return _nodes

    @staticmethod
    def describe(node_: structure.node_structs.Node_Struct, to_node_data_keys: list = None, mode: str = None, describer_=print, describer_args: list = None):
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
            for count, relation_claim in enumerate(node_.relation_claims):
                describer("\n-- relation {} :".format(count))
                #print('from_node : ', _.from_node.node_ID)
                describer('to_node : {}'.format(
                    relation_claim.to_node.node_ID))
                if to_node_data_keys != None:
                    data = [(key, relation_claim.to_node.data[key]) if key in relation_claim.to_node.data.keys(
                    ) else ('', '') for key in to_node_data_keys]
                    data = dict(data)
                    describer('   to_node_data: {}'.format(data))
                describer('{} = {}'.format(relation_claim.rel_direction,
                                           relation_claim.relation.relation_name))
        else:
            describer("FROM : {}".format(node_.node_ID))
            describer("---- DATA ----")
            for data_ in node_.data.items():
                describer("{} : {}".format(data_[0], data_[1]))
            describer("---- RELATIONS ----")
            for count, relation_claim in enumerate(node_.relation_claims):
                describer("\n-- relation {} :".format(count))
                describer('to_node')
                describer(relation_claim.to_node.node_ID)
                if to_node_data_keys != None:
                    for key in to_node_data_keys:
                        if key in relation_claim.to_node.data.keys():
                            describer((key, relation_claim.to_node.data[key]))
                        else:
                            describer(())
                describer('relation_name = {}\nrel_direction = {}'.format(
                    relation_claim.relation.relation_name, relation_claim.rel_direction))

    @staticmethod
    def delete_node(node_: structure.node_structs.Node_Struct, mode=None):
        # objects cannot be directly deleted in python. If nothing is referencing the object its deleted
        return None


class Node_Pack:
    @staticmethod
    def create_pack(seed_node: structure.node_structs.Node_Struct = None, packName=None):
        """
        creates a list of nodes from a related collected of nodes using a seed_node

        Arguments:
            seed_node {structure.node_structs.Node_Struct} -- any node that is related to the collection of related nodes

        Returns:
            [type] -- [description]
        """
        Debug_Tools.debug_msg('Nodepack create_pack started')

        nodePack_ = structure.node_structs.NodePack_Struct(
            packName=packName,
            pack=set()
        )
        if seed_node != None:
            nodePack_.pack.add(seed_node)

            def add_relations(node_: structure.node_structs.Node_Struct):
                for relation in node_.relation_claims:
                    if relation.to_node not in nodePack_.pack:
                        nodePack_.pack.add(relation.to_node)
                        add_relations(relation.to_node)
            add_relations(seed_node)

        Debug_Tools.debug_msg('Nodepack create_pack ended')
        return nodePack_

    @staticmethod
    def refresh_pack(node_pack):
        pass

    @staticmethod
    def generate_IDs(nodePack_: structure.node_structs.NodePack_Struct):
        Debug_Tools.debug_msg('Nodepack generate_IDs started', True)

        def generate_relative(nodePack_: structure.node_structs.NodePack_Struct):
            """ NOTE currently nodepack is a list, each item in a list already has a unique index.
            But Im looking to make nodepack into a unordered set or something.
            """
            pass
        Debug_Tools.debug_msg('Nodepack generate_IDs ended', True)

    @staticmethod
    def describe(nodePack_: structure.node_structs.NodePack_Struct, to_node_data_keys: list = None, mode: str = None, describer_=print, describer_args: list = None):
        Debug_Tools.debug_msg('Nodepack describe started', True)
        print('Pack name: {}'.format(nodePack_.packName))
        for node_ in nodePack_.pack:
            Node_Manager.describe(
                node_=node_,
                to_node_data_keys=to_node_data_keys,
                mode=mode,
                describer_=describer_,
                describer_args=describer_args)
        Debug_Tools.debug_msg('Nodepack describe ended', True)


class Model:

    # @staticmethod
    pass
