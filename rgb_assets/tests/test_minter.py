import pytest
from unittest.mock import MagicMock, patch
from rgb_assets.minter import NftMintingService

@pytest.fixture
def mock_wallet():
    return MagicMock()

@pytest.fixture
def nft_minting_service(mock_wallet):
    with patch('rgb_assets.minter.generate_or_load_wallet') as mock_generate_or_load_wallet:
        mock_generate_or_load_wallet.return_value = (mock_wallet, True)
        yield NftMintingService()

def test_create_new_utxos(nft_minting_service, mock_wallet):
    nft_minting_service.create_new_utxos(1)
    mock_wallet.create_utxos.assert_called_once_with(True, 1, None, nft_minting_service.cfg.fee_rate)

def test_get_new_blinded_utxo(nft_minting_service, mock_wallet):
    mock_wallet.blind_receive.return_value = MagicMock(recipient_id="123abc")
    result = nft_minting_service.get_new_blinded_utxo()
    assert result == "123abc"
    mock_wallet.blind_receive.assert_called_once_with(None, None, None, nft_minting_service.cfg.transport_endpoints, 1)

# Add more tests for other methods as needed...
