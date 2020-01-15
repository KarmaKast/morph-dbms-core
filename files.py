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

import yaml
from typing import Set

from . import structure
from .debug import Debug_Tools


def write_cluster(node_cluster: structure.node_structs.NodeClusterStruct, path):
    def write_node(node_: structure.node_structs.NodeStruct, file):
        """
        n'<node name>' n@<node unique hash>
        r'<relation name>' r@<relation unique hash>

        Arguments:
            node_cluster {structure.node_structs.NodeClusterStruct, path} -- [description]
            file {[type]} -- [description]
        """
        
        #file.write("    {}\n    {}\n    {}\n".format(
        #    node_.node_ID.node_label, node_.data))
        dir_str = ''
        for relation_claim in node_.relation_claims:
            if relation_claim.rel_direction == 'from_self':
                dir_str = '->'
            elif relation_claim.rel_direction == 'to_self':
                dir_str = '<-'
            file.write("n@{} :r@{} {} n@{}\n".format(node_.node_ID.ID,
                                                   relation_claim.relation.ID, 
                                                   dir_str,
                                                   relation_claim.to_node.node_ID.ID))
            pass

    with open(path, 'w') as file:
        # WRITE FILE
        file.write("c@%s '%s'\n" % (node_cluster.ID, node_cluster.cluster_name))
        # write all unique relations in the cluster
        for _,relation in node_cluster.relations.items():
            file.write("r@%s '%s'\n"%(relation.ID, relation.relation_name))
            
        file.write("")
        
        for node_ in node_cluster.nodes:
            file.write("n@%s '%s'\n    %s\n"%(node_.node_ID.ID, node_.node_ID.node_label, node_.data))
        for node_ in node_cluster.nodes:
            write_node(node_, file=file)
        """
        for relation in relations:
            for relation_ in relations:
                if id(relation) != id(relation_):
                    if relation.relation_name == relation_.relation_name:
                        relations.remove(relation_)
        Debug_Tools.debug_msg(relations, False)
        # file.write(yaml.dump(relations))
        file.write(yaml.dump(node_))
        """
