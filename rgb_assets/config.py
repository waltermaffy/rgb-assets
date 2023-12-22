import rgb_lib
from dotenv import load_dotenv
from dataclasses import dataclass, field
from typing import List
import os, sys

SUPPORTED_NETWORKS = {
    "regtest": rgb_lib.BitcoinNetwork.REGTEST,
    "testnet": rgb_lib.BitcoinNetwork.TESTNET,
}

def default_transport_endpoints():
    return os.getenv("TRANSPORT_ENDPOINTS", "rpc://proxy:3000/json-rpc").split(",")

@dataclass
class WalletConfig:
    network: str = os.getenv("NET", "regtest")
    wallet_name: str = os.getenv("WALLET_NAME", "rgb_wallet")
    data_dir: str = os.getenv("DATA_DIR", "./data/wallet")
    backup_pass = os.getenv("BACKUP_PASS", "password")
    electrum_url: str = os.getenv("ELECTRUM_URL", "tcp://electrs:50001")
    proxy_url: str = os.getenv("PROXY_URL", "https://proxy.rgbtools.org")
    transport_endpoints: List[str] = field(default_factory=default_transport_endpoints)
    fee_rate: float = float(os.getenv("FEE_RATE", "1.5"))
    vanilla_keychain: int = int(os.getenv("VANILLA_KEYCHAIN", "1"))
    log_path: str = os.getenv("LOG_PATH", "/data/minter.log")

    
def get_config():
    load_dotenv()
    return WalletConfig()


def check_config(cfg: WalletConfig):

    if cfg.network not in SUPPORTED_NETWORKS:
        print(f"Network not supported")
        sys.exit(1)

    cfg.keys_path = os.path.join(cfg.data_dir, f"{cfg.wallet_name}.json")
    cfg.backup_path = os.path.join(cfg.data_dir, f"{cfg.wallet_name}.backup")
    # Check if keys_path and backup path exists
    if os.path.exists(cfg.keys_path) and os.path.exists(cfg.backup_path):
        cfg.init = False
    else:
        cfg.init = True
