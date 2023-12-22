import argparse

from rgb_assets.config import WalletConfig
from rgb_assets.models import NftDefinition
from rgb_assets.wallet_helper import generate_or_load_wallet, setup_logger
from rgb_assets.wallet_service import WalletService

logger = setup_logger("./data/client.log")


class NftClient(WalletService):
    def __init__(self, cfg: WalletConfig):
        super().__init__(cfg)

    def ask_mint(self):
        pass


def main():
    parser = argparse.ArgumentParser(description="NFT Client")
    parser.add_argument(
        "--list-assets", "-l", action="store_true", help="List RGB assets of the wallet"
    )
    parser.add_argument(
        "--blinded_utxo", "-b", action="store_true", help="Generate a new blinded UTXO"
    )
    parser.add_argument(
        "--receiving_address",
        "-r",
        action="store_true",
        help="Get the receiving address",
    )

    args = parser.parse_args()

    cfg = (
        WalletConfig()
    )  # Initialize the WalletConfig with default values or set through environment variables
    cfg.wallet_name = "nft_client"
    nft_client = NftClient(cfg)

    if args.blinded_utxo:
        new_blinded_utxo = nft_client.get_new_blinded_utxo()
        print(f"New Blinded UTXO: {new_blinded_utxo}")

    if args.receiving_address:
        receiving_address = nft_client.get_receiving_address()
        print(f"Receiving Address: {receiving_address}")

    if args.list_assets is not None:
        assets = nft_client.get_assets()
        print(f"Wallet assets: {assets}")


if __name__ == "__main__":
    main()
