import os
from dataclasses import dataclass
from typing import List

from dotenv import load_dotenv


@dataclass
class WalletConfig:
    net: str = os.getenv("NET", "regtest")
    wallet_name: str = os.getenv("WALLET_NAME", "rgb_wallet")
    data_dir: str = os.getenv("DATA_DIR", "/data/wallet")
    electrum_url: str = os.getenv("ELECTRUM_URL", "tcp://electrs:50001")
    proxy_url: str = os.getenv("PROXY_URL", "https://proxy.rgbtools.org")
    transport_endpoints: List[str] = os.getenv(
        "TRANSPORT_ENDPOINTS", "rpc://proxy:3000/json-rpc"
    ).split(",")
    fee_rate: float = float(os.getenv("FEE_RATE", "1.5"))
    vanilla_keychain: int = int(os.getenv("VANILLA_KEYCHAIN", "1"))


def get_config():
    load_dotenv(".env")
    return WalletConfig()
