<<<<<<< HEAD
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

from typing import List, Any

#import nodeLib
from . import structure

=======
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

from typing import List, Any

#import nodeLib
from . import structure

>>>>>>> 0.0.2
class Debug_Tools:
    DEBUG_GLOBAL = False
    
    @staticmethod
    def debug_msg(msg, local_debug=0):
        if DEBUG_GLOBAL or local_debug:
            print(msg)
    @classmethod
    def set_debug_global(cls, bool_):
        cls.DEBUG_GLOBAL = True
<<<<<<< HEAD

class Debug_Node:
    @staticmethod
    def describe(node_ : structure.node_structs.Node_Struct, mode:str = None):
        # describe self.node_data
        print()
        if mode == 'compact':
            print("FROM ", node_.node_ID)
            print("---- DATA ----")
            print(node_.data)
            print("---- RELATIONS ----")
            for count,relation_claim in enumerate(node_.relation_claims):
                print("\n-- relation ",count," :")
                #print('from_node : ', _.from_node.node_ID)
                print('to_node : ',  relation_claim.to_node.node_ID)
                print(relation_claim.rel_direction, ' = ', relation_claim.relation.relation_name)
        else:
            print(node_.node_ID)
            print("---- DATA ----")
            for relation_claim in node_.data.items():
                print(relation_claim[0], " : ", relation_claim[1])
            print("---- RELATIONS ----")
            for count,relation_claim in enumerate(node_.relation_claims):
                print("\n-- relation ",count," :")
                print('from_node')
                print( node_.node_ID)
                print('to_node')
                print( relation_claim.to_node.node_ID)
                print('relation_name = ', relation_claim.relation.relation_name, '\nrel_direction = ', relation_claim.rel_direction)
=======
        
>>>>>>> 0.0.2
