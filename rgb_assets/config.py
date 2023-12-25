import os
import sys
from dataclasses import dataclass, field
from typing import List

import rgb_lib
from dotenv import load_dotenv
import sys 

SUPPORTED_NETWORKS = {
    "regtest": rgb_lib.BitcoinNetwork.REGTEST,
    "testnet": rgb_lib.BitcoinNetwork.TESTNET,
}
LOG_PATH = "./data/test.log"

def default_transport_endpoints():
    return os.getenv("TRANSPORT_ENDPOINTS", "rpc://proxy:3000/json-rpc").split(",")


@dataclass
class WalletConfig:
    network: str = os.getenv("NET", "regtest")
    init: bool = os.getenv("INIT", True)
    wallet_name: str = os.getenv("WALLET_NAME", "minter_wallet")
    data_dir: str = os.getenv("DATA_DIR", "./data/wallet")
    backup_pass: str = os.getenv("BACKUP_PASS", "password")
    electrum_url: str = os.getenv("ELECTRUM_URL", "tcp://electrs:50001")
    proxy_url: str = os.getenv("PROXY_URL", "https://proxy.rgbtools.org")
    transport_endpoints: List[str] = field(default_factory=default_transport_endpoints)
    fee_rate: float = float(os.getenv("FEE_RATE", "1.5"))
    vanilla_keychain: int = int(os.getenv("VANILLA_KEYCHAIN", "1"))
    log_path: str = os.getenv("LOG_PATH", "./data/minter.log")


def get_config():
    load_dotenv()
    return WalletConfig()


def check_config(cfg: WalletConfig):
    if not hasattr(rgb_lib.BitcoinNetwork, cfg.network.upper()):
        print(f'unsupported Bitcoin network "{cfg.network}"')
        sys.exit(1)

    cfg.keys_path = os.path.join(cfg.data_dir, f"{cfg.wallet_name}.json")
    cfg.backup_path = os.path.join(cfg.data_dir, f"{cfg.wallet_name}.backup")
