# Copyright 2019 Sree Chandan.R . All rights reserved.
#
# Copyright [yyyy] [name of copyright owner]
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

from typing import List, Any
from dataclasses import dataclass

#import relations_struct
@dataclass
class node_ID:
    ID : str
    node_name : str
    
@dataclass
class node_struct:
    node_ID : node_ID
    data: dict
    relations: List['relation_struct']

@dataclass
class relation_struct:
    from_node : node_struct
    to_node : node_struct
    # what is the first node to the second node
    rel_from_to_to : str
    rel_to_to_from : str


    
