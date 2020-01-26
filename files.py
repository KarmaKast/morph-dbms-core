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
import zipfile

from . import structure, cluster, node, constants
from .debug import Debug_Tools


def create_database(path: str, name: str):
    """
    database is a zipfile

    Arguments:
        path {str} -- [description]
        name {str} -- [description]
    """

    # todo: create a <database-name>.<database-file_extension> file
    # doing: check if it already exists at <cwd>/data/
    exists = False
    database_file_name = name+'.'+constants.file_extensions['database']
    for path_ in os.listdir(path):
        if path_ == database_file_name and os.path.isdir(os.path.join(os.getcwd(), path)):
            exists = True
            break

    if exists == False:
        # doing: create the database file
        database_file_path = os.path.join(path, database_file_name)
        zipfile.ZipFile(database_file_path, mode='x')
        """
        # doing: creating empty folders 'clusters', 'nodes', 'relations'
        with zipfile.ZipFile(database_file_path, 'a') as database:
            empty_file_name = 'test.txt'
            empty_file_path = os.path.join(path, empty_file_name)
            with open(empty_file_path) as file:
                file.write('')
            database.write(empty_file_path, 'cluster/'+empty_file_name)
            database.write(empty_file_path, 'nodes/'+empty_file_name)
            database.write(empty_file_path, 'relations/'+empty_file_name)"""


#create_database(os.path.join(os.getcwd(), 'data'), 'test')

def write_cluster(node_cluster: structure.node_structs.NodeClusterStruct, path, database_name):
    # doing: create the database file if not already
    create_database(path, database_name)
    # todo: write the cluster and nodes in it
    full_name = database_name+'.'+constants.file_extensions['database']
    with zipfile.ZipFile(os.path.join(path, full_name), 'a') as database:
        # doing: write cluster
        cluster_file_name = node_cluster.ID + \
            '.'+constants.file_extensions['cluster']
        cluster_file_path = os.path.join(path, cluster_file_name)
        with open(cluster_file_path, 'w') as cluster_file:
            cluster_file.write(json.dumps(
                {
                    'ID': node_cluster.ID,
                    'name': node_cluster.cluster_name,
                    'nodes': list(node_cluster.nodes.keys()),
                    'relations': list(node_cluster.relations.keys())
                }
            ))
        database.write(cluster_file_path, 'clusters/'+cluster_file_name)
        os.remove(cluster_file_path)
        # doing: write nodes in the cluster. each in a separate file
        for node_ in node_cluster.nodes.values():
            # doing: write node into a separate file, add it to zip and remove it
            node_file_name = node_.node_ID.ID + '.' + \
                constants.file_extensions['node']
            node_file_path = os.path.join(path, node_file_name)
            rel_claims = list()
            for rel_claim in node_.relation_claims:
                dir_str = ''
                if rel_claim.rel_direction == 'from_self':
                    dir_str = '->'
                elif rel_claim.rel_direction == 'to_self':
                    dir_str = '<-'
                rel_claims.append(
                    [rel_claim.relation.ID, dir_str, rel_claim.to_node.node_ID.ID])

            with open(node_file_path, 'w') as node_file:
                node_file.write(json.dumps(
                    {
                        'ID': node_.node_ID.ID,
                        'node_label': node_.node_ID.node_label,
                        'data': node_.data,
                        'rel_claims': rel_claims
                    }
                ))
            database.write(node_file_path, 'nodes/'+node_file_name)
            os.remove(node_file_path)
        # todo: write relations
        for relation in node_cluster.relations.values():
            relations_file_name = relation.ID + '.' + \
                constants.file_extensions['relation']
            relations_file_path = os.path.join(path, relations_file_name)
            with open(relations_file_path, 'w') as rel_file:

                rel_file.write(json.dumps(
                    {
                        'ID': relation.ID,
                        'name': relation.relation_name
                    }
                ))
            database.write(relations_file_path,
                           'relations/'+relations_file_name)
            os.remove(relations_file_path)

        
