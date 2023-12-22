from rgb_assets.models import NftDefinition
from rgb_assets.config import WalletConfig
from rgb_assets.wallet_helper import generate_or_load_wallet, setup_logger
import argparse

logger = setup_logger("./data/client.log")

class NftClient:
    def __init__(self, cfg: WalletConfig):
        self.cfg = cfg
        self.wallet, self.online = generate_or_load_wallet(cfg)
        logger.info(f"Create {amount} new utxos")

    def create_new_utxos(self, amount: int):
        try:
            count = self.wallet.create_utxos(self.online, True, amount,
                                            None, self.cfg.fee_rate)
            if count > 0:
                print(f'{count} new UTXOs created')
        except rgb_lib.RgbLibError.AllocationsAlreadyAvailable:
            pass
        except rgb_lib.RgbLibError.InsufficientBitcoins as err:
            print((f'Insufficient funds ({err.available} available sats).\n'
                   f'Funds can be sent to the following address'),
                  self.wallet.get_address())


    def get_new_blinded_utxo(self):
        try:
            self.create_new_utxos(1)
            print(self.cfg.transport_endpoints)
            blind_data = self.wallet.blind_receive(None, None, None, self.cfg.transport_endpoints, 1)        
            logger.info(f"New blinded utxo: {data}")
            return data.recipient_id
        except rgb_lib.RgbLibError as err:  # pylint: disable=catching-non-exception
            print(f'Error generating blind data: {err}')
            logger.error(err)
            raise err

    def get_address(self):
        return self.wallet.get_address()

    def get_assets(self):
        assets = self.wallet.list_assets(filter_asset_schemas=[])
        return assets.cfa

    def refresh(self):
        self.wallet.refresh(self.online, None, [])




def main():
    parser = argparse.ArgumentParser(description="NFT Client")
    parser.add_argument(
        "--list-assets",
        "-l",
        action="store_true",
        help="List RGB assets of the wallet"
    )
    parser.add_argument(
        "--blinded_utxo",
        "-b",
        action="store_true",
        help="Generate a new blinded UTXO"
    )
    parser.add_argument(
        "--receiving_address",
        "-r",
        action="store_true",
        help="Get the receiving address"
    )
    
    args = parser.parse_args()

    cfg = WalletConfig()  # Initialize the WalletConfig with default values or set through environment variables
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
