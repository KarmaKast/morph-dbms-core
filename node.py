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
    def create_node(node_ID: structure.node_structs.NodeIdStruct, data={}, relation_claims=set()):
        """[kwargs]
        node_ID
        data
        relation_claims
        """
        node_ = structure.node_structs.NodeStruct(
            node_ID=structure.node_structs.NodeIdStruct(
                ID=node_ID['ID'] if 'ID' in node_ID.keys() else 0,
                node_label=node_ID['node_name'] if 'node_name' in node_ID.keys() else None),
            data=data,
            relation_claims=relation_claims
        )

        node_.__hash__()
        Debug_Tools.debug_msg('{} is created'.format(node_), True)

        return node_

    @staticmethod
    def add_relation(check_nodes: Set[structure.node_structs.NodeStruct],
                     rel_from_to_self: str = None,
                     rel_self_to_from: str = None):

        relations:  Dict[structure.node_structs.RelationStruct] = dict()

        if rel_from_to_self != None:
            exists = False
            for node_ in check_nodes:
                # TODO check if relation is already exists in this node
                for relation_claim in node_.relation_claims:
                    if rel_from_to_self == relation_claim.relation.relation_name:
                        exists = True
                        relations['from_to_self'] = relation_claim.relation
                        break
            if not exists:
                relation = structure.node_structs.RelationStruct(
                    relation_name=rel_from_to_self)
                relation.__hash__()
                relations['from_to_self'] = relation

        if rel_self_to_from != None:
            exists = False
            for node_ in check_nodes:
                # TODO check if relation is already exists in this node
                for relation_claim in node_.relation_claims:
                    if rel_self_to_from == relation_claim.relation.relation_name:
                        exists = True
                        relations['self_to_from'] = relation_claim.relation
                        break
            if not exists:
                relation = structure.node_structs.RelationStruct(
                    relation_name=rel_self_to_from)
                relation.__hash__()
                relations['self_to_from'] = relation

        return relations

    @staticmethod
    def add_relation_claim(from_node: structure.node_structs.NodeStruct,
                           to_node: structure.node_structs.NodeStruct,
                           rel_from_to_self: str = None,
                           rel_self_to_from: str = None):

        relations = Node_Manager.add_relation(
            [from_node, to_node], rel_from_to_self, rel_self_to_from)
        Debug_Tools.debug_msg(relations)

        relation_claims: Set[structure.node_structs.RelationStruct] = set()
        if rel_from_to_self != None:
            exists = False  # TODO check if relation claim already exists in from_node
            for relation_claim in from_node.relation_claims:
                bools = [False, False, False]
                if relation_claim.to_node == to_node:
                    assert relation_claim.to_node._hash == to_node._hash
                    bools[0] = True
                if relation_claim.relation.relation_name == relations['from_to_self']:
                    assert relation_claim.relation._hash == relations['from_to_self']._hash
                    bools[1] = True
                if relation_claim.rel_direction == 'from_to_self':
                    bools[2] = True
                if bools[0] and bools[1] and bools[2]:
                    exists = True
                    relation_claims.add(relation_claim)
                    break

            if not exists:
                relation:  structure.node_structs.RelationStruct = relations['from_to_self']
                relation_claim = structure.node_structs.RelationClaimStruct(
                    to_node=to_node,
                    relation=relation,
                    rel_direction='from_to_self'
                )
                # relation_claim.__hash__()
                relation_claims.add(relation_claim)

        if rel_self_to_from != None:
            exists = False  # TODO check if relation claim already exists in from_node
            for relation_claim in from_node.relation_claims:
                bools = [False, False, False]
                if relation_claim.to_node == to_node:
                    assert relation_claim.to_node._hash == to_node._hash
                    bools[0] = True
                if relation_claim.relation.relation_name == relations['self_to_from']:
                    assert relation_claim.relation._hash == relations['self_to_from']._hash
                    bools[1] = True
                if relation_claim.rel_direction == 'self_to_from':
                    bools[2] = True
                if bools[0] and bools[1] and bools[2]:
                    exists = True
                    relation_claims.add(relation_claim)
                    break

            if not exists:
                relation:  structure.node_structs.RelationStruct = relations['self_to_from']
                relation_claim = structure.node_structs.RelationClaimStruct(
                    to_node=to_node,
                    relation=relation,
                    rel_direction='self_to_from'
                )
                # relation_claim.__hash__()
                relation_claims.add(relation_claim)
            Debug_Tools.debug_msg(relation_claims)
        return relation_claims

    @staticmethod
    def claim_relations(from_node: structure.node_structs.NodeStruct,
                        to_nodes: Set[structure.node_structs.NodeStruct],
                        rel_from_to_self: str = None,
                        rel_self_to_from: str = None):
        for to_node_ in to_nodes:
            relation_claims = Node_Manager.add_relation_claim(
                from_node, to_node_, rel_from_to_self, rel_self_to_from)
            from_node.relation_claims.update(relation_claims)

    @staticmethod
    def accept_relations(node_: structure.node_structs.NodeStruct, from_nodes: Set[structure.node_structs.NodeStruct]):
        """ if nodes from from_nodes has relation claims towards node_ , create counter claims in to_node_
            Arguments:
                to_node_ {structure.node_structs.NodeStruct} -- [description]
                from_nodes {List[structure.node_structs.NodeStruct]} -- [description]
        """
        Debug_Tools.debug_msg('Node accept_relations started')
        for from_node in from_nodes:
            for relation in from_node.relation_claims:
                # check if from_node has a relation claim towards node_
                """
                if relation.to_node == node_:
                    # instead of changing with the set during iteration
                    if relation.rel_direction == 'self_to_from':
                        Node_Manager.claim_relations(from_node=node_, to_nodes=[
                                                     from_node], rel_from_to_self=relation.relation.relation_name)
                    elif relation.rel_direction == 'from_to_self':
                        Node_Manager.claim_relations(from_node=node_, to_nodes=[
                                                     from_node], rel_self_to_from=relation.relation.relation_name)
                """
        Debug_Tools.debug_msg('Node accept_relations ended')

    @staticmethod
    def create_related_node(from_node: structure.node_structs.NodeStruct,
                            node_ID: structure.node_structs.NodeIdStruct = None,
                            data: dict = None,
                            rel_from_to_self: str = None,
                            rel_self_to_from: str = None):
        """
            use create_node() and then add relation_claims btw them
            [kwargs]
                from_node
                node_ID
                data
                rel_from_to_self
                rel_self_to_from
        """
        new_node_ = Node_Manager.create_node(node_ID=node_ID, data=data)

        Node_Manager.claim_relations(
            from_node=from_node,
            to_nodes=[new_node_],
            rel_from_to_self=rel_from_to_self,
            rel_self_to_from=rel_self_to_from
        )
        Node_Manager.claim_relations(
            from_node=new_node_,
            to_nodes=[from_node],
            rel_from_to_self=rel_self_to_from,
            rel_self_to_from=rel_from_to_self
        )

        return new_node_

    @staticmethod
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

    @staticmethod
    def get_rel_nodes(
            node_,
            hash_deep_list: List[List[int]] = None,
            nodeID_deep_list: List[List[structure.node_structs.NodeIdStruct]] = None,
            data_deep_list: List[List[dict]] = None):

        _nodes: List[structure.node_structs.NodeStruct] = []
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
    def delete_node(node_: structure.node_structs.NodeStruct, mode=None):
        # objects cannot be directly deleted in python. If nothing is referencing the object its deleted
        return None


