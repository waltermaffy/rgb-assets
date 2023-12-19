from dataclasses import dataclass
from typing import List

import rgb_lib


@dataclass
class NFTMint:
    asset: rgb_lib.AssetCfa
    blinded_utxo: rgb_lib.BlindedUtxo
    txid: str = ""
