from typing import List, Set, Dict, Any

from . import structure
from .debug import Debug_Tools
from . import node


def create_cluster(cluster_name=None,
                    nodes_: Set[structure.node_structs.NodeStruct] = None, 
                    relations_: Set[structure.node_structs.RelationStruct] = None):
    """
    creates a list of nodes from a related collected of nodes using a nodes_

    Arguments:
        nodes_ {structure.node_structs.NodeStruct} -- any node that is related to the collection of related nodes

    Returns:
        [type] -- [description]
    """
    Debug_Tools.debug_msg('NodeCluster create_cluster started')

    nodeCluster_ = structure.node_structs.NodeClusterStruct(
        cluster_name=cluster_name,
        nodes=set(),
        relations=set()
    )
    if nodes_ != None:
        nodeCluster_.nodes.update(nodes_)
    if relations_ != None:
        nodeCluster_.relations.update(relations_)

    Debug_Tools.debug_msg('NodeCluster create_cluster ended')
    return nodeCluster_

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
    describer_('Cluster name: {}'.format(node_cluster.cluster_name))
    for node_ in node_cluster.nodes:
        node.describe(
            node_=node_,
            to_node_data_keys=to_node_data_keys,
            mode=mode,
            describer_=describer_,
            describer_args=describer_args)
    Debug_Tools.debug_msg('NodeCluster describe ended', True)