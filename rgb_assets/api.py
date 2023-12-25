from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from rgb_assets.minter import NftMintingService
from rgb_assets.models import NftDefinition, MintRequest, SendRequest
from rgb_assets.config import get_config

app = FastAPI()
cfg = get_config()
mint_service = NftMintingService(cfg)


class Definition(BaseModel):
    definition_file: str
    blinded_utxo: Optional[str] = None


@app.get("/refresh")
async def refresh():
    try:
        mint_service.refresh()
        return {"message": "Refresh OK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")


@app.get("/cfa_assets")
async def get_cfa_assets():
    try:
        mints = mint_service.get_cfa_assets()
        return {"mints": mints}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")


@app.get("/new_address")
async def get_address():
    try:
        address = mint_service.get_address()
        return {"address": address}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")


@app.get("/new_blinded_utxo")
async def get_new_blinded_utxo():
    try:
        blinded_utxo = mint_service.get_new_blinded_utxo()
        return {"blinded_utxo": blinded_utxo}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")


@app.get("/list_unspent")
async def list_unspent():
    try:
        unspents = mint_service.list_unspent()
        return {"unspents": unspents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")


@app.post("/issue_cfa")
async def issue_cfa(definition: NftDefinition):
    try:
        asset_id = mint_service.issue_asset_cfa(definition)
        return {"message": f"Issued new CFA asset", "assset_id": asset_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

# TODO: (Better naming should be defined) CFA --> NFT 

@app.post("/mint_nft")
async def mint_nft(mint_request: MintRequest):
    try:
        tx_id = mint_service.mint_nft(mint_request.blinded_utxo, mint_request.nft_definition)
        return {"message": "NFT minted and sent", "tx_id": tx_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

@app.post("/send_nft")
async def send_nft(send_request: SendRequest):
    try:
        tx_id = mint_service.send_nft(send_request.blinded_utxo, send_request.asset_id)
        return {"message": "NFT sent", "tx_id": tx_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
