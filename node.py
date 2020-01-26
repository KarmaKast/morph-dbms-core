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
import uuid

#import nodeLib
from . import structure
from .debug import Debug_Tools


def create_node(node_ID: dict, data=None, relation_claims: Set[structure.node_structs.RelationClaimStruct] = None):
    """[kwargs]
    node_ID
    data
    relation_claims
    """
    _ID = node_ID['ID'] if 'ID' in node_ID.keys() else str(uuid.uuid1())
    node_ = structure.node_structs.NodeStruct(
        node_ID=structure.node_structs.NodeIdStruct(
            ID=_ID,
            node_label=node_ID['node_label'] if 'node_label' in node_ID.keys() else None),
        data=data if data != None else dict(),
        relation_claims=relation_claims if relation_claims != None else set()
    )

    node_.__hash__()
    Debug_Tools.debug_msg('{} is created'.format(node_), True)
    Debug_Tools.debug_msg("%s" % (id(node_.relation_claims)), False)

    return node_


def add_relation(check_nodes: Set[structure.node_structs.NodeStruct],
                 rel_self_to_to: str = None,
                 rel_to_to_self: str = None):

    relations:  Dict[structure.node_structs.RelationStruct] = dict()

    if rel_self_to_to != None:
        exists = False
        for node_ in check_nodes:
            # DOING check if relation is already exists in this node
            for relation_claim in node_.relation_claims:
                if rel_self_to_to == relation_claim.relation.relation_name:
                    exists = True
                    relations['from_self'] = relation_claim.relation
                    break
        if not exists:
            relation = structure.node_structs.RelationStruct(
                ID = uuid.uuid1(),
                relation_name=rel_self_to_to)
            relation.__hash__()
            relations['from_self'] = relation

    if rel_to_to_self != None:
        exists = False
        for node_ in check_nodes:
            # TODO check if relation is already exists in this node
            for relation_claim in node_.relation_claims:
                if rel_to_to_self == relation_claim.relation.relation_name:
                    exists = True
                    relations['to_self'] = relation_claim.relation
                    break
        if not exists:
            relation = structure.node_structs.RelationStruct(
                ID = uuid.uuid1(),
                relation_name=rel_to_to_self)
            relation.__hash__()
            relations['to_self'] = relation

    return relations


def add_relation_claim(node_: structure.node_structs.NodeStruct,
                       to_node: structure.node_structs.NodeStruct,
                       relation: structure.node_structs.RelationStruct = None,
                       direction: str = None):

    # check if node_ and to_node_ is same
    if node_._hash == to_node._hash:
        Debug_Tools.debug_msg('node and to_node same. How?')

    relation_claims: Set[structure.node_structs.RelationStruct] = set()

    relation_claim = structure.node_structs.RelationClaimStruct(
        to_node=to_node,
        relation=relation,
        rel_direction=direction
    )
    relation_claims.add(relation_claim)
    return relation_claims


def claim_relation(node_: structure.node_structs.NodeStruct,
                   to_node: structure.node_structs.NodeStruct,
                   relation=None,
                   direction=None,):
    # todo: if to_cluster is not given check if to_node belongs to this cluster 
    relation_claims = add_relation_claim(
        node_, to_node, relation, direction)
    node_.relation_claims.update(relation_claims)


def accept_relations(node_: structure.node_structs.NodeStruct, node_s: Set[structure.node_structs.NodeStruct]):
    """ if nodes from node_s has relation claims towards node_ , create counter claims in to_node_
        Arguments:
            to_node_ {structure.node_structs.NodeStruct} -- [description]
            node_s {List[structure.node_structs.NodeStruct]} -- [description]
    """
    Debug_Tools.debug_msg('Node accept_relations started')
    for node_ in node_s:
        for relation in node_.relation_claims:
            # check if node_ has a relation claim towards node_
            """
            if relation.to_node == node_:
                # instead of changing with the set during iteration
                if relation.rel_direction == 'to_to_self':
                    claim_relations(node_=node_, to_nodes=[
                                                    node_], rel_self_to_to=relation.relation.relation_name)
                elif relation.rel_direction == 'self_to_to':
                    claim_relations(node_=node_, to_nodes=[
                                                    node_], rel_to_to_self=relation.relation.relation_name)
            """
    Debug_Tools.debug_msg('Node accept_relations ended')


