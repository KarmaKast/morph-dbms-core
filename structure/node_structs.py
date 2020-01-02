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
from typing import List, Set, Dict, Union
from dataclasses import dataclass
from collections import namedtuple

#dict({'custom':Union[int,str], 'auto':str})
@dataclass
class Node_ID_Struct:
    ID: Union[int, str]
    node_name: str


@dataclass(repr=False)
class Node_Struct:
    node_ID: Node_ID_Struct
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
            hash_ = int(hash_, base=16)
            self._hash = hash_
        return self._hash

    def __repr__(self):
        # return super().__repr__()
        repr_ = 'node ({}) with hash {}'.format(self.node_ID, self._hash)
        return repr_


@dataclass
class Relation_Struct:
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
            hasher = hashlib.md5()
            hasher.update(str(id(self)).split(sep=' ')[-1][:-1].encode())
            hash_ = hasher.hexdigest()
            hash_ = int(hash_, base=16)
            self._hash = hash_

        return self._hash

    def __repr__(self):
        repr_ = 'relation(name={}) with hash {}'.format(
            self.relation_name,
            self._hash,
        )
        return repr_


#directions_ = namedtuple('directions', ['to_to_from','from_to_to'])
#directions_ = directions_('to_to_from','from_to_to')

@dataclass
class Relation_Claim_Struct:
    # from_node : Node_Struct
    to_node: Node_Struct
    # what is the first node to the second node
    relation: Relation_Struct
    rel_direction: str  # [to_to_from,from_to_to] / [ttf,ftt]

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
        repr_ = 'relation claim(to_node={}, relation={}, rel_direction={}) with hash{}'.format(
            self.to_node,
            self.relation,
            'ftt' if self.rel_direction == 'from_to_to' else (
                'ttf' if self.rel_direction == 'to_to_from' else 'INVALID'),
            self._hash
        )
        return repr_


@dataclass
class NodeCluster_Struct:
    clusterName: str
    cluster: Set[Node_Struct]
