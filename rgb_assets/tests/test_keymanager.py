import json
import os
from unittest.mock import MagicMock, patch

import pytest
import rgb_lib

from rgb_assets.config import SUPPORTED_NETWORKS, WalletConfig, check_config
from rgb_assets.wallet_helper import (export_keys, generate_new_keys,
                                      generate_or_load_wallet, load_keys,
                                      log_keys, setup_logger)


def test_check_config(sample_config):
    check_config(sample_config)
    assert sample_config.keys_path is not None
    assert sample_config.backup_path is not None


def test_generate_new_keys(sample_config):
    check_config(sample_config)
    assert sample_config.keys_path is not None
    assert sample_config.backup_path is not None
    # Check the return value of generate_new_keys os rgb_lib.Keys
    bitcoin_network = getattr(rgb_lib.BitcoinNetwork, sample_config.network.upper())
    assert type(bitcoin_network) == rgb_lib.BitcoinNetwork
    keys = generate_new_keys(sample_config.keys_path, bitcoin_network)
    assert keys is not None
    assert keys.xpub is not None
    assert keys.mnemonic is not None
    assert type(keys) == rgb_lib.Keys


def test_load_keys(sample_config):
    check_config(sample_config)
    assert sample_config.keys_path is not None
    assert sample_config.backup_path is not None
    # Check the return value of load_keys os rgb_lib.Keys
    bitcoin_network = getattr(rgb_lib.BitcoinNetwork, sample_config.network.upper())
    keys = load_keys(sample_config.keys_path, bitcoin_network)
    assert keys is not None
    assert keys.xpub is not None
    assert keys.mnemonic is not None
    assert type(keys) == rgb_lib.Keys