def create_related_node(node_: structure.node_structs.NodeStruct,
                        to_node_ID: structure.node_structs.NodeIdStruct = None,
                        data: dict = None,
                        relations_self_to_to: str = None,
                        relations_to_to_self: str = None):
    """
        use create_node() and then add relation_claims btw them
        [kwargs]
            node_
            node_ID
            data
            rel_self_to_to
            rel_to_to_self
    """
    new_node_ = create_node(node_ID=to_node_ID, data=data)

    for rel_self_to_to in relations_self_to_to:
        claim_relations(
            node_=node_,
            to_nodes=[new_node_],
            relation=rel_self_to_to,
            rel_self_to_to=True,
        )
    for rel_to_to_self in relations_to_to_self:
        claim_relations(
            node_=node_,
            to_nodes=[new_node_],
            relation=rel_to_to_self,
            rel_to_to_self=True,
        )

    return new_node_


def get_rel_node(
        node_: structure.node_structs.NodeStruct,
        hash_deep: List[int] = None,
        nodeID_deep: List[structure.node_structs.NodeIdStruct] = None,
        data_deep: List[dict] = None):
    """[summary]

        Arguments:
            node_ {structure.node_structs.NodeStruct} -- [description]

        Keyword Arguments:
            hash_deep {List[int]} -- [description] (default: {None})
            nodeID_deep {List[structure.node_structs.NodeIdStruct]} -- [description] (default: {None})
            data_deep {List[dict]} -- [description] (default: {None})

        Returns:
            [type] -- [description]
    """
    # TODO deal with wrong inputs
    def _get_rel_node(
            node_: structure.node_structs.NodeStruct,
            hash_shallow: int = None,
            nodeID_shallow: structure.node_structs.NodeIdStruct = None,
            data_shallow: dict = None):
        """[summary]

            Arguments:
                node_ {structure.node_structs.NodeStruct} -- [description]

            Keyword Arguments:
                hash_shallow {int} -- [description] (default: {None})
                nodeID_shallow {structure.node_structs.NodeIdStruct} -- [description] (default: {None})
                data_shallow {dict} -- [description] (default: {None})

            Returns:
                [type] -- [description]
        """
        # only first order relations
        ret_node_ = None
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


def get_rel_nodes(
        node_,
        hash_deep_list: List[List[int]] = None,
        nodeID_deep_list: List[List[structure.node_structs.NodeIdStruct]] = None,
        data_deep_list: List[List[dict]] = None):

    _nodes: List[structure.node_structs.NodeStruct] = []
    if hash_deep_list != None:
        for hash_deep in hash_deep_list:
            _nodes.append(get_rel_node(
                node_, hash_deep=hash_deep))
    elif nodeID_deep_list != None:
        for nodeID_deep in nodeID_deep_list:
            _nodes.append(get_rel_node(
                node_, nodeID_deep=nodeID_deep))
    elif data_deep_list != None:
        for data_deep in data_deep_list:
            _nodes.append(get_rel_node(
                node_, data_deep=data_deep))

    return _nodes


def describe(node_: structure.node_structs.NodeStruct, to_node_data_keys: list = None, mode: str = None, describer_=print, describer_args: list = None):
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
            #print('node_ : ', _.node_.node_ID)
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


def delete_node(node_: structure.node_structs.NodeStruct, mode=None):
    # objects cannot be directly deleted in python. If nothing is referencing the object its deleted
    return None
