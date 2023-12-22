import os

from rgb_assets.config import WalletConfig


def get_test_config():
    return WalletConfig(
        network="regtest",
        wallet_name="test_wallet",
        data_dir="./data/wallet",
        backup_pass="password",
        electrum_url="tcp://localhost:50001",
        proxy_url="https://proxy.rgbtools.org",
        transport_endpoints=["rpc://localhost:3000/json-rpc"],
        fee_rate=1.5,
        vanilla_keychain=1,
        log_path="./data/test.log",
    )


def fund_wallet(wallet):
    try:
        address = wallet.get_address()
        os.system(f"./services.sh fund {address}")
        os.system(f"./services.sh mine")
        return True
    except Exception as e:
        print(e)
        return False
