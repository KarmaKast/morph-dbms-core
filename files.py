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
import shutil
from typing import Set

from . import structure, cluster, node, constants
from .debug import Debug_Tools


def create_database(path: str, name: str):
    """
    database is a folder

    Arguments:
        path {str} -- [description]
        name {str} -- [description]
    """

    # todo: create a folder <database-name> with a .<database-file-extension> file in it

    if not os.path.exists(os.path.join(path, name)):
        os.makedirs(os.path.join(path, name))
        os.makedirs(os.path.join(path, name+'/clusters'))
        os.makedirs(os.path.join(path, name+'/nodes'))
        os.makedirs(os.path.join(path, name+'/relations'))
        file_path = os.path.join(
            path, name, '.'+constants.file_extensions['database'])
        with open(file_path, 'w') as file:
            # file is empty for now. could be used as a config file later
            file.write('')


def archive_database(path: str, name: str, mode, remove):
    """[summary]

    Arguments:
        path {str} -- [description]
        name {str} -- [description]
        mode {[type]} -- 'pack','unpack'
        remove {[type]} -- [description]
    """
    # check if the path is a node database
    # remove any existing zip with that name and create a new one
    if mode == 'pack':
        if os.path.exists(os.path.join(path, name)):
            archive_name = name+'.'+constants.file_extensions['database']
            if archive_name in os.listdir():
                # todo: delete the archive file
                os.remove(os.path.join(path, archive_name))
            """shutil.make_archive(
                archive_name,
                format='zip',
                root_dir=path,
                base_dir=os.path.join(path, name),
            )"""
            shutil.make_archive(
                archive_name,
                format='zip',
                root_dir=path,
                #base_dir=os.path.join(path, name),
            )
            shutil.move(os.path.join(os.getcwd(), archive_name +
                                     '.zip'), os.path.join(path, archive_name))

        if remove == True:
            # todo: remove the database folder and its contents
            shutil.rmtree(os.path.join(path, name))

    elif mode == 'unpack':
        archive_name = name+'.'+constants.file_extensions['database']
        if archive_name in os.listdir(path):
            shutil.unpack_archive(
                os.path.join(path, archive_name), path, format='zip')
        if remove == True:
            os.remove(os.path.join(path, archive_name))

#create_database(os.path.join(os.getcwd(), 'data'), 'test')


def write_cluster(node_cluster: structure.node_structs.NodeClusterStruct, path, database_name):
    # todo: check if database folder exists
    if not os.path.exists(os.path.join(path, database_name)):
        # todo: check if database archive exists
        if os.path.exists(os.path.join(path, database_name+'.'+constants.file_extensions['database'])):
            # unpack database
            archive_database(path, database_name, mode='unpack', remove=False)
        else:
            # todo: create a new database wit <database-name>
            create_database(path, database_name)

    # todo: write cluster to database folder
    database_path = os.path.join(path, database_name)
    cluster_file_name = node_cluster.ID + '.' + \
        constants.file_extensions['cluster']
    cluster_file_path = os.path.join(
        database_path, 'clusters', cluster_file_name)

    # doing: step1: writing cluster decleration file
    with open(cluster_file_path, 'w') as cluster_file_obj:
        cluster_file_obj.write(json.dumps(
            {
                'ID': node_cluster.ID,
                'name': node_cluster.cluster_name,
                'nodes': list(node_cluster.nodes.keys()),
                'relations': list(node_cluster.relations.keys())
            }
        ))

    # todo: step2: write relation files for relations in the cluster
    for relation_ in node_cluster.relations.values():
        relation_file_name = relation_.ID + '.' + \
            constants.file_extensions['relation']
        relation_file_path = os.path.join(
            database_path, 'relations', relation_file_name)
        with open(relation_file_path, 'w') as relation_file_obj:
            relation_file_obj.write(json.dumps(
                {
                    'ID': relation_.ID,
                    'name': relation_.relation_name
                }
            ))

    # todo: step3: write node files for nodes in the cluster
    for node_ in node_cluster.nodes.values():
        node_file_name = node_.node_ID.ID + '.' + \
            constants.file_extensions['node']
        node_file_path = os.path.join(
            database_path, 'nodes', node_file_name)

        rel_claims = list()
        for rel_claim in node_.relation_claims:
            dir_str = ''
            if rel_claim.rel_direction == 'from_self':
                dir_str = '->'
            elif rel_claim.rel_direction == 'to_self':
                dir_str = '<-'
            rel_claims.append(
                [rel_claim.relation.ID, dir_str, rel_claim.to_node.node_ID.ID])
        with open(node_file_path, 'w') as node_file_obj:
            node_file_obj.write(json.dumps(
                {
                    'ID': node_.node_ID.ID,
                    'node_label': node_.node_ID.node_label,
                    'data': node_.data,
                    'rel_claims': rel_claims
                }
            ))


