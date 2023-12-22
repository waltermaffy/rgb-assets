
import pytest
from rgb_assets.tests.utils import fund_wallet
from rgb_assets.models import MintRequest


def test_mint(client, minter, nft_demo):
    # Fund both wallets
    fund_wallet(client)
    blinded_utxo = client.get_new_blinded_utxo()
    mint_request = MintRequest(
        nft_definition=nft_demo,
        blinded_utxo=blinded_utxo
    )
    txid = client.ask_mint(mint_request)
    assert txid is not None
    assert type(txid) == str