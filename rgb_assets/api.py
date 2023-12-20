from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from rgb_assets.minter import NftMintingService
from rgb_assets.config import get_config

app = FastAPI()
# Instantiate NftMintingService 
cfg = get_config()
mint_service = NftMintingService(cfg)  # Provide proper configuration here
mint_service.initialize_wallet()

class Definition(BaseModel):
    definition_file: str
    blinded_utxo: Optional[str] = None


@app.get("/mints/")
async def mint_nft():
    try:
        mints = mint_service.get_mints()
        return {"mints": mints}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

@app.get("/new_address/")
async def mint_nft():
    try:
        address = mint_service.get_receiving_address()
        return {"address": address}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")


@app.post("/mint_nft/")
async def mint_nft(definition: Definition):
    try:
        asset_id = mint_service.mint_nft(definition.definition_file)
        return {"message": f"NFT minted with asset ID: {asset_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")


@app.post("/send_nft/")
async def send_nft(blinded_utxo: str, asset_id: str):
    try:
        tx_id = mint_service.send_nft(blinded_utxo, asset_id)
        return {"message": f"NFT sent with txid: {tx_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

if __name__ == "__main__":
    import uvicorn
