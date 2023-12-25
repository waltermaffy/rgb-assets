import pytest

from rgb_assets.config import SUPPORTED_NETWORKS, WalletConfig, get_config
from rgb_assets.minter import NftMintingService
from rgb_assets.models import NftDefinition
from rgb_assets.wallet_service import WalletService
from rgb_assets.client import NftClient
from rgb_assets.tests.utils import fund_wallet

def get_test_config(local: bool = True):
    return WalletConfig(
        network="regtest",
        wallet_name="test_wallet",
        data_dir="./data/wallet",
        backup_pass="password",
        electrum_url="tcp://localhost:50001" if local else "tcp://electrs:50001",
        proxy_url="https://proxy.rgbtools.org",
        transport_endpoints=["rpc://localhost:3000/json-rpc"] if local else ["rpc://proxy:3000/json-rpc"],
        fee_rate=1.5,
        vanilla_keychain=1,
        log_path="./data/test.log",
    )


@pytest.fixture(scope="module")
def test_config():
    return get_test_config()


@pytest.fixture(scope="module")
def wallet():
    cfg = get_test_config()
    wallet = WalletService(cfg)
    fund_wallet(wallet)
    yield wallet


@pytest.fixture(scope="module")
def minter():
    cfg = get_test_config()
    cfg.wallet_name = "minter"
    cfg.init = True
    minter = NftMintingService(cfg)
    fund_wallet(minter)
    return minter

@pytest.fixture(scope="module")
def client():
    cfg = get_test_config()
    cfg.wallet_name = "client"
    cfg.init = True
    minter_url = "http://localhost:8000"
    client = NftClient(cfg, minter_url)
    fund_wallet(client)
    return client


@pytest.fixture(scope="module")
def nft_demo():
    return NftDefinition(
        name="RGB Asset",
        precision=0,
        amounts=[1],
        description="A new incredible collectible",
        encoded_data='',
        file_type = 'JPEG'
)
