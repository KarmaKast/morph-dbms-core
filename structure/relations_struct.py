from typing import NamedTuple, List, Any
from dataclasses import dataclass

#import node_struct

#import relations_struct

@dataclass
class Node_struct:
    data: Any
    relations: List['relation_struct']

@dataclass
class relation_struct:
    from_node : Node_struct
    to_node : Node_struct
    # what is the first node to the second node
    from_to_to : str
    to_to_from : str

    