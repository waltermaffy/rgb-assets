import os
import json
from unittest.mock import MagicMock, patch
import pytest

from rgb_assets.wallet_helper import (
    setup_logger,
    generate_or_load_wallet,
    load_keys,
    generate_new_keys,
    log_keys,
    export_keys
)

from rgb_assets.config import  SUPPORTED_NETWORKS, WalletConfig, check_config

# Create a fixture for WalletConfig
@pytest.fixture
def sample_config():
    return WalletConfig(
        network="regtest",
        wallet_name="test_wallet",
        data_dir="./data/wallet",
        backup_pass="password",
        electrum_url="tcp://electrs:50001",
        proxy_url="https://proxy.rgbtools.org",
        transport_endpoints=["rpc://proxy:3000/json-rpc"],
        fee_rate=1.5,
        vanilla_keychain=1,
        log_path="./data/test.log"
    )

def test_load_keys(sample_config):
    check_config(sample_config)
    assert sample_config.keys_path is not None
    assert sample_config.backup_path is not None 

    

def test_generate_or_load_wallet(sample_config):
    # Mocking methods and objects to test generate_or_load_wallet function
    with patch('rgb_assets.wallet_helper.check_config'), \
         patch('os.path.exists', return_value=True), \
         patch('rgb_assets.wallet_helper.rgb_lib.BitcoinNetwork'), \
         patch('rgb_assets.wallet_helper.rgb_lib.Wallet'), \
         patch('rgb_assets.wallet_helper.rgb_lib.restore_backup'), \
         patch('builtins.print') as mock_print:
        
        mock_keys = MagicMock()
        mock_wallet = MagicMock()
        mock_online = MagicMock()
        
        mock_keys.xpub = "mock_xpub"
        mock_keys.mnemonic = "mock_mnemonic"
        
        mock_wallet_data = MagicMock()
        mock_wallet_data.return_value = mock_wallet
        mock_wallet.go_online.return_value = mock_online
        
        mock_network = MagicMock()
        mock_network.return_value = "mock_bitcoin_network"

        # Set return values for mocked functions
        mock_keys = MagicMock()
        mock_wallet = MagicMock()
        mock_online = MagicMock()
        mock_network = MagicMock()

        mock_keys.xpub = "mock_xpub"
        mock_keys.mnemonic = "mock_mnemonic"
        mock_online = True
        
        # Execute the function
        wallet, online = generate_or_load_wallet(sample_config)

        # Assertions
        assert wallet == mock_wallet
        assert online == mock_online
        mock_print.assert_called()