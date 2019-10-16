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

from typing import List, Set, Any, Union
from dataclasses import dataclass
from collections import namedtuple

@dataclass
class Node_ID_Struct:
    ID : str
    node_name : str
    
@dataclass(repr=False)
class Node_Struct:
    node_ID : Node_ID_Struct
    data: dict
    relation_claims: List['Relation_Claim_Struct']

@dataclass
class Relation_Struct:
    relation_name : str

directions_ = namedtuple(
    'directions', ['to_to_from','from_to_to']
    )

@dataclass
class Relation_Claim_Struct:
    # from_node : Node_Struct
    to_node : Node_Struct
    # what is the first node to the second node
    relation : Relation_Struct
    rel_direction : str # [to_to_from,from_to_to] / [ttf,ftt]

@dataclass
class NodePack_Struct:
    pack : List[Node_Struct]