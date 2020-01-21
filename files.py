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

#import yaml
import json
import os
from typing import Set

from . import structure, cluster, node
from .debug import Debug_Tools


def write_cluster(node_cluster: structure.node_structs.NodeClusterStruct, path, name=None):
    def write_node(node_: structure.node_structs.NodeStruct, file):
        """
        n'<node name>' n@<node unique hash>
        r'<relation name>' r@<relation unique hash>

        Arguments:
            node_cluster {structure.node_structs.NodeClusterStruct, path} -- [description]
            file {[type]} -- [description]
        """

        # file.write("    {}\n    {}\n    {}\n".format(
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

    if name == None:
        name = node_cluster.cluster_name
    full_path = os.path.join(path, name+'.node_cluster')
    with open(full_path, 'w') as file:
        # WRITE FILE
        file.write("c@%s '%s'\n" %
                   (node_cluster.ID, node_cluster.cluster_name))
        # write all unique relations in the cluster
        for _, relation in node_cluster.relations.items():
            file.write("r@%s '%s'\n" % (relation.ID, relation.relation_name))

        file.write("")

        for node_ in node_cluster.nodes.values():
            file.write("n@%s '%s'\n    %s\n" %
                       (node_.node_ID.ID, node_.node_ID.node_label, json.dumps(node_.data)))
        for node_ in node_cluster.nodes.values():
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


def load_cluster(path):
    cluster_ = None
    file_lines = []
    node_lines = []
    relation_lines = []

    with open(path, 'r') as file:
        for line in file.readlines():
            file_lines.append(line.split('\n')[0])

    # doing: create cluster
    for line in file_lines:
        if line[0] == 'c':
            cluster_ = cluster.create_cluster(
                cluster_name=line.split(line.split(' ')[0])[1].split("'")[1],
                ID=line.split(' ')[0].split('@')[1])
            break
    # doing: create and add relations to cluster
    for line in file_lines:
        # line starts with r
        if line.startswith('r'):
            # if name has "'" that might cause problems
            name = line.split(line.split(' ')[0])[-1]
            name = name.split("'")[1]
            ID = line.split(' ')[0].split('@')[1]
            relation = cluster.create_relation(cluster_,name,ID)
            cluster_.relations[relation.ID] = relation 
    
    # doing: create and add nodes to cluster
    for i in range(len(file_lines)):
        if file_lines[i].startswith('n'):
            # next line should be a data line.
            if i < len(file_lines)-1:
                next_line: str = file_lines[i+1]
                if next_line.startswith('    {'):
                    # ok then current line is node declaration line
                    node_lines.append([file_lines[i], file_lines[i+1]])
                else:
                    relation_lines.append(file_lines[i])
    for line in node_lines:
        dec = line[0]
        # if data has 4 spaces inside it that might cause problems
        data = json.loads(line[1].split('    ')[1])
        ID = dec.split(' ')[0].split('@')[1]
        # if name has "'" that might cause problems
        name = dec.split(dec.split(' ')[0])[1].split("'")[1]
        node_ = node.create_node(
            node_ID={'ID': ID, 'node_label': name}, data=data)
        cluster_.nodes[node_.node_ID.ID] = node_

    # doing: create and add relation claims

    for line in relation_lines:
        # claimant_node claims relation r with direction d to node B
        node_ = line.split(' :')[0].split('n')[1].split('@')[1]
        node_ = cluster_.nodes[node_]

        direction = '->' if '->' in line else '<-'

        to_node = line.split(direction)[1].split('n')[1].split('@')[1]
        # check whether this node exists in this cluster or not
        if to_node not in cluster_.nodes.keys():
            continue
        to_node = cluster_.nodes[to_node]
        
        # todo claim relation
        relation_ = line.split(direction)[0].split(':r@')[-1].split(' ')[0]
        relation_ = cluster_.relations[relation_]
        node.claim_relation(
            node_,
            to_node,
            relation=relation_,
            direction='from_self' if direction=='->' else 'to_self'
            )
        
        

    return cluster_
