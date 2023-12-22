import pytest

from rgb_assets.config import SUPPORTED_NETWORKS, WalletConfig, get_config
from rgb_assets.minter import NftMintingService
from rgb_assets.models import NftDefinition
from rgb_assets.tests.utils import get_test_config
from rgb_assets.wallet_service import WalletService


@pytest.fixture
def sample_config():
    return get_test_config()


@pytest.fixture
def wallet():
    cfg = get_test_config()
    wallet = WalletService(cfg)
    yield wallet


@pytest.fixture
def minter():
    cfg = get_test_config()
    minter = NftMintingService(cfg)
    yield minter


@pytest.fixture
def nft_demo():
    return NftDefinition(
        name="RGB Asset",
        precision=0,
        amounts=[1],
        description="A new incredible collectible",
        parent_id=None,
        file_path=None,
    )