def load_cluster(path, cluster_name=None, ID=None):
    """ 
    path : database path
    If ID is given use it
    If name is given use it. If multiple clusters have same name print all the ID and return None
    """
    cluster_ = None
    nodes = dict()
    relations = dict()
    
    # note: file names not files
    all_clusters = []
    all_nodes = []
    all_relations = []
    
    
    
    with zipfile.ZipFile(path, 'r') as database:
        
        for name in database.namelist():
            if 'clusters/' in name:
                all_clusters.append(name.split('clusters/')[1].split('.'+constants.file_extensions['cluster'])[0])
                # clusters.append(name)
            elif 'nodes/' in name:
                all_nodes.append(name.split('nodes/')[1].split('.'+constants.file_extensions['node'])[0])
            elif 'relations/' in name:
                all_relations.append(name.split('relations/')[1].split('.'+constants.file_extensions['relation'])[0])
        # print(cluster_files)
        cluster_ID = None
        if ID == None:
            # todo: get
            for cluster_ID_ in all_clusters:
                with database.open('clusters/'+cluster_ID_+'.'+constants.file_extensions['cluster'], mode='r') as cluster_file:
                    cluster_file_data = json.loads(cluster_file.readline())
                    if cluster_file_data['name'] == cluster_name:
                        cluster_ID = cluster_ID_
                        break
        else:
            cluster_ID = ID
        
        cluster_file_data = None
        with database.open('clusters/'+cluster_ID+'.'+constants.file_extensions['cluster'], mode='r') as cluster_file:
            cluster_file_data = json.loads(cluster_file.readline())
        # print(cluster_file_data)
        cluster_ = cluster.create_cluster(
            cluster_file_data['name'], cluster_file_data['ID'])
        # todo: load relations belonging to this cluster and add them to this cluster
        for relation_ID in cluster_file_data['relations']:
            # doing: search relation_ID in the database
            exist_in_database =  True if relation_ID in all_relations else False
            # doing: create relation obj from data in relation file and add it to cluster obj
            if exist_in_database == True:
                with database.open('relations/'+relation_ID+'.'+constants.file_extensions['relation'], 'r') as rel_file:
                    rel_file_data = json.loads(rel_file.readline())
                    # note
                    relation_ = cluster.create_relation(
                        cluster_, rel_file_data['name'], rel_file_data['ID'])
                    relations.update({relation_.ID: relation_})
                    #print('cluster %s RELATIONS %s'%(cluster_.cluster_name, relations.values()))
            else:
                print('relation with ID %s does not exist in database' %
                      (relation_ID))
                
        # todo: load nodes and add them to this cluster
        for node_ID in cluster_file_data['nodes']:
            # doing: search node_ID in the database
            exist_in_database = True if node_ID in all_nodes else False
            if exist_in_database == True:
                with database.open('nodes/'+node_ID+'.'+constants.file_extensions['node'], 'r') as node_file:
                    node_file_data = json.loads(node_file.readline())
                    # note
                    node_ = node.create_node(
                        {'ID': node_file_data['ID'], 'node_label': node_file_data['node_label']}, data=node_file_data['data'])
                    # todo: add relation cliams
                    # node.claim_relation
                    cluster_.nodes[node_.node_ID.ID] = node_
                    nodes[node_.node_ID.ID] = node_
            else:
                print('node with ID %s does not exist in database' % (node_ID))

        for node_ID in cluster_file_data['nodes']:
            # doing: search node_ID in the database
            exist_in_database = True if node_ID in all_nodes else False
            if exist_in_database == True:
                with database.open('nodes/'+node_ID+'.'+constants.file_extensions['node'], 'r') as node_file:
                    node_file_data = json.loads(node_file.readline())
                    # note: each rel_claim has a relation_ID, direction, to_node_ID
                    rel_claims_data = node_file_data['rel_claims']
                    # note
                    #node_ = node.create_node({'ID':node_file_data['ID'],'node_label':node_file_data['node_label']},data=node_file_data['data'])
                    # node.claim_relation
                    print(node_file_data['rel_claims'])
                    # todo: get relation_ID
                    for rel_claim_data in node_file_data['rel_claims']:
                        relation_ID = rel_claim_data[0]
                        to_node_ID = rel_claim_data[2]
                        #print('cluster %s RELATIONS %s'%(cluster_.cluster_name, relations.values()))
                        # note: the relation_ID might not belong to this cluster and if so has not been loaded yet
                        if relation_ID not in cluster_file_data['relations']:
                            # relation_ID does not exist in this cluster
                            continue
                        if to_node_ID not in cluster_file_data['nodes']:
                            continue
                        
                        relation_ = relations[relation_ID]
                        print(relation_)
                        direction = 'from_self' if rel_claim_data[1] == '->' else '<-'
                        to_node_ = nodes[to_node_ID]
                        print(to_node_)
                        curr_node_ = nodes[node_ID]
                        print(curr_node_)
                        node.claim_relation(curr_node_,to_node_,relation_,direction)

                    # cluster_.nodes[node_.node_ID.ID].relation_claims
            else:
                print('node with ID %s does not exist in database' % (node_ID))

    return cluster_
