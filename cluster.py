from typing import List, Set, Dict, Any
import uuid

from . import structure
from .debug import Debug_Tools
from . import node


def create_cluster(cluster_name=None,
                   ID=None,
                   nodes_: Set[structure.node_structs.NodeStruct] = None,
                   relations_: Set[structure.node_structs.RelationStruct] = None):
    """
    creates a list of nodes from a related collected of nodes using a nodes_

    Arguments:
        nodes_ {structure.node_structs.NodeStruct} -- any node that is related to the collection of related nodes

    Returns:
        [type] -- [description]
    """
    Debug_Tools.debug_msg('NodeCluster create_cluster started', False)

    nodeCluster_ = structure.node_structs.NodeClusterStruct(
        ID=ID if ID != None else str(uuid.uuid1()),
        cluster_name=cluster_name,
        nodes=dict(),
        relations=dict()
    )
    if nodes_ != None:
        nodeCluster_.nodes.update(nodes_)
    if relations_ != None:
        nodeCluster_.relations.update(relations_)

    Debug_Tools.debug_msg('{} is created'.format(nodeCluster_), True)
    Debug_Tools.debug_msg('NodeCluster create_cluster ended', False)
    return nodeCluster_

def clear_cluster(nodeCluster_: structure.node_structs.NodeClusterStruct):
    nodeCluster_.nodes=dict()
    nodeCluster_.relations=dict()

def create_relation(nodeCluster_: structure.node_structs.NodeClusterStruct,
                    relation=None,
                    ID=None
                    ):
    """
    create a relation and add it to cluster
    """
    _ID = None
    if ID ==None:
        _ID = str(uuid.uuid1())
    else:
        _ID = ID
    relation_obj = structure.node_structs.RelationStruct(
        ID=_ID, relation_name=relation)
    relation_obj.__hash__()
    nodeCluster_.relations[relation_obj.ID] = relation_obj

    return relation_obj


def refresh_cluster(node_Cluster):
    pass


def generate_IDs(nodeCluster_: structure.node_structs.NodeClusterStruct):
    Debug_Tools.debug_msg('NodeCluster generate_IDs started', True)

    def generate_relative(nodeCluster_: structure.node_structs.NodeClusterStruct):
        """ NOTE all nodes in the loaded into the memory most likely already has relatively unique hashes.
        The point of this function is to not depend on that mechanism to guaranty relatively unique hashes.
        """
        pass
    Debug_Tools.debug_msg('NodeCluster generate_IDs ended', True)


def describe(node_cluster: structure.node_structs.NodeClusterStruct, to_node_data_keys: list = None, mode: str = None, describer_=print, describer_args: list = None):
    Debug_Tools.debug_msg('NodeCluster describe started', True)
    describer_('Cluster name: {} @{}'.format(node_cluster.cluster_name, node_cluster.ID))
    describer_('Relations: %s'%(['\'%s\':\'%s\''%(value.ID, value.relation_name) for value in node_cluster.relations.values()]))
    for node_ in node_cluster.nodes.values():
        node.describe(
            node_=node_,
            to_node_data_keys=to_node_data_keys,
            mode=mode,
            describer_=describer_,
            describer_args=describer_args)
    Debug_Tools.debug_msg('NodeCluster describe ended', True)
