import rgb_lib

from rgb_assets.config import WalletConfig
from rgb_assets.wallet_helper import generate_or_load_wallet, logger
import os 


class WalletService:
    def __init__(self, cfg: WalletConfig):
        self.cfg = cfg
        self.wallet, self.online = generate_or_load_wallet(cfg)
        # Fund wallet if regtest
        self.fund_wallet()

    def get_address(self):
        return self.wallet.get_address()

    def create_new_utxos(self, amount: int):
        try:
            count = self.wallet.create_utxos(
                self.online, True, amount, None, self.cfg.fee_rate
            )
            if count > 0:
                logger.info(f"{count} new UTXOs created")
            return count
        except rgb_lib.RgbLibError.AllocationsAlreadyAvailable:
            pass
        except rgb_lib.RgbLibError.InsufficientBitcoins as err:
            print(
                f"Insufficient funds ({err.available} available sats).\n"
                f"Funds can be sent to the following address: {self.wallet.get_address()}"
            )

    def get_new_blinded_utxo(self):
        try:
            self.create_new_utxos(1)
            blind_data = self.wallet.blind_receive(
                None, None, None, self.cfg.transport_endpoints, 1
            )
            logger.info(f"New blinded utxo: {blind_data}")
            return blind_data.recipient_id
        except rgb_lib.RgbLibError as err:  # pylint: disable=catching-non-exception
            print(f"Error generating blind data: {err}")
            logger.error(err)
            return None

    def refresh(self):
        self.wallet.refresh(self.online, None, [])

    def get_cfa_assets(self):
        self.refresh()
        assets = self.wallet.list_assets(filter_asset_schemas=[])
        return assets.cfa

    def list_unspent(self):
        self.refresh()
        return self.wallet.list_unspents(self.online, settled_only=False)

    def fund_wallet(self):
        try:
            if self.cfg.network == "regtest":
                address = self.get_address()
                os.system(f"./services.sh fund {address}")
                os.system(f"./services.sh mine")
        except Exception as e:
            print(e)
            