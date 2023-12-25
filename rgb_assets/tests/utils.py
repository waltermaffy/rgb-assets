import os

from rgb_assets.config import WalletConfig


def fund_wallet(wallet):
    try:
        address = wallet.get_address()
        os.system(f"./services.sh fund {address}")
        os.system(f"./services.sh mine")
        return True
    except Exception as e:
        print(e)
        return False
