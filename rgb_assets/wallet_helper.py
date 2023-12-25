import json
import logging
import os

import rgb_lib

from rgb_assets.config import SUPPORTED_NETWORKS, LOG_PATH, WalletConfig, check_config


def setup_logger(file_path: str = "app.log") -> logging.Logger:
    # Create a logger instance
    logger = logging.getLogger("fastapi_logger")
    logger.setLevel(logging.DEBUG)

    # Create a file handler and set the log level
    file_handler = logging.FileHandler(file_path)
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter and set it to the file handler
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger

logger = setup_logger(LOG_PATH)


def generate_or_load_wallet(cfg: WalletConfig):
    check_config(cfg)
    bitcoin_network = getattr(rgb_lib.BitcoinNetwork, cfg.network.upper())

    if cfg.init:
        print("Initializing new wallet")
        keys = generate_new_keys(cfg.keys_path, bitcoin_network)
    else:
        # Load existing wallet
        print("Loading existing wallet..")
        keys = load_keys(cfg.keys_path, bitcoin_network)
        rgb_lib.restore_backup(cfg.backup_path, cfg.backup_pass, cfg.data_dir)
        print("Restore complete!")

    wallet_data = rgb_lib.WalletData(
        cfg.data_dir,
        bitcoin_network,
        rgb_lib.DatabaseType.SQLITE,
        1,
        keys.xpub,
        keys.mnemonic,
        cfg.vanilla_keychain,
    )
    wallet = rgb_lib.Wallet(wallet_data)
    print(cfg.electrum_url)
    online = wallet.go_online(False, cfg.electrum_url)
    print("Wallet initialized!")
    if not os.path.exists(cfg.backup_path):
        wallet.backup(cfg.backup_path, cfg.backup_pass)
        print(f"Wallet backuped to {cfg.backup_path}")
    return wallet, online


def load_keys(keys_path: str, network: rgb_lib.BitcoinNetwork) -> rgb_lib.Keys:
    if not os.path.exists(keys_path):
        raise FileExistsError("Keys not found")
    try:
        # Load keys from json file
        print(f"Loading existing keys at {keys_path}")
        with open(keys_path, "r") as file:
            data = json.load(file)
            mnemonic = data.get("mnemonic", None)
            if not mnemonic:
                raise Exception("No mnemonic found in file.")
    except Exception as e:
        raise Exception(f"Error loading keys from file: {e}")

    return rgb_lib.restore_keys(network, mnemonic)


def generate_new_keys(keys_path: str, network: rgb_lib.BitcoinNetwork) -> rgb_lib.Keys:
    keys = rgb_lib.generate_keys(network)
    log_keys(keys)
    export_keys(keys_path, keys)
    return keys


def log_keys(keys: rgb_lib.Keys):
    logging.info(f"===Wallet keys===")
    logging.info(" - mnemonic:", keys.mnemonic)
    logging.info(" - xpub:", keys.xpub)
    logging.info(f"- xpub fingerprint: {keys.xpub_fingerprint}")


def export_keys(keys_path: str, keys: rgb_lib.Keys):
    if not os.path.exists(os.path.dirname(keys_path)):
        os.makedirs(os.path.dirname(keys_path))

    with open(keys_path, "w") as file:
        json.dump(
            {
                "mnemonic": keys.mnemonic,
                "xpub": keys.xpub,
                "xpub_fingerprint": keys.xpub_fingerprint,
            },
            file,
            indent=4,
        )
