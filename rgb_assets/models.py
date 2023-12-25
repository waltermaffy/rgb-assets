import base64
import os
import uuid
from dataclasses import dataclass
from typing import List, Optional
from rgb_assets.wallet_helper import logger

import rgb_lib
from pydantic import BaseModel
import json 

class NftDefinition(BaseModel):
    name: str
    precision: int = 0
    amounts: List[int] = [1]
    description: str = ""
    parent_id: Optional[str] = None
    file_path: Optional[str] = None
    encoded_data: Optional[str] = None
    file_type: Optional[str] = "JPEG"

    @staticmethod
    def from_file(file_path: str) -> "NftDefinition":
        try:
            with open(file_path, "r") as file:
                json_data = json.load(file)
                return NftDefinition.parse_obj(json_data)
        except FileNotFoundError:
            logger.error(f"File '{file_path}' not found.")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            return None

    def to_file(self, file_path: str):
        with open(file_path, "w") as file:
            json.dump(self.dict(), file, indent=4)
    
    @staticmethod
    def from_folder(folder_path: str) -> List["NftDefinition"]:
        definitions = []
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path) and file_path.endswith('.json'):
                definition = NftDefinition.from_file(file_path)
                if definition:
                    definitions.append(definition)
        return definitions


class BlindedUxto(BaseModel):
    blinded_utxo: str


class MintRequest(BaseModel):
    nft_definition: NftDefinition
    blinded_utxo: str

class SendRequest(BaseModel):
    asset_id: str
    blinded_utxo: str


class NftMint(BaseModel):
    asset: NftDefinition
    blinded_utxo: BlindedUxto
    txid: str = ""
    created_at: str = ""


class DataConverter:
    @staticmethod
    def encode_data(file_path: str) -> str:
        try:
            with open(file_path, "rb") as file:
                data = file.read()
                return base64.b64encode(data).decode("utf-8")
        except Exception as e:
            logger.error(f"Error encoding data: {e}")
            return None

    @staticmethod
    def decode_data(encoded_data: str, file_type: str, data_dir: str) -> Optional[str]:
        try:
            mint_folder = os.path.join(data_dir, "mint_data")
            os.makedirs(mint_folder, exist_ok=True) 
            decoded_data = base64.b64decode(encoded_data)
            file_name = f"{str(uuid.uuid4())}.{file_type.lower()}"
            file_path = os.path.join(mint_folder, file_name)
            with open(file_path, "wb") as file:
                file.write(decoded_data)
            return file_path
        except Exception as e:
            logger.error(f"Error decoding data: {e}")
            return None