def load_cluster(path: str, database_name: str, cluster_name: str, ID: str = None, mode='limited'):
    """[summary]
    todo: implement mode
    Arguments:
        path {str} -- [description]
        database_name {str} -- [description]
        cluster_name {str} -- [description]

    Keyword Arguments:
        Id {str} -- [description] (default: {None})
        mode {str} -- 'limited1' for loading only things that the cluster owns. 
                        'limited2' for loading only things that the database has
                        'full' loads what ever can be loaded (default: 
                        {'limited'})
    """
    # check if database path exists
    database_path = os.path.join(path, database_name)
    assert os.path.exists(database_path)

    cluster_ = None
    """
    If ID is given ignore name.
    else: get ID using name.
    """
    cluster_ID = None
    if ID != None:
        cluster_ID = ID
    else:
        """
        get list of cluster files under database/clusters/
        search for clusters using name
        get cluster ID
        """
        # clusters_: clusters with name <name>
        cluster_IDs = []
        for cluster_file_name in os.listdir(os.path.join(database_path, 'clusters')):
            # there shouldn't be any folders inside database/clusters/ for now
            cluster_file_path = os.path.join(
                database_path, 'clusters', cluster_file_name)
            assert os.path.isfile(cluster_file_path)
            with open(cluster_file_path, 'r') as cluster_file_obj:
                cluster_file_data = json.loads(cluster_file_obj.readline())
                if cluster_file_data['name'] == cluster_name:
                    cluster_IDs.append(cluster_file_data['ID'])

        # note: for now Im not dealing with multiple clusters with same name
        try:
            assert not len(cluster_IDs) > 1
        except AssertionError as error:
            Debug_Tools.debug_msg(
                'There are multiple clusters with same name: %s' % (cluster_IDs))
            raise

        cluster_ID = cluster_IDs[0]

    cluster_file_path = os.path.join(
        database_path, 'clusters', cluster_ID+'.'+constants.file_extensions['cluster'])
    with open(cluster_file_path, 'r') as cluster_file_obj:
        cluster_file_data = json.loads(cluster_file_obj.readline())
        cluster_ = cluster.create_cluster(
            cluster_file_data['name'], cluster_file_data['ID'])

        # todo: load relations
        for relation_ID in cluster_file_data['relations']:
            # doing: assuming relation exists in this database
            # load relation with this ID from database
            relation_file_name = relation_ID+'.' + \
                constants.file_extensions['relation']
            relation_file_path = os.path.join(
                database_path, 'relations', relation_file_name)
            with open(relation_file_path, 'r') as relation_file_obj:
                relation_file_data = json.loads(relation_file_obj.readline())
                cluster.create_relation(
                    cluster_, relation_file_data['name'], relation_file_data['ID'])

        # todo: load nodes
        # doing: pass 1 load all nodes without relation claims
        for node_ID in cluster_file_data['nodes']:
            # doing: assuming node exists in this database
            node_file_name = node_ID+'.'+constants.file_extensions['node']
            node_file_path = os.path.join(
                database_path, 'nodes', node_file_name)
            with open(node_file_path, 'r') as node_file_obj:
                node_file_data = json.loads(node_file_obj.readline())
                node_ = node.create_node(
                    {'ID': node_file_data['ID'],
                        'node_label': node_file_data['node_label']},
                    data=node_file_data['data']
                )
                cluster_.nodes[node_.node_ID.ID] = node_
        # doing: pass 2 load relation claims for all nodes
        for node_ID in cluster_file_data['nodes']:
            node_file_name = node_ID+'.'+constants.file_extensions['node']
            node_file_path = os.path.join(
                database_path, 'nodes', node_file_name)
            with open(node_file_path, 'r') as node_file_obj:
                node_file_data = json.loads(node_file_obj.readline())
                for rel_claim_data in node_file_data['rel_claims']:
                    
                    # doing: get relation
                    relation = None
                    if rel_claim_data[0] in cluster_.relations.keys():
                        relation = cluster_.relations[rel_claim_data[0]]
                    else:
                        # doing: assuming relation exists in this database
                        relation_file_name = rel_claim_data[0] + \
                            '.' + constants.file_extensions['relation']
                        relation_file_path = os.path.join(
                            database_path, 'relations', relation_file_name)
                        with open(relation_file_path, 'r') as relation_file_obj:
                            relation_file_data = json.loads(
                                relation_file_obj.readline())
                            relation = structure.node_structs.RelationStruct(
                                ID=relation_file_data['ID'], relation_name=relation_file_data['name'])
                            relation.__hash__()

                    # doing: parse direction
                    direction = 'from_self' if rel_claim_data[1] == '->' else 'to_self'
                    
                    # doing: get to_node
                    to_node = None
                    if rel_claim_data[2] in cluster_.nodes.keys():
                        to_node = cluster_.nodes[rel_claim_data[2]]
                    else:
                        # doing: assuming to_node exists in this database
                        to_node_file_name = rel_claim_data[2] + \
                            '.'+constants.file_extensions['node']
                        to_node_file_path = os.path.join(
                            database_path, 'nodes', to_node_file_name)
                        with open(to_node_file_path, 'r') as to_node_file_obj:
                            to_node_file_data = json.loads(
                                to_node_file_obj.readline())
                            to_node = node.create_node(
                                {'ID': to_node_file_data['ID'],
                                 'node_label': to_node_file_data['node_label']},
                                data=to_node_file_data['data']
                            )

                    node.claim_relation(
                        cluster_.nodes[node_ID], to_node, relation, direction)

    # todo: cluster_ = cluster.create_cluster(cluster_name, cluster_ID)

    return cluster_
