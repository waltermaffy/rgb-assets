import json
import os

import pytest
import rgb_lib
from wallet_helper import export_keys, generate_new_keys, generate_or_load_keys

# Test data
TEST_WALLET_PATH = "test_wallet.json"
TEST_NETWORK = rgb_lib.BitcoinNetwork.REGTEST


def test_generate_or_load_keys_existing_wallet(tmpdir):
    # Create a temporary wallet file for testing existing wallet scenario
    wallet_path = os.path.join(tmpdir, "existing_wallet.json")
    keys_data = {
        "mnemonic": "test mnemonic",
        "xpub": "test xpub",
        "xpub_fingerprint": "test fingerprint",
    }
    with open(wallet_path, "w") as file:
        json.dump(keys_data, file)

    keys = generate_or_load_keys(wallet_path, TEST_NETWORK)

    assert keys is not None
    assert isinstance(keys, rgb_lib.Keys)
    assert keys.mnemonic == "test mnemonic"


def test_generate_or_load_keys_new_wallet(tmpdir):
    # Test scenario when there's no existing wallet file
    wallet_path = os.path.join(tmpdir, "new_wallet.json")

    keys = generate_or_load_keys(wallet_path, TEST_NETWORK)

    assert keys is not None
    assert isinstance(keys, rgb_lib.Keys)
    assert keys.mnemonic is not None


def test_generate_new_keys(tmpdir):
    # Test if new keys are generated properly
    wallet_path = os.path.join(tmpdir, "generate_new_keys_test.json")

    keys = generate_new_keys(wallet_path, TEST_NETWORK)

    assert keys is not None
    assert isinstance(keys, rgb_lib.Keys)
    assert keys.mnemonic is not None
    assert keys.xpub is not None


def test_export_keys(tmpdir):
    # Test export keys functionality
    wallet_path = os.path.join(tmpdir, "export_keys_test.json")
    keys = rgb_lib.generate_keys(TEST_NETWORK)

    export_keys(wallet_path, keys)

    assert os.path.exists(wallet_path)


if __name__ == "__main__":
    pytest.main()
