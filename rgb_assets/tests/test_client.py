
import pytest
from rgb_assets.tests.utils import fund_wallet
from rgb_assets.models import MintRequest


def test_mint(client, minter, nft_demo):
    print("Getting new blinded utxo for the client to receive NFT...")
    blinded_utxo = client.get_new_blinded_utxo()
    print("Blinded UTXO: ", blinded_utxo)
    mint_request = MintRequest(
        nft_definition=nft_demo,
        blinded_utxo=blinded_utxo
    )
    print("Asking for mint...")
    #txid = client.ask_mint(mint_request)
    txid = minter.mint_nft(mint_request.blinded_utxo, mint_request.nft_definition)
    print("Minted with txid: ", txid)
    assert txid is not None
    assert type(txid) == str