class Node_Cluster:
    @staticmethod
    def create_cluster(seed_node: structure.node_structs.NodeStruct = None, cluster_name=None):
        """
        creates a list of nodes from a related collected of nodes using a seed_node

        Arguments:
            seed_node {structure.node_structs.NodeStruct} -- any node that is related to the collection of related nodes

        Returns:
            [type] -- [description]
        """
        Debug_Tools.debug_msg('NodeCluster create_cluster started')

        nodeCluster_ = structure.node_structs.NodeClusterStruct(
            cluster_name=cluster_name,
            cluster=set()
        )
        if seed_node != None:
            nodeCluster_.cluster.add(seed_node)

            def add_relations(node_: structure.node_structs.NodeStruct):
                for relation in node_.relation_claims:
                    if relation.to_node not in nodeCluster_.cluster:
                        nodeCluster_.cluster.add(relation.to_node)
                        add_relations(relation.to_node)
            add_relations(seed_node)

        Debug_Tools.debug_msg('NodeCluster create_cluster ended')
        return nodeCluster_

    @staticmethod
    def refresh_cluster(node_Cluster):
        pass

    @staticmethod
    def generate_IDs(nodeCluster_: structure.node_structs.NodeClusterStruct):
        Debug_Tools.debug_msg('NodeCluster generate_IDs started', True)

        def generate_relative(nodeCluster_: structure.node_structs.NodeClusterStruct):
            """ NOTE all nodes in the loaded into the memory most likely already has relatively unique hashes.
            The point of this function is to not depend on that mechanism to guaranty relatively unique hashes.
            """
            pass
        Debug_Tools.debug_msg('NodeCluster generate_IDs ended', True)

    @staticmethod
    def describe(node_cluster: structure.node_structs.NodeClusterStruct, to_node_data_keys: list = None, mode: str = None, describer_=print, describer_args: list = None):
        Debug_Tools.debug_msg('NodeCluster describe started', True)
        describer_('Cluster name: {}'.format(node_cluster.cluster_name))
        for node_ in node_cluster.cluster:
            Node_Manager.describe(
                node_=node_,
                to_node_data_keys=to_node_data_keys,
                mode=mode,
                describer_=describer_,
                describer_args=describer_args)
        Debug_Tools.debug_msg('NodeCluster describe ended', True)


class Model:

    # @staticmethod
    pass
