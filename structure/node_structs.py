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


    
