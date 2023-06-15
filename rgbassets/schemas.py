from dataclasses import dataclass
from typing import List


@dataclass
class RGB21Asset:
    name: str
    precision: int
    amounts: List[int]
    description: str
    parent_id: str = None
    file_path: str = None
    
@dataclass
class RGB20Asset:
    name: str
    precision: int
    amounts: List[int]
    ticker: str
    