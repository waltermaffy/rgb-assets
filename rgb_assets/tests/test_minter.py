import pytest
import rgb_lib

from rgb_assets.minter import NftMintingService
from rgb_assets.tests.utils import fund_wallet
from rgb_assets.models import DataConverter
import os 


def test_issue(minter, nft_demo):
    # Test issue a CFA asset
    assets = minter.get_cfa_assets()
    # There should be no assets yet
    assert len(assets) == 0
    asset_id = minter.issue_asset_cfa(nft_demo)
    assets = minter.get_cfa_assets()
    assert len(assets) > 0
    assert asset_id is not None
    assert type(asset_id) == str
    assert asset_id.startswith("rgb:")


def test_send_nft(minter, nft_demo):
    # Mint a CFA asset and try to send it to a new utxob
    blinded_utxo = minter.get_new_blinded_utxo()
    asset_id = minter.issue_asset_cfa(nft_demo)
    txid = minter.send_nft(blinded_utxo, asset_id)
    assert txid is not None
    assert type(txid) == str


def test_mint_nft(minter, nft_demo):
    # Mint a CFA asset and try to send it to a new utxob
    blinded_utxo = minter.get_new_blinded_utxo()
    n_assets = len(minter.get_cfa_assets())
    txid = minter.mint_nft(blinded_utxo, nft_demo)
    assert len(minter.get_cfa_assets()) == n_assets + 1
    assert txid is not None
    assert type(txid) == str

def test_issue_from_file(minter):
    file_path = "rgb_assets/tests/data/nft_definition.json"
    n_assets = len(minter.get_cfa_assets())
    asset_id = minter.issue_nft_from_file(file_path)
    assert len(minter.get_cfa_assets()) == n_assets + 1
    assert asset_id.startswith("rgb:")

def test_issue_from_folder(minter):
    data_path = "rgb_assets/tests/data"
    n_assets = len(minter.get_cfa_assets())
    asset_ids = minter.issue_nft_from_folder(data_path)
    assert len(minter.get_cfa_assets()) > n_assets
    assert len(asset_ids) > 0
    assert asset_ids[0].startswith("rgb:")


def test_mint_from_file(minter, wallet):
    data_path = "rgb_assets/tests/data/nft_definition.json"
    blinded_utxo = wallet.get_new_blinded_utxo()
    n_assets = len(minter.get_cfa_assets())
    txid = minter.mint_nft_from_file(blinded_utxo, data_path)
    assert len(minter.get_cfa_assets()) > n_assets
    assert txid is not None
    assert type(txid) == str


def test_mint_with_encoding(minter, nft_demo):
    file_path = "rgb_assets/tests/data/sample.png"
    encode_data = DataConverter.encode_data(file_path)
    nft_demo.encoded_data = encode_data
    nft_demo.file_type = "PNG"
    blinded_utxo = minter.get_new_blinded_utxo()
    n_assets = len(minter.get_cfa_assets())
    txid = minter.mint_nft(blinded_utxo, nft_demo)
    assert len(minter.get_cfa_assets()) == n_assets + 1
    assert txid is not None

def test_dataconverter_decode():
    file_path = "rgb_assets/tests/data/sample.png"
    encode_data = DataConverter.encode_data(file_path)
    assert encode_data is not None
    assert type(encode_data) == str
    assert encode_data != ""
    decode_data = DataConverter.decode_data(encode_data, "PNG", "rgb_assets/tests")
    assert decode_data is not None
    assert type(decode_data) == str
    assert os.path.exists(decode_data)
    assert decode_data != ""
    assert decode_data.endswith("png")
