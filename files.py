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

from . import structure
from .debug import Debug_Tools


def write(node_: structure.node_structs.Node_Struct, path):

    with open(path, 'w') as file:
        # TODO write a set of relations
        relations = set()
        relations_ = set()
        for rel_claim in node_.relation_claims:
            relations.add(rel_claim.relation)
        relations = list(relations)
        print(relations)
        for relation in relations:
            for relation_ in relations:
                if id(relation) != id(relation_):
                    if relation.relation_name == relation_.relation_name:
                        relations.remove(relation_)
        print(relations)
        # file.write(yaml.dump(relations))
        file.write(yaml.dump(node_))
