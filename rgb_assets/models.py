from dataclasses import dataclass
import rgb_lib
from typing import List, Optional
from pydantic import BaseModel


class NftDefinition(BaseModel):
    name: str
    precision: int = 0
    amounts: List[int] = [1]
    description: str = ''
    parent_id: Optional[str] = None
    file_path:Optional[str] = None

class BlindedUxto(BaseModel):
    blinded_utxo: str

class MintRequest(BaseModel):
    asset_id: str
    blinded_utxo: str


class NftMint(BaseModel):
    asset: NftDefinition
    blinded_utxo: BlindedUxto
    txid: str = ""
