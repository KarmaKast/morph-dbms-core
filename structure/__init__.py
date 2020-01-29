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

import hashlib
import uuid
from typing import List, Set, Dict, Union
from dataclasses import dataclass
from collections import namedtuple

#dict({'custom':Union[int,str], 'auto':str})
@dataclass
class NodeIdStruct:
    ID: Union[int, str]
    node_label: str


@dataclass(repr=False)
class NodeStruct:
    node_ID: NodeIdStruct
    data: dict
    relation_claims: Set['Relation_Claim_Struct']

    def __hash__(self):
        """
        this hash is created using the memory location of this object.
        It is unique among all the nodes currently loaded into the memory
        Returns:
            [type] -- [description]
        """
        # return super().__hash__()
        if not hasattr(self, '_hash'):
            # """
            hasher = hashlib.md5()
            hasher.update(str(id(self)).split(sep=' ')[-1][:-1].encode())
            hash_ = hasher.hexdigest()
            # """
            #hash_ = str(uuid.uuid1())
            hash_ = int(hash_, base=16)
            self._hash = hash_
        return self._hash

    def __repr__(self):
        # return super().__repr__()
        repr_ = 'node \'%s\' with ID : %s'%(self.node_ID.node_label, self.node_ID.ID)
        return repr_


@dataclass
class RelationStruct:
    ID: str
    relation_name: str
    #rel_direction : str

    def __hash__(self):
        """
        this hash is created using the memory location of this object.
        It is unique among all the nodes currently loaded into the memory
        Returns:
            [type] -- [description]
        """
        # return super().__hash__()
        if not hasattr(self, '_hash'):
            # """
            # unique hash using id(obj). unique among the nodes loaded into the memory.
            # """
            hasher = hashlib.md5()
            hasher.update(str(id(self)).split(sep=' ')[-1][:-1].encode())
            hash_ = hasher.hexdigest()
            # """
            # hash_ =
            hash_ = int(hash_, base=16)
            self._hash = hash_

        return self._hash

    def __repr__(self):
        repr_ = 'relation \'%s\' with ID : %s'%(self.relation_name, self.ID)
        return repr_


#directions_ = namedtuple('directions', ['to_to_from','from_to_to'])
#directions_ = directions_('to_to_from','from_to_to')

@dataclass
class RelationClaimStruct:
    # from_node : Node_Struct
    to_node: NodeStruct
    # what is the first node to the second node
    relation: RelationStruct
    rel_direction: str
    # [to_to_from,from_to_to] / [ttf,ftt]

    def __hash__(self):
        """
        this hash is created using the memory location of this object.
        It is unique among all the nodes currently loaded into the memory
        Returns:
            [type] -- [description]
        """
        # return super().__hash__()
        if not hasattr(self, '_hash'):
            # """
            hasher = hashlib.md5()
            hasher.update(str(id(self)).split(sep=' ')[-1][:-1].encode())
            hash_ = hasher.hexdigest()
            hash_ = int(hash_, base=16)
            self._hash = hash_

        return self._hash

    def __repr__(self):
        repr_ = 'relation claim(to_node={}, relation={}, rel_direction={})'.format(
            self.to_node,
            self.relation,
            self.rel_direction
        )
        return repr_


@dataclass
class NodeClusterStruct:
    ID: str
    cluster_name: str
    nodes: Dict[str, NodeStruct]
    relations: dict()
    
    def __repr__(self):
        repr_ = 'node cluster \'%s\' with ID : %s'%(self.cluster_name, self.ID)
        return repr_